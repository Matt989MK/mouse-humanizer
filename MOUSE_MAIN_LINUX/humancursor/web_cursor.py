import time
import random
from typing import Union, List, Optional

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException, TimeoutException

from humancursor.utilities.web_adjuster import WebAdjuster


class WebCursor:
    """Linux-optimized web cursor for human-like web automation"""
    
    def __init__(self, driver):
        """Initialize WebCursor for Linux
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.__driver = driver
        self.__action = ActionChains(self.__driver, duration=0)
        self.human = WebAdjuster(self.__driver)
        self.origin_coordinates = [0, 0]
        self._linux_optimizations = self._detect_linux_capabilities()
        
    def _detect_linux_capabilities(self) -> dict:
        """Detect Linux-specific browser capabilities"""
        capabilities = {
            'supports_smooth_scroll': True,
            'supports_hover_events': True,
            'supports_native_events': False,
            'headless_mode': False
        }
        
        try:
            # Check if headless
            if hasattr(self.__driver, 'execute_script'):
                result = self.__driver.execute_script(
                    "return window.navigator.webdriver || window.outerWidth === 0"
                )
                capabilities['headless_mode'] = bool(result)
                
            # Check native events support
            if hasattr(self.__driver, 'capabilities'):
                caps = self.__driver.capabilities
                capabilities['supports_native_events'] = caps.get('nativeEvents', False)
                
        except Exception:
            pass
            
        return capabilities

    def move_to(self,
                element: Union[WebElement, List[int]],
                relative_position: Optional[List[float]] = None,
                absolute_offset: bool = False,
                origin_coordinates: Optional[List[int]] = None,
                steady: bool = False) -> Union[List[int], bool]:
        """Move cursor to element or coordinates with human-like movement
        
        Args:
            element: Target WebElement or coordinates [x, y]
            relative_position: Position within element [0-1, 0-1]
            absolute_offset: Whether coordinates are absolute offsets
            origin_coordinates: Starting coordinates (uses current if None)
            steady: Use steady movement with less randomization
            
        Returns:
            Final coordinates or False if failed
        """
        try:
            # Ensure element is visible
            if not self.scroll_into_view_of_element(element):
                return False
                
            # Set origin coordinates
            if origin_coordinates is None:
                origin_coordinates = self.origin_coordinates
                
            # Execute movement with Linux optimizations
            final_coords = self.human.move_to(
                element,
                origin_coordinates=origin_coordinates,
                absolute_offset=absolute_offset,
                relative_position=relative_position,
                steady=steady
            )
            
            self.origin_coordinates = final_coords
            return final_coords
            
        except Exception as e:
            print(f"Warning: Move operation failed: {e}")
            return False

    def click_on(self,
                 element: Union[WebElement, List[int]],
                 number_of_clicks: int = 1,
                 click_duration: float = 0,
                 relative_position: Optional[List[float]] = None,
                 absolute_offset: bool = False,
                 origin_coordinates: Optional[List[int]] = None,
                 steady: bool = False,
                 button: str = 'left') -> bool:
        """Click on element or coordinates with human-like movement
        
        Args:
            element: Target WebElement or coordinates [x, y]
            number_of_clicks: Number of clicks to perform
            click_duration: Duration to hold click (for long press)
            relative_position: Position within element [0-1, 0-1]
            absolute_offset: Whether coordinates are absolute offsets
            origin_coordinates: Starting coordinates
            steady: Use steady movement
            button: Mouse button ('left', 'right', 'middle')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Move to target
            move_result = self.move_to(
                element,
                relative_position=relative_position,
                absolute_offset=absolute_offset,
                origin_coordinates=origin_coordinates,
                steady=steady
            )
            
            if not move_result:
                return False
                
            # Perform click with Linux optimizations
            return self._perform_click(
                number_of_clicks, click_duration, button
            )
            
        except Exception as e:
            print(f"Warning: Click operation failed: {e}")
            return False

    def _perform_click(self,
                      number_of_clicks: int,
                      click_duration: float,
                      button: str = 'left') -> bool:
        """Perform click action with Linux optimizations"""
        try:
            for _ in range(number_of_clicks):
                if click_duration > 0:
                    # Long press
                    if button == 'right':
                        self.__action.context_click().pause(click_duration)
                    else:
                        self.__action.click_and_hold().pause(click_duration).release()
                else:
                    # Regular click
                    if button == 'right':
                        self.__action.context_click()
                    elif button == 'middle':
                        # Middle click - use JavaScript for better Linux compatibility
                        self.__driver.execute_script("""
                            var event = new MouseEvent('mousedown', {
                                bubbles: true,
                                cancelable: true,
                                button: 1
                            });
                            document.elementFromPoint(arguments[0], arguments[1]).dispatchEvent(event);
                            
                            event = new MouseEvent('mouseup', {
                                bubbles: true,
                                cancelable: true,
                                button: 1
                            });
                            document.elementFromPoint(arguments[0], arguments[1]).dispatchEvent(event);
                        """, self.origin_coordinates[0], self.origin_coordinates[1])
                    else:
                        self.__action.click()
                        
                # Add pause between multiple clicks
                if number_of_clicks > 1:
                    self.__action.pause(random.uniform(0.170, 0.280))
                    
            self.__action.perform()
            return True
            
        except Exception as e:
            print(f"Warning: Click performance failed: {e}")
            return False

    def move_by_offset(self, x: int, y: int, steady: bool = False) -> bool:
        """Move cursor by offset with human-like movement
        
        Args:
            x: Horizontal offset in pixels
            y: Vertical offset in pixels
            steady: Use steady movement
            
        Returns:
            True if successful, False otherwise
        """
        try:
            final_coords = self.human.move_to(
                [x, y],
                absolute_offset=True,
                steady=steady
            )
            
            self.origin_coordinates = final_coords
            return True
            
        except Exception as e:
            print(f"Warning: Move by offset failed: {e}")
            return False

    def drag_and_drop(self,
                      drag_from_element: Union[WebElement, List[int]],
                      drag_to_element: Union[WebElement, List[int]],
                      drag_from_relative_position: Optional[List[float]] = None,
                      drag_to_relative_position: Optional[List[float]] = None,
                      steady: bool = False) -> bool:
        """Drag and drop with human-like movement
        
        Args:
            drag_from_element: Source element or coordinates
            drag_to_element: Target element or coordinates
            drag_from_relative_position: Position within source element
            drag_to_relative_position: Position within target element
            steady: Use steady movement
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Move to source element
            if drag_from_relative_position is None:
                move_result = self.move_to(drag_from_element, steady=steady)
            else:
                move_result = self.move_to(
                    drag_from_element,
                    relative_position=drag_from_relative_position,
                    steady=steady
                )
                
            if not move_result:
                return False
                
            # Start drag operation
            if drag_to_element is None:
                # Simple click if no target
                self.__action.click().perform()
                return True
            else:
                # Click and hold
                self.__action.click_and_hold().perform()
                
                # Add small delay for drag recognition
                time.sleep(0.1)
                
                # Move to target
                if drag_to_relative_position is None:
                    move_result = self.move_to(drag_to_element, steady=steady)
                else:
                    move_result = self.move_to(
                        drag_to_element,
                        relative_position=drag_to_relative_position,
                        steady=steady
                    )
                    
                if not move_result:
                    # Release if move failed
                    self.__action.release().perform()
                    return False
                    
                # Release
                self.__action.release().perform()
                return True
                
        except Exception as e:
            print(f"Warning: Drag and drop failed: {e}")
            try:
                # Ensure mouse is released
                self.__action.release().perform()
            except:
                pass
            return False

    def control_scroll_bar(self,
                          scroll_bar_element: WebElement,
                          amount_by_percentage: float,
                          orientation: str = "horizontal",
                          steady: bool = False) -> bool:
        """Control scroll bar with human-like movement
        
        Args:
            scroll_bar_element: Scroll bar element
            amount_by_percentage: Position as percentage (0.0 to 1.0)
            orientation: 'horizontal' or 'vertical'
            steady: Use steady movement
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure valid percentage
            amount_by_percentage = max(0.0, min(1.0, amount_by_percentage))
            
            # Move to scroll bar
            move_result = self.move_to(scroll_bar_element)
            if not move_result:
                return False
                
            # Click and hold
            self.__action.click_and_hold().perform()
            
            # Calculate target position
            if orientation.lower() == "horizontal":
                target_position = [
                    amount_by_percentage,
                    random.uniform(0.3, 0.7)  # Random vertical position
                ]
            else:
                target_position = [
                    random.uniform(0.3, 0.7),  # Random horizontal position
                    amount_by_percentage
                ]
                
            # Move to target position
            self.move_to(
                scroll_bar_element,
                relative_position=target_position,
                steady=steady
            )
            
            # Release
            self.__action.release().perform()
            return True
            
        except Exception as e:
            print(f"Warning: Scroll bar control failed: {e}")
            try:
                self.__action.release().perform()
            except:
                pass
            return False

    def scroll_into_view_of_element(self, element: Union[WebElement, List[int]]) -> bool:
        """Scroll element into view if needed
        
        Args:
            element: Target element or coordinates
            
        Returns:
            True if successful or already in view, False otherwise
        """
        try:
            if isinstance(element, WebElement):
                # Check if element is in viewport
                is_in_viewport = self.__driver.execute_script("""
                    var element = arguments[0];
                    var rect = element.getBoundingClientRect();
                    return (
                        rect.top >= 0 &&
                        rect.left >= 0 &&
                        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
                    );
                """, element)
                
                if not is_in_viewport:
                    # Scroll into view with smooth behavior on Linux
                    scroll_behavior = 'smooth' if self._linux_optimizations['supports_smooth_scroll'] else 'auto'
                    self.__driver.execute_script(f"""
                        arguments[0].scrollIntoView({{
                            behavior: '{scroll_behavior}',
                            block: 'center',
                            inline: 'center'
                        }});
                    """, element)
                    
                    # Wait for scroll to complete
                    time.sleep(random.uniform(0.8, 1.4))
                    
                return True
                
            elif isinstance(element, list):
                # For coordinates, assume they're valid
                return True
            else:
                print("Warning: Invalid element type for scroll_into_view")
                return False
                
        except Exception as e:
            print(f"Warning: Scroll into view failed: {e}")
            return False

    def scroll_smooth(self,
                     direction: str = 'down',
                     clicks: int = 3,
                     element: Optional[WebElement] = None) -> bool:
        """Perform smooth scrolling with Linux optimizations
        
        Args:
            direction: 'up', 'down', 'left', 'right'
            clicks: Number of scroll steps
            element: Element to scroll (page if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            target_element = element if element else self.__driver.find_element("tag name", "body")
            
            # Use web adjuster's smooth scroll
            return self.human.scroll_smooth(
                target_element,
                direction=direction,
                amount=clicks,
                smooth=True
            )
            
        except Exception as e:
            print(f"Warning: Smooth scroll failed: {e}")
            return False

    def show_cursor(self) -> bool:
        """Show visual cursor indicator for debugging
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.__driver.execute_script('''
                let dot;
                function displayRedDot() {
                    // Get the cursor position
                    const x = event.clientX;
                    const y = event.clientY;

                    if (!dot) {
                        // Create a new div element for the red dot if it doesn't exist
                        dot = document.createElement("div");
                        // Style the dot with CSS
                        dot.style.position = "fixed";
                        dot.style.width = "5px";
                        dot.style.height = "5px";
                        dot.style.borderRadius = "50%";
                        dot.style.backgroundColor = "red";
                        dot.style.zIndex = "9999";
                        dot.style.pointerEvents = "none";
                        // Add the dot to the page
                        document.body.appendChild(dot);
                    }

                    // Update the dot's position
                    dot.style.left = x + "px";
                    dot.style.top = y + "px";
                }

                // Add event listener to update the dot's position on mousemove
                document.addEventListener("mousemove", displayRedDot);
            ''')
            return True
            
        except Exception as e:
            print(f"Warning: Show cursor failed: {e}")
            return False

    def hide_cursor(self) -> bool:
        """Hide visual cursor indicator
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.__driver.execute_script('''
                // Remove cursor indicator
                const dots = document.querySelectorAll('div[style*="background-color: red"]');
                dots.forEach(dot => {
                    if (dot.style.position === 'fixed' && dot.style.width === '5px') {
                        dot.remove();
                    }
                });
                
                // Remove event listener
                document.removeEventListener("mousemove", displayRedDot);
            ''')
            return True
            
        except Exception as e:
            print(f"Warning: Hide cursor failed: {e}")
            return False

    def get_cursor_position(self) -> List[int]:
        """Get current cursor position
        
        Returns:
            Current cursor coordinates [x, y]
        """
        return self.origin_coordinates.copy()

    def reset_cursor_position(self) -> bool:
        """Reset cursor position to origin
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.origin_coordinates = [0, 0]
            self.human.reset_origin()
            return True
            
        except Exception as e:
            print(f"Warning: Reset cursor position failed: {e}")
            return False

    def wait_for_element_clickable(self,
                                  element: WebElement,
                                  timeout: int = 10) -> bool:
        """Wait for element to be clickable with Linux optimizations
        
        Args:
            element: Target element
            timeout: Timeout in seconds
            
        Returns:
            True if element becomes clickable, False otherwise
        """
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            WebDriverWait(self.__driver, timeout).until(
                EC.element_to_be_clickable(element)
            )
            return True
            
        except TimeoutException:
            print(f"Warning: Element not clickable after {timeout} seconds")
            return False
        except Exception as e:
            print(f"Warning: Wait for clickable failed: {e}")
            return False

    def get_browser_info(self) -> dict:
        """Get browser and system information
        
        Returns:
            Dictionary with browser and system info
        """
        try:
            info = self.__driver.execute_script('''
                return {
                    userAgent: navigator.userAgent,
                    platform: navigator.platform,
                    webdriver: navigator.webdriver,
                    windowSize: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    },
                    screenSize: {
                        width: screen.width,
                        height: screen.height
                    },
                    devicePixelRatio: window.devicePixelRatio
                };
            ''')
            
            # Add Linux-specific information
            info['linux_optimizations'] = self._linux_optimizations
            info['viewport_info'] = self.human.get_viewport_info()
            
            return info
            
        except Exception as e:
            print(f"Warning: Could not get browser info: {e}")
            return {
                'error': str(e),
                'linux_optimizations': self._linux_optimizations
            }