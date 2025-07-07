import os
import time
from humancursor.system_cursor import SystemCursor
from humancursor.utilities.virtual_display import virtual_display


def start_sys_demo(use_virtual_display: bool = True):
    """Start system demonstration with Linux optimizations
    
    Args:
        use_virtual_display: Whether to use virtual display for headless operation
    """
    print('Initializing Linux System Demo')
    
    # Setup virtual display if requested and no display is available
    if use_virtual_display and not os.environ.get('DISPLAY'):
        print('No display detected, starting virtual display...')
        with virtual_display(1920, 1080):
            _run_demo()
    else:
        _run_demo()


def _run_demo():
    """Run the actual demo"""
    try:
        # Initialize SystemCursor with Linux optimizations
        cursor = SystemCursor()
        
        print('Starting mouse movement demonstration...')
        print('Screen size:', cursor.size())
        
        # Get screen dimensions for safe movement
        screen_width, screen_height = cursor.size()
        
        # Calculate safe movement boundaries (10% margin)
        margin = 0.1
        min_x = int(screen_width * margin)
        max_x = int(screen_width * (1 - margin))
        min_y = int(screen_height * margin)
        max_y = int(screen_height * (1 - margin))
        
        print(f'Movement boundaries: ({min_x}, {min_y}) to ({max_x}, {max_y})')
        
        # Demo movements with Linux-optimized coordinates
        movements = [
            [min_x + 200, min_y + 200],  # Top-left area
            [max_x - 200, min_y + 200],  # Top-right area
            [max_x - 200, max_y - 200],  # Bottom-right area
            [min_x + 200, max_y - 200],  # Bottom-left area
            [screen_width // 2, screen_height // 2],  # Center
        ]
        
        # Perform demonstration movements
        for i in range(3):  # 3 complete cycles
            print(f'Movement cycle {i + 1}/3')
            
            for j, target in enumerate(movements):
                print(f'  Moving to point {j + 1}: {target}')
                
                try:
                    # Move with human-like curve
                    cursor.move_to(target, steady=False)
                    time.sleep(0.5)  # Brief pause to see movement
                    
                    # Perform a test click (safe on virtual display)
                    if j == len(movements) - 1:  # Only click at center
                        print('  Performing test click...')
                        cursor.click_on(target, clicks=1)
                        
                except Exception as e:
                    print(f'  Warning: Movement to {target} failed: {e}')
                    continue
                    
            print(f'Cycle {i + 1} completed')
            time.sleep(1)  # Pause between cycles
            
        # Demonstrate additional features
        print('Demonstrating additional features...')
        
        # Test drag and drop
        print('Testing drag and drop...')
        start_point = [screen_width // 4, screen_height // 2]
        end_point = [3 * screen_width // 4, screen_height // 2]
        
        try:
            cursor.drag_and_drop(start_point, end_point, duration=2.0)
            print('Drag and drop completed')
        except Exception as e:
            print(f'Drag and drop failed: {e}')
            
        # Test scrolling
        print('Testing scroll functionality...')
        center_point = [screen_width // 2, screen_height // 2]
        
        try:
            cursor.scroll(center_point, direction='down', clicks=3)
            time.sleep(0.5)
            cursor.scroll(center_point, direction='up', clicks=3)
            print('Scroll test completed')
        except Exception as e:
            print(f'Scroll test failed: {e}')
            
        # Test different mouse buttons
        print('Testing different mouse buttons...')
        test_point = [screen_width // 2, screen_height // 2]
        
        try:
            cursor.click_on(test_point, button='left')
            time.sleep(0.2)
            cursor.click_on(test_point, button='right')
            time.sleep(0.2)
            cursor.click_on(test_point, button='middle')
            print('Mouse button tests completed')
        except Exception as e:
            print(f'Mouse button tests failed: {e}')
            
        print('Linux System Demo completed successfully!')
        
    except Exception as e:
        print(f'Demo failed with error: {e}')
        print('This might be due to missing dependencies or permissions.')
        print('Try running: sudo apt-get install libx11-dev libxtst-dev')


def test_virtual_display():
    """Test virtual display functionality"""
    print('Testing virtual display functionality...')
    
    try:
        from humancursor.utilities.virtual_display import VirtualDisplay
        
        display = VirtualDisplay(1920, 1080)
        if display.start():
            print('Virtual display started successfully')
            
            cursor = SystemCursor()
            cursor.move_to([960, 540])  # Center of virtual screen
            print('Mouse movement on virtual display successful')
            
            display.stop()
            print('Virtual display stopped')
        else:
            print('Failed to start virtual display')
            
    except Exception as e:
        print(f'Virtual display test failed: {e}')


if __name__ == '__main__':
    import sys
    
    # Check command line arguments
    use_virtual = '--no-virtual' not in sys.argv
    
    if '--test-virtual' in sys.argv:
        test_virtual_display()
    else:
        start_sys_demo(use_virtual_display=use_virtual)
        
    print('Demo finished. Use --help for options:')