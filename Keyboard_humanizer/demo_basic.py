#!/usr/bin/env python3
"""
Simple Keyboard Humanizer Demonstration
Shows natural human-like typing with errors, corrections, and realistic pacing
"""

import time
import sys
import os

# Add the parent directory to sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from keyboard_humanizer import KeyboardHumanizer, create_humanizer
except ImportError:
    print("Warning: Could not import keyboard_humanizer. Running in simulation mode.")
    KeyboardHumanizer = None

def basic_demo():
    """Demonstrate basic human typing behavior"""
    print("⌨️ Keyboard Humanizer - Basic Demo")
    print("=" * 50)
    print("This demo shows natural human typing patterns including:")
    print("• Natural speed variations and rhythm")
    print("• Realistic typing errors and corrections")
    print("• Thinking pauses between sentences")
    print("• Context-aware behavior adaptation")
    print("• Copy-paste intelligence")
    print()
    
    if not KeyboardHumanizer:
        print("❌ KeyboardHumanizer not available - check imports")
        return
    
    # Create humanizer with natural behavior
    humanizer = create_humanizer()
    
    # Demo texts to type
    demo_texts = [
        "Hello, welcome to the keyboard humanizer demonstration!",
        "This system simulates natural human typing patterns.",
        "Notice how the speed varies naturally, just like real typing.",
        "Sometimes there are small mistakes that get corrected automatically.",
        "The system even adds thinking pauses between sentences.",
        "Email addresses like user@example.com are often copy-pasted.",
        "Programming code like 'def hello_world():' is typed more carefully.",
        "This creates a very convincing human typing simulation!"
    ]
    
    print("🚀 Starting typing demonstration...")
    print("(Focus on any text editor to see the actual typing)")
    print()
    
    # Give user time to focus on target application
    for i in range(5, 0, -1):
        print(f"Starting in {i} seconds...")
        time.sleep(1)
    
    print("\n🎬 Demo in progress...")
    print("Watch for:")
    print("• Speed variations")
    print("• Occasional errors and corrections")
    print("• Natural pauses")
    print("• Context-aware behavior")
    print()
    
    # Type each demo text
    for i, text in enumerate(demo_texts, 1):
        print(f"[{i}/{len(demo_texts)}] Typing: {text}")
        
        # Type the text with human-like behavior
        start_time = time.time()
        success = humanizer.type_text(text)
        end_time = time.time()
        
        if success:
            print(f"✅ Completed in {end_time - start_time:.1f}s")
        else:
            print("❌ Error occurred")
        
        # Add natural break between sentences
        if i < len(demo_texts):
            break_time = 1.5 + (i * 0.2)  # Increasing breaks
            print(f"💭 Natural pause ({break_time:.1f}s)...")
            time.sleep(break_time)
        
        print()
    
    # Show final statistics
    print("\n📊 Final Session Statistics:")
    print("=" * 40)
    humanizer.print_stats()
    
    print("\n🎉 Demo completed!")
    print("The keyboard humanizer successfully simulated natural human typing.")

def feature_demo():
    """Demonstrate specific features"""
    print("🔧 Feature Demonstration")
    print("=" * 50)
    
    if not KeyboardHumanizer:
        print("❌ KeyboardHumanizer not available")
        return
    
    humanizer = create_humanizer()
    
    features = [
        ("Error Simulation", "This text will havw errors that get corected."),
        ("Code Context", "def hello_world(): print('Hello, World!')"),
        ("Email Context", "Contact me at user@example.com for more information."),
        ("Copy-Paste Test", "user@example.com and http://www.example.com are copy-pasted."),
        ("Speed Variation", "Short. Medium length sentence here. This is a much longer sentence to demonstrate speed variations."),
    ]
    
    print("Testing specific humanization features...")
    time.sleep(2)
    
    for i, (feature_name, test_text) in enumerate(features, 1):
        print(f"\n[{i}/{len(features)}] Testing: {feature_name}")
        print(f"Text: {test_text}")
        
        start_time = time.time()
        humanizer.type_text(test_text)
        end_time = time.time()
        
        print(f"✅ Typed in {end_time - start_time:.1f}s")
        time.sleep(1)
    
    humanizer.print_stats()

def configuration_demo():
    """Demonstrate configuration options"""
    print("⚙️ Configuration Demonstration")
    print("=" * 50)
    
    if not KeyboardHumanizer:
        print("❌ KeyboardHumanizer not available")
        return
    
    humanizer = create_humanizer()
    
    # Show current configuration
    print("Current configuration:")
    config = humanizer.get_current_config()
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # Test different configurations
    configurations = [
        {"name": "No Errors", "settings": {"simulate_errors": False}},
        {"name": "No Copy-Paste", "settings": {"use_copy_paste": False}},
        {"name": "Fast Typing", "settings": {"speed_multiplier": 1.5}},
        {"name": "Slow Typing", "settings": {"speed_multiplier": 0.5}},
    ]
    
    test_text = "This is a test of different typing configurations."
    
    print("\nTesting different configurations...")
    time.sleep(2)
    
    for i, config_test in enumerate(configurations, 1):
        print(f"\n[{i}/{len(configurations)}] {config_test['name']}")
        
        start_time = time.time()
        humanizer.type_text(test_text, **config_test["settings"])
        end_time = time.time()
        
        print(f"✅ Typed in {end_time - start_time:.1f}s")
        time.sleep(1)

def interactive_demo():
    """Interactive demo where user can test typing"""
    print("🎮 Interactive Demo")
    print("=" * 50)
    
    if not KeyboardHumanizer:
        print("❌ KeyboardHumanizer not available")
        return
    
    humanizer = create_humanizer()
    
    while True:
        print("\nChoose an option:")
        print("1. Type custom text")
        print("2. Show statistics")
        print("3. Reset session")
        print("4. Configure settings")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            text = input("Enter text to type: ")
            if text:
                print(f"Typing: {text}")
                print("Focus on target application...")
                time.sleep(3)
                
                start_time = time.time()
                humanizer.type_text(text)
                end_time = time.time()
                
                print(f"✅ Completed in {end_time - start_time:.1f}s")
        
        elif choice == '2':
            humanizer.print_stats()
        
        elif choice == '3':
            humanizer.reset_session()
            print("✅ Session reset")
        
        elif choice == '4':
            print("\nCurrent configuration:")
            config = humanizer.get_current_config()
            for key, value in config.items():
                print(f"  {key}: {value}")
            
            setting = input("\nEnter setting name to toggle (or 'back'): ").strip()
            if setting == 'back':
                continue
            elif setting in config and isinstance(config[setting], bool):
                new_value = not config[setting]
                humanizer.configure(**{setting: new_value})
                print(f"✅ {setting} set to {new_value}")
            else:
                print("❌ Invalid setting or setting type")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")

def main():
    """Main function to run the demonstration"""
    print("⌨️ Keyboard Humanizer Demonstration")
    print("=" * 50)
    print("Choose demonstration mode:")
    print("1. Basic Demo (automated)")
    print("2. Feature Demo (specific features)")
    print("3. Configuration Demo (settings)")
    print("4. Interactive Demo")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1':
        basic_demo()
    elif choice == '2':
        feature_demo()
    elif choice == '3':
        configuration_demo()
    elif choice == '4':
        interactive_demo()
    elif choice == '5':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("This might be due to missing dependencies or permissions.")
        print("Check that pynput is installed: pip install pynput")