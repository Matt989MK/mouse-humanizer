import random
import time
from typing import Union, List, Optional, Tuple

from selenium.common.exceptions import MoveTargetOutOfBoundsException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Firefox

from humancursor.utilities.human_curve_generator import HumanizeMouseTrajectory
from humancursor.utilities.calculate_and_randomize import generate_random_curve_parameters, calculate_absolute_offset


class WebAdjuster:
    """Linux-optimized web adjuster for human-like cursor movement"""
    
    def __init__(self, driver):
        """Initialize web adjuster
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.__driver = driver
        self.__action = ActionChains(
            self.__driver, 
            duration=0 if not isinstance(driver, Firefox) else 1
        )
        self.origin_coordinate = [0, 0]
        self._linux_optimizations = self._detect_linux_optimizations()
        
    def _detect_linux_optimizations(self) -> dict:
        """Detect Linux-specific optimizations to apply"""
        optimizations = {
            'use_native_events': False,
            'reduce_polling': True,
            'optimize_for_headless': False
        }
        
        try:
            # Check if running in headless mode
            if hasattr(self.__driver, 'execute_script'):
                result = self.__driver.execute_script("return navigator.webdriver")
                if result:
                    optimizations['optimize_for_headless'] = True
                    
            # Check for native events support
            if hasattr(self.__driver, 'capabilities'):
                caps = self.__driver.capabilities
                if caps.get('nativeEvents', False):
                    optimizations['use_native_events'] = True
                    
        except Exception:
            pass
            
        return optimizations

    def move_to(self,
                element_or_pos: Union[WebElement, List[int], Tuple[int, int]],
                origin_coordinates: Optional[List[int]] = None,
                absolute_offset: bool = False,
                relative_position: Optional[List[float]] = None,
                human_curve: Optional[HumanizeMouseTrajectory] = None,
                steady: bool = False) -> List[int]:
        """Move cursor to element or position with human-like movement
        
        Args:
            element_or_pos: Target element or coordinates
            origin_coordinates: Starting coordinates (uses current if None)
            absolute_offset: Whether coordinates are absolute offsets
            relative_position: Relative position within element [0-1, 0-1]
            human_curve: Pre-calculated curve (generated if None)
            steady: Use steady movement with less randomization
            
        Returns:
            Final cursor coordinates
        """
        origin = origin_coordinates if origin_coordinates else self.origin_coordinate
        pre_origin = tuple(origin)
        
        try:
            # Calculate target coordinates
            target_coords = self._calculate_target_coordinates(
                element_or_pos, (pre_origin[0], pre_origin[1]), absolute_offset, relative_position
            )
            
            if not target_coords:
                return list(pre_origin)
                
            x, y = target_coords
            
            # Generate or use provided human curve
            if not human_curve:
                human_curve = self._generate_human_curve(
                    origin, (x, y), steady
                )
            
            # Execute movement with Linux optimizations
            final_coords = self._execute_web_movement(
                human_curve, (pre_origin[0], pre_origin[1]), (x, y)
            )
            
            self.origin_coordinate = list(final_coords)
            return list(final_coords)
            
        except Exception as e:
            print(f"Warning: Web movement failed: {e}")
            return list(pre_origin)

    def _calculate_target_coordinates(self, 
                                    element_or_pos: Union[WebElement, List[int], Tuple[int, int]],
                                    origin: Tuple[int, int],
                                    absolute_offset: bool,
                                    relative_position: Optional[List[float]]) -> Optional[Tuple[int, int]]:
        """Calculate target coordinates based on input type"""
        try:
            if isinstance(element_or_pos, (list, tuple)):
                if not absolute_offset:
                    return (int(element_or_pos[0]), int(element_or_pos[1]))
                else:
                    return (
                        int(element_or_pos[0] + origin[0]),
                        int(element_or_pos[1] + origin[1])
                    )
            else:
                # WebElement
                return self._get_element_coordinates(element_or_pos, relative_position)
                
        except Exception as e:
            print(f"Warning: Could not calculate target coordinates: {e}")
            return None

    def _get_element_coordinates(self, 
                               element: WebElement,
                               relative_position: Optional[List[float]]) -> Tuple[int, int]:
        """Get coordinates for WebElement with Linux optimizations"""
        try:
            # Use JavaScript for more accurate positioning on Linux
            script = """
            var rect = arguments[0].getBoundingClientRect();
            return {
                x: Math.round(rect.left + window.scrollX),
                y: Math.round(rect.top + window.scrollY),
                width: Math.round(rect.width),
                height: Math.round(rect.height)
            };
            """
            
            result = self.__driver.execute_script(script, element)
            
            if relative_position is None:
                # Random position within element with Linux-optimized distribution
                x_random_off = random.choice(range(25, 75)) / 100  # More centered
                y_random_off = random.choice(range(25, 75)) / 100
                
                x = result["x"] + (result["width"] * x_random_off)
                y = result["y"] + (result["height"] * y_random_off)
            else:
                abs_exact_offset = calculate_absolute_offset(element, relative_position)
                x = result["x"] + abs_exact_offset[0]
                y = result["y"] + abs_exact_offset[1]
                
            return (int(x), int(y))
            
        except Exception as e:
            print(f"Warning: Could not get element coordinates: {e}")
            # Fallback to Selenium's location
            try:
                location = element.location
                size = element.size
                return (
                    int(location['x'] + size['width'] / 2),
                    int(location['y'] + size['height'] / 2)
                )
            except:
                return (0, 0)

    def _generate_human_curve(self, 
                            origin: List[int],
                            destination: Tuple[int, int],
                            steady: bool) -> HumanizeMouseTrajectory:
        """Generate human-like curve with Linux optimizations"""
        try:
            (
                offset_boundary_x,
                offset_boundary_y,
                knots_count,
                distortion_mean,
                distortion_st_dev,
                distortion_frequency,
                tween,
                target_points,
            ) = generate_random_curve_parameters(
                self.__driver, origin, destination
            )
            
            if steady:
                offset_boundary_x, offset_boundary_y = 10, 10
                distortion_mean, distortion_st_dev, distortion_frequency = 1.2, 1.2, 0.1
                
            # Linux-specific adjustments
            if self._linux_optimizations['optimize_for_headless']:
                # Reduce complexity for headless environments
                knots_count = min(knots_count, 3)
                target_points = min(target_points, 30)
                
            return HumanizeMouseTrajectory(
                origin,
                destination,
                offset_boundary_x=offset_boundary_x,
                offset_boundary_y=offset_boundary_y,
                knots_count=knots_count,
                distortion_mean=distortion_mean,
                distortion_st_dev=distortion_st_dev,
                distortion_frequency=distortion_frequency,
                tween=tween,
                target_points=target_points,
            )
            
        except Exception as e:
            print(f"Warning: Could not generate human curve: {e}")
            # Fallback to simple movement
            return HumanizeMouseTrajectory(origin, destination)

    def _execute_web_movement(self, 
                            human_curve: HumanizeMouseTrajectory,
                            origin: Tuple[int, int],
                            destination: Tuple[int, int]) -> Tuple[int, int]:
        """Execute web movement with Linux optimizations"""
        if not human_curve.points:
            return destination
            
        extra_numbers = [0.0, 0.0]
        total_offset = [0, 0]
        current_origin = list(origin)
        
        try:
            # Use batched movements for better performance on Linux
            batch_size = 3 if self._linux_optimizations['reduce_polling'] else 1
            movements = []
            
            for i, point in enumerate(human_curve.points):
                x_offset = point[0] - current_origin[0]
                y_offset = point[1] - current_origin[1]
                
                extra_numbers[0] += x_offset - int(x_offset)
                extra_numbers[1] += y_offset - int(y_offset)
                
                # Collect movements for batching
                if abs(extra_numbers[0]) > 1 or abs(extra_numbers[1]) > 1:
                    movements.append((int(extra_numbers[0]), int(extra_numbers[1])))
                    total_offset[0] += int(extra_numbers[0])
                    total_offset[1] += int(extra_numbers[1])
                    extra_numbers[0] = extra_numbers[0] - int(extra_numbers[0])
                    extra_numbers[1] = extra_numbers[1] - int(extra_numbers[1])
                elif abs(extra_numbers[0]) > 1:
                    movements.append((int(extra_numbers[0]), 0))
                    total_offset[0] += int(extra_numbers[0])
                    extra_numbers[0] = extra_numbers[0] - int(extra_numbers[0])
                elif abs(extra_numbers[1]) > 1:
                    movements.append((0, int(extra_numbers[1])))
                    total_offset[1] += int(extra_numbers[1])
                    extra_numbers[1] = extra_numbers[1] - int(extra_numbers[1])
                
                current_origin[0], current_origin[1] = point[0], point[1]
                total_offset[0] += int(x_offset)
                total_offset[1] += int(y_offset)
                movements.append((int(x_offset), int(y_offset)))
                
                # Execute batched movements
                if len(movements) >= batch_size or i == len(human_curve.points) - 1:
                    for move_x, move_y in movements:
                        if move_x != 0 or move_y != 0:
                            self.__action.move_by_offset(move_x, move_y)
                    movements.clear()
            
            # Handle remaining fractional movements
            if abs(extra_numbers[0]) > 0.5 or abs(extra_numbers[1]) > 0.5:
                final_x = int(extra_numbers[0] + 0.5)
                final_y = int(extra_numbers[1] + 0.5)
                total_offset[0] += final_x
                total_offset[1] += final_y
                self.__action.move_by_offset(final_x, final_y)
            
            # Execute all movements
            self.__action.perform()
            
            return (origin[0] + total_offset[0], origin[1] + total_offset[1])
            
        except MoveTargetOutOfBoundsException as e:
            print(f"Warning: Move target out of bounds: {e}")
            try:
                # Fallback to simple movement
                self.__action.move_to_element_with_offset(self.__driver.find_element("tag name", "body"), destination[0], destination[1])
                self.__action.perform()
                return destination
            except:
                return origin
                
        except WebDriverException as e:
            print(f"Warning: WebDriver exception during movement: {e}")
            return origin
            
        except Exception as e:
            print(f"Warning: Unexpected error during movement: {e}")
            return origin

    def scroll_smooth(self, 
                     element: WebElement,
                     direction: str = 'down',
                     amount: int = 3,
                     smooth: bool = True) -> bool:
        """Perform smooth scrolling with Linux optimizations
        
        Args:
            element: Element to scroll
            direction: 'up', 'down', 'left', 'right'
            amount: Number of scroll steps
            smooth: Whether to use smooth scrolling
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if smooth and self._linux_optimizations['use_native_events']:
                # Use JavaScript smooth scrolling for better Linux compatibility
                script = """
                arguments[0].scrollBy({
                    left: arguments[1],
                    top: arguments[2],
                    behavior: 'smooth'
                });
                """
                
                scroll_map = {
                    'up': (0, -100 * amount),
                    'down': (0, 100 * amount),
                    'left': (-100 * amount, 0),
                    'right': (100 * amount, 0)
                }
                
                left, top = scroll_map.get(direction.lower(), (0, 100 * amount))
                self.__driver.execute_script(script, element, left, top)
                
                if smooth:
                    time.sleep(0.5)  # Wait for smooth scroll to complete
                    
                return True
            else:
                # Fallback to action chains
                self.__action.move_to_element(element)
                for _ in range(amount):
                    if direction.lower() in ['up', 'down']:
                        delta_y = -1 if direction.lower() == 'up' else 1
                        self.__action.scroll_by_amount(0, delta_y * 100)
                    else:
                        delta_x = -1 if direction.lower() == 'left' else 1
                        self.__action.scroll_by_amount(delta_x * 100, 0)
                    
                    if smooth:
                        time.sleep(0.1)
                        
                self.__action.perform()
                return True
                
        except Exception as e:
            print(f"Warning: Smooth scroll failed: {e}")
            return False

    def get_viewport_info(self) -> dict:
        """Get viewport information with Linux optimizations"""
        try:
            script = """
            return {
                width: Math.max(document.documentElement.clientWidth, window.innerWidth || 0),
                height: Math.max(document.documentElement.clientHeight, window.innerHeight || 0),
                scrollX: window.pageXOffset || document.documentElement.scrollLeft,
                scrollY: window.pageYOffset || document.documentElement.scrollTop,
                devicePixelRatio: window.devicePixelRatio || 1
            };
            """
            
            return self.__driver.execute_script(script)
            
        except Exception as e:
            print(f"Warning: Could not get viewport info: {e}")
            return {
                'width': 1920,
                'height': 1080,
                'scrollX': 0,
                'scrollY': 0,
                'devicePixelRatio': 1
            }

    def reset_origin(self) -> None:
        """Reset origin coordinates to current cursor position"""
        try:
            # Try to get current cursor position via JavaScript
            script = """
            return {
                x: document.documentElement.scrollLeft || document.body.scrollLeft || 0,
                y: document.documentElement.scrollTop || document.body.scrollTop || 0
            };
            """
            
            result = self.__driver.execute_script(script)
            self.origin_coordinate = [result['x'], result['y']]
            
        except Exception:
            self.origin_coordinate = [0, 0]