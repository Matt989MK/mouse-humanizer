import sys
import time
import os
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

from humancursor.web_cursor import WebCursor
from humancursor.utilities.virtual_display import virtual_display


def setup_linux_chrome_driver() -> Optional[webdriver.Chrome]:
    """Setup Chrome driver with Linux optimizations"""
    try:
        chrome_options = Options()
        
        # Linux-specific optimizations
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Faster loading
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        
        # Check if running in headless environment
        if not os.environ.get('DISPLAY'):
            print('No display detected, running in headless mode')
            chrome_options.add_argument('--headless=new')
            
        # Set window size for consistent behavior
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Try to create driver
        try:
            driver = webdriver.Chrome(options=chrome_options)
            print('Chrome driver initialized successfully')
            return driver
        except WebDriverException as e:
            print(f'Failed to initialize Chrome driver: {e}')
            print('Make sure ChromeDriver is installed and in PATH')
            return None
            
    except Exception as e:
        print(f'Error setting up Chrome driver: {e}')
        return None


def setup_firefox_driver() -> Optional[webdriver.Firefox]:
    """Setup Firefox driver as fallback"""
    try:
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from selenium.webdriver.firefox.service import Service as FirefoxService
        
        firefox_options = FirefoxOptions()
        
        # Linux-specific optimizations
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--disable-gpu')
        
        # Check if running in headless environment
        if not os.environ.get('DISPLAY'):
            firefox_options.add_argument('--headless')
            
        # Set window size
        firefox_options.add_argument('--width=1920')
        firefox_options.add_argument('--height=1080')
        
        driver = webdriver.Firefox(options=firefox_options)
        print('Firefox driver initialized successfully')
        return driver
        
    except Exception as e:
        print(f'Failed to initialize Firefox driver: {e}')
        return None


def start_web_demo(use_virtual_display: bool = True):
    """Start web demonstration with Linux optimizations
    
    Args:
        use_virtual_display: Whether to use virtual display for headless operation
    """
    print('Initializing Linux Web Demo')
    
    # Setup virtual display if needed
    if use_virtual_display and not os.environ.get('DISPLAY'):
        print('No display detected, starting virtual display...')
        with virtual_display(1920, 1080):
            _run_web_demo()
    else:
        _run_web_demo()


def _run_web_demo():
    """Run the actual web demo"""
    driver = None
    
    try:
        print('Setting up web driver...')
        
        # Try Chrome first, then Firefox
        driver = setup_linux_chrome_driver()
        if not driver:
            print('Chrome failed, trying Firefox...')
            driver = setup_firefox_driver()
            
        if not driver:
            print('Could not initialize any web driver')
            print('Please install ChromeDriver or GeckoDriver')
            return
            
        # Initialize WebCursor with Linux optimizations
        cursor = WebCursor(driver)
        
        print('Web driver ready, starting demonstration...')
        
        # Navigate to test page
        test_url = 'https://humanbenchmark.com/tests/chimp'
        print(f'Navigating to: {test_url}')
        
        try:
            driver.get(test_url)
            driver.maximize_window()
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print('Page loaded successfully')
            
        except TimeoutException:
            print('Page load timeout, trying alternative demo...')
            _run_simple_demo(driver, cursor)
            return
        except Exception as e:
            print(f'Navigation failed: {e}, trying alternative demo...')
            _run_simple_demo(driver, cursor)
            return
            
        # Show cursor for debugging
        if cursor.show_cursor():
            print('Visual cursor indicator enabled')
            
        # Wait for page elements
        time.sleep(2)
        
        try:
            # Look for start button with multiple selectors
            start_button = None
            selectors = [
                '//button[contains(text(), "Start Test")]',
                '//button[contains(text(), "START")]',
                '//button[@class*="start"]',
                '//div[contains(text(), "Start")][@role="button"]'
            ]
            
            for selector in selectors:
                try:
                    start_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f'Found start button with selector: {selector}')
                    break
                except TimeoutException:
                    continue
                    
            if not start_button:
                print('Could not find start button, trying alternative demo...')
                _run_simple_demo(driver, cursor)
                return
                
            # Click start button
            print('Clicking start button...')
            if cursor.click_on(start_button):
                print('Start button clicked successfully')
            else:
                print('Failed to click start button')
                return
                
            time.sleep(2)
            
            # Look for game elements
            print('Looking for game elements...')
            
            # Try to find numbered blocks
            for attempt in range(5):
                try:
                    blocks = driver.find_elements(By.XPATH, '//div[@data-cellnumber]')
                    if blocks:
                        print(f'Found {len(blocks)} game blocks')
                        
                        # Sort blocks by number
                        blocks_sorted = sorted(blocks, 
                                             key=lambda x: int(x.get_attribute('data-cellnumber')))
                        
                        # Click blocks in order
                        for i, block in enumerate(blocks_sorted):
                            print(f'Clicking block {i+1}/{len(blocks_sorted)}')
                            if cursor.click_on(block):
                                time.sleep(0.2)  # Brief pause between clicks
                            else:
                                print(f'Failed to click block {i+1}')
                                break
                                
                        # Look for continue button
                        try:
                            continue_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, 
                                    '//button[contains(text(), "Continue") or contains(text(), "CONTINUE")]'))
                            )
                            print('Clicking continue button...')
                            cursor.click_on(continue_button)
                            time.sleep(2)
                            
                        except TimeoutException:
                            print('No continue button found, test may have ended')
                            break
                            
                    else:
                        print(f'No blocks found on attempt {attempt + 1}')
                        time.sleep(1)
                        
                except Exception as e:
                    print(f'Error in game loop: {e}')
                    break
                    
            print('Game demonstration completed')
            
        except Exception as e:
            print(f'Game interaction failed: {e}')
            _run_simple_demo(driver, cursor)
            
        # Hide cursor indicator
        cursor.hide_cursor()
        print('Demo completed successfully')
        
    except Exception as e:
        print(f'Web demo failed: {e}')
        print('This might be due to missing web drivers or network issues')
        
    finally:
        if driver:
            print('Closing web driver...')
            try:
                driver.quit()
            except:
                pass


def _run_simple_demo(driver, cursor):
    """Run a simple demo using basic page elements"""
    print('Running simple web demo...')
    
    try:
        # Navigate to a simple page
        driver.get('data:text/html,<html><body style="margin:50px;"><h1>HumanCursor Linux Demo</h1><button id="btn1" style="margin:20px;padding:10px;">Button 1</button><button id="btn2" style="margin:20px;padding:10px;">Button 2</button><div style="width:200px;height:200px;background:lightblue;margin:20px;"></div></body></html>')
        
        time.sleep(1)
        
        # Find and click buttons
        try:
            btn1 = driver.find_element(By.ID, "btn1")
            btn2 = driver.find_element(By.ID, "btn2")
            
            print('Clicking Button 1...')
            cursor.click_on(btn1)
            time.sleep(1)
            
            print('Clicking Button 2...')
            cursor.click_on(btn2)
            time.sleep(1)
            
            # Test movement to different areas
            print('Testing cursor movement...')
            cursor.move_to([300, 300])
            time.sleep(0.5)
            cursor.move_to([600, 400])
            time.sleep(0.5)
            cursor.move_to([400, 200])
            
            print('Simple demo completed')
            
        except Exception as e:
            print(f'Simple demo failed: {e}')
            
    except Exception as e:
        print(f'Could not create simple demo: {e}')


def test_browser_capabilities():
    """Test browser capabilities and optimizations"""
    print('Testing browser capabilities...')
    
    driver = setup_linux_chrome_driver()
    if not driver:
        driver = setup_firefox_driver()
        
    if not driver:
        print('No web driver available for testing')
        return
        
    try:
        cursor = WebCursor(driver)
        
        # Navigate to test page
        driver.get('data:text/html,<html><body><h1>Capability Test</h1></body></html>')
        
        # Get browser info
        info = cursor.get_browser_info()
        print('Browser Information:')
        for key, value in info.items():
            print(f'  {key}: {value}')
            
        # Test viewport info
        viewport = cursor.human.get_viewport_info()
        print('Viewport Information:')
        for key, value in viewport.items():
            print(f'  {key}: {value}')
            
    except Exception as e:
        print(f'Capability test failed: {e}')
        
    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    # Check command line arguments
    use_virtual = '--no-virtual' not in sys.argv
    
    if '--test-capabilities' in sys.argv:
        test_browser_capabilities()
    else:
        start_web_demo(use_virtual_display=use_virtual)
        
    print('Web demo finished. Options:')
    print('  --no-virtual: Skip virtual display setup')
    print('  --test-capabilities: Test browser capabilities')