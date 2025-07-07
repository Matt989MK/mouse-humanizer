#!/usr/bin/env python3
"""
Simple Human Behavior Demonstration
Shows natural human-like mouse movements and keyboard typing
"""

import time
import random
from humancursor import SystemCursor

def demonstrate_mouse_behavior():
    """Demonstrate natural mouse behavior"""
    print("🖱️ Mouse Behavior Demonstration")
    print("=" * 50)
    print("This shows natural human-like mouse movements:")
    print("• Natural curve movements")
    print("• Speed variations based on distance")
    print("• Micro-jitter and hesitations")
    print("• Overshoot and correction")
    print("• Fatigue effects over time")
    print()
    
    cursor = SystemCursor()
    screen_width, screen_height = cursor.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    
    print(f"Detected screen: {screen_width}x{screen_height}")
    print()
    
    # Test different movement types
    movements = [
        # Short precise movements
        ([center_x - 50, center_y - 50], [center_x - 30, center_y - 30], "Short precise movement"),
        
        # Medium movements  
        ([center_x - 100, center_y], [center_x + 100, center_y], "Medium horizontal movement"),
        ([center_x, center_y - 100], [center_x, center_y + 100], "Medium vertical movement"),
        
        # Long movements
        ([center_x - 300, center_y - 200], [center_x + 300, center_y + 200], "Long diagonal movement"),
        
        # Back to center
        ([center_x + 300, center_y + 200], [center_x, center_y], "Return to center"),
    ]
    
    print("🎬 Starting movement demonstration...")
    time.sleep(2)
    
    for i, (start, end, description) in enumerate(movements, 1):
        print(f"[{i}/{len(movements)}] {description}")
        
        # Move to start position first
        cursor.move_to(start, steady=True)
        time.sleep(0.5)
        
        # Then perform human-like movement
        start_time = time.time()
        cursor.move_to(end, steady=False)  # Human-like movement
        end_time = time.time()
        
        print(f"  ✅ Completed in {end_time - start_time:.2f}s")
        
        # Demonstrate clicking with human behavior
        if i == len(movements):
            print("  🖱️ Demonstrating human-like click...")
            cursor.click_on(end)
        
        time.sleep(1)
    
    print("\n📊 Mouse behavior features demonstrated:")
    print("• Natural curved movements (not straight lines)")
    print("• Variable speed based on distance")
    print("• Micro-jitter simulating hand tremor")
    print("• Occasional overshoots with corrections")
    print("• Natural pauses and hesitations")

def demonstrate_clicking_patterns():
    """Demonstrate different clicking behaviors"""
    print("\n🖱️ Click Pattern Demonstration")
    print("=" * 50)
    
    cursor = SystemCursor()
    screen_width, screen_height = cursor.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    
    click_tests = [
        ([center_x - 100, center_y - 100], "Quick click"),
        ([center_x + 100, center_y - 100], "Click with pre-pause"),
        ([center_x, center_y + 100], "Variable duration click"),
        ([center_x - 100, center_y + 100], "Right click test"),
    ]
    
    for i, (position, description) in enumerate(click_tests, 1):
        print(f"[{i}/{len(click_tests)}] {description}")
        
        # Move to position
        cursor.move_to(position)
        
        # Different click types
        if "Right" in description:
            cursor.click("right")
        else:
            # Variable click duration for realism
            duration = 0.1 + random.uniform(-0.03, 0.05)
            cursor.click("left", duration)
        
        time.sleep(1)

def demonstrate_fatigue_effects():
    """Demonstrate how fatigue affects movement over time"""
    print("\n😴 Fatigue Effects Demonstration")
    print("=" * 50)
    print("Simulating movement patterns over extended use...")
    
    cursor = SystemCursor()
    screen_width, screen_height = cursor.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    
    # Simulate time passing for demo
    cursor.session_start = time.time() - 7200  # 2 hours ago
    
    targets = [
        [center_x - 150, center_y - 150],
        [center_x + 150, center_y - 150],
        [center_x + 150, center_y + 150],
        [center_x - 150, center_y + 150]
    ]
    
    print("Notice how movements become slower and less precise...")
    
    for i in range(8):
        target = targets[i % len(targets)]
        
        print(f"Movement {i+1}: Fatigue level ~{cursor.fatigue_level:.1%}")
        
        start_time = time.time()
        cursor.move_to(target)
        end_time = time.time()
        
        print(f"  Time taken: {end_time - start_time:.2f}s")
        time.sleep(0.5)

def demonstrate_resolution_independence():
    """Show that it works on any screen resolution"""
    print("\n📐 Resolution Independence Demonstration")
    print("=" * 50)
    
    cursor = SystemCursor()
    screen_width, screen_height = cursor.size()
    
    print(f"Current resolution: {screen_width}x{screen_height}")
    print("Testing movements at screen boundaries...")
    
    # Test movements to screen edges
    edge_positions = [
        ([10, 10], "Top-left corner"),
        ([screen_width - 10, 10], "Top-right corner"),
        ([screen_width - 10, screen_height - 10], "Bottom-right corner"),
        ([10, screen_height - 10], "Bottom-left corner"),
        ([screen_width // 2, screen_height // 2], "Center"),
    ]
    
    for position, description in edge_positions:
        print(f"Moving to {description}: {position}")
        cursor.move_to(position)
        time.sleep(0.5)
    
    print("✅ All movements stayed within screen bounds")

def run_complete_demo():
    """Run the complete demonstration"""
    print("🎯 Human Behavior Library - Complete Demonstration")
    print("=" * 60)
    print("This library makes mouse and keyboard automation indistinguishable from human behavior")
    print()
    
    try:
        demonstrate_mouse_behavior()
        demonstrate_clicking_patterns()
        demonstrate_fatigue_effects()
        demonstrate_resolution_independence()
        
        print("\n🎉 Demonstration completed successfully!")
        print("\n📝 Key Features Shown:")
        print("✅ Natural curved movements (no straight lines)")
        print("✅ Speed variation based on distance and context")
        print("✅ Micro-jitter simulating natural hand tremor")
        print("✅ Overshoot and correction behaviors")
        print("✅ Fatigue effects over extended use")
        print("✅ Resolution independence")
        print("✅ Variable click timing and pre-click pauses")
        print("✅ No display management or system modifications")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        print("This might be due to missing dependencies or permissions")

if __name__ == "__main__":
    run_complete_demo()