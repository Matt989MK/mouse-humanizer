# 🎯 Keyboard Humanizer - Ultra-Realistic Human Typing Simulation

Transform your automated typing into indistinguishable human-like behavior with advanced error simulation, natural rhythms, and intelligent context adaptation.

## 🚀 Features

### 🎭 **Human-Like Behavior**
- **Natural typing rhythms** with variable speeds and pauses
- **Realistic error patterns** (substitutions, insertions, deletions, transpositions)
- **Intelligent corrections** with backspace simulation
- **Context-aware adaptation** for different text types
- **Fatigue simulation** that affects speed and accuracy over time

### 👥 **Multiple Typing Profiles**
- **Professional** - Fast, accurate, efficient (75 WPM)
- **Casual** - Moderate speed, occasional errors (45 WPM)
- **Beginner** - Slow, hunt-and-peck, frequent corrections (20 WPM)
- **Gaming** - Fast bursts, good with shortcuts (60 WPM)
- **Programmer** - Excellent with symbols, variable speed (65 WPM)
- **Elderly** - Slow, careful, prone to fatigue (25 WPM)
- **Mobile** - Touch typing simulation (35 WPM)

### 🧠 **Smart Features**
- **Copy-paste detection** for repeated/long content
- **Thinking pauses** at natural break points
- **Spontaneous corrections** going back to fix earlier errors
- **Learning mode** that adapts to your patterns
- **Context detection** (code, email, formal text)

### 🐧 **Linux Optimized**
- Full **pynput** integration for reliable keystroke simulation
- **Virtual display** support for headless environments
- **X11** compatibility for all Linux desktop environments
- **Minimal dependencies** and easy installation

## 📦 Installation

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3-pip python3-dev
sudo apt install python3-tk python3-dev
sudo apt install xvfb  # For headless operation

pip3 install pynput
```

### Fedora/RHEL
```bash
sudo dnf install python3-pip python3-devel
sudo dnf install python3-tkinter
sudo dnf install xorg-x11-server-Xvfb  # For headless operation

pip3 install pynput
```

### Arch Linux
```bash
sudo pacman -S python-pip python-tkinter
sudo pacman -S xorg-server-xvfb  # For headless operation

pip3 install pynput
```

## 🎮 Quick Start

### Basic Usage
```python
from keyboard_humanizer import KeyboardHumanizer

# Create humanizer with default profile
humanizer = KeyboardHumanizer()

# Type text with human-like behavior
humanizer.type_text("Hello, this is realistic human typing!")

# Check statistics
humanizer.print_stats()
```

### Using Different Profiles
```python
from keyboard_humanizer import KeyboardHumanizer

# Create with specific profile
humanizer = KeyboardHumanizer()
humanizer.set_profile_by_name("professional")

# Or use convenience function
from keyboard_humanizer import create_humanizer
humanizer = create_humanizer("programmer")

# Available profiles
print(humanizer.get_available_profiles())
# ['professional', 'casual', 'beginner', 'gaming', 'programmer', 'elderly', 'mobile']
```

### Advanced Configuration
```python
# Configure behavior
humanizer.configure(
    simulate_errors=True,
    use_copy_paste=True,
    add_thinking_pauses=True,
    simulate_fatigue=True,
    context_aware=True,
    learning_mode=True
)

# Type with custom settings
humanizer.type_text(
    "This text will be typed with custom behavior",
    speed_multiplier=1.5,  # 50% faster
    simulate_errors=False,  # No errors for this text
    use_copy_paste=False   # Force manual typing
)
```

## 🎯 Demo Examples

### 1. Basic Demonstration
```python
#!/usr/bin/env python3
from keyboard_humanizer import KeyboardHumanizer

def basic_demo():
    humanizer = KeyboardHumanizer()
    
    texts = [
        "Hello, welcome to the keyboard humanizer demo!",
        "This system simulates realistic human typing patterns.",
        "Notice the natural variations in speed and occasional corrections.",
        "The system even adds thinking pauses between sentences."
    ]
    
    for text in texts:
        print(f"Typing: {text}")
        humanizer.type_text(text)
        input("Press Enter to continue...")
    
    humanizer.print_stats()

if __name__ == "__main__":
    basic_demo()
```

### 2. Profile Comparison
```python
#!/usr/bin/env python3
from keyboard_humanizer import KeyboardHumanizer

def profile_comparison():
    test_text = "The quick brown fox jumps over the lazy dog."
    profiles = ["beginner", "casual", "professional", "gaming"]
    
    for profile_name in profiles:
        print(f"\n=== {profile_name.upper()} PROFILE ===")
        humanizer = KeyboardHumanizer()
        humanizer.set_profile_by_name(profile_name)
        
        print(f"Typing: {test_text}")
        humanizer.type_text(test_text)
        humanizer.print_stats()
        
        input("Press Enter for next profile...")

if __name__ == "__main__":
    profile_comparison()
```

### 3. Context-Aware Typing
```python
#!/usr/bin/env python3
from keyboard_humanizer import KeyboardHumanizer

def context_demo():
    humanizer = KeyboardHumanizer()
    humanizer.configure(context_aware=True)
    
    contexts = [
        ("Email", "Dear John, I hope this email finds you well. Best regards, user@example.com"),
        ("Code", "def hello_world(): print('Hello, World!') if __name__ == '__main__':"),
        ("Formal", "Furthermore, the analysis demonstrates that consequently, the methodology is sound."),
        ("Casual", "Hey there! How's it going? Just wanted to check in and see what's up!")
    ]
    
    for context_type, text in contexts:
        print(f"\n=== {context_type.upper()} CONTEXT ===")
        print(f"Typing: {text}")
        humanizer.type_text(text)
        input("Press Enter for next context...")
    
    humanizer.print_stats()

if __name__ == "__main__":
    context_demo()
```

## 🔧 Advanced Features

### Error Simulation
```python
# Configure error behavior
humanizer.configure(
    simulate_errors=True,
    auto_correct=True  # Automatically correct most errors
)

# The humanizer will:
# - Make realistic typing mistakes
# - Correct them with backspace
# - Occasionally leave some errors uncorrected
# - Adapt error rate based on fatigue
```

### Copy-Paste Simulation
```python
# Enable copy-paste for repeated/long content
humanizer.configure(use_copy_paste=True)

# Will automatically copy-paste:
# - Repeated words/phrases
# - Email addresses
# - URLs
# - Long technical terms
```

### Learning Mode
```python
# Enable learning from typing patterns
humanizer.configure(learning_mode=True)

# The system will:
# - Adapt speed based on accuracy
# - Learn from correction patterns
# - Adjust to your typing style over time
```

### Fatigue Simulation
```python
# Enable fatigue effects
humanizer.configure(simulate_fatigue=True)

# Over time, the system will:
# - Gradually slow down
# - Make more errors
# - Take longer pauses
# - Simulate realistic human fatigue
```

## 🎪 Interactive Demo Mode

Run the built-in demo to see all features in action:

```python
from keyboard_humanizer import KeyboardHumanizer

humanizer = KeyboardHumanizer()
humanizer.demo_mode(duration=120)  # 2-minute demo
```

## 📊 Statistics and Monitoring

```python
# Get detailed statistics
stats = humanizer.get_session_stats()
print(f"WPM: {stats.current_wpm:.1f}")
print(f"Accuracy: {stats.accuracy:.1f}%")
print(f"Characters typed: {stats.characters_typed}")
print(f"Errors made: {stats.errors_made}")
print(f"Corrections made: {stats.corrections_made}")

# Print formatted stats
humanizer.print_stats()

# Reset session
humanizer.reset_session()
```

## 🛠️ Customization

### Create Custom Profiles
```python
from keyboard_humanizer.profiles.typing_profiles import TypingCharacteristics, create_custom_profile

# Define custom characteristics
custom_char = TypingCharacteristics(
    base_wpm=50,
    wpm_variance=20,
    error_rate=0.03,
    correction_rate=0.85,
    thinking_pause_freq=0.12,
    burst_typing=True,
    copy_paste_likelihood=0.25,
    fatigue_sensitivity=1.0,
    accuracy_focus=False
)

# Create profile
custom_profile = create_custom_profile("my_style", custom_char)
humanizer.set_profile(custom_profile)
```

### Fine-tune Settings
```python
# Access engine directly for fine control
humanizer.engine.base_wpm = 60
humanizer.engine.error_rate = 0.015
humanizer.engine.correction_rate = 0.9
humanizer.engine.thinking_pauses = True
```

## 🐛 Troubleshooting

### Permission Issues
```bash
# Add user to input group
sudo usermod -a -G input $USER

# For X11 access
xhost +local:
```

### Virtual Display Setup
```python
# For headless environments
import os
os.environ['DISPLAY'] = ':99'

# Start Xvfb
# Xvfb :99 -screen 0 1024x768x24 &
```

### Dependencies
```bash
# Install all dependencies
pip3 install pynput python-xlib

# For development
pip3 install pynput python-xlib pytest black flake8
```

## 📈 Performance Tips

- **Reduce error rate** for faster typing: `humanizer.engine.error_rate = 0.005`
- **Disable thinking pauses** for continuous typing: `humanizer.configure(add_thinking_pauses=False)`
- **Use copy-paste mode** for repetitive content: `humanizer.configure(use_copy_paste=True)`
- **Adjust speed** with profile selection or multipliers

## 🤝 Integration Examples

### Web Automation
```python
from selenium import webdriver
from keyboard_humanizer import KeyboardHumanizer

driver = webdriver.Chrome()
humanizer = KeyboardHumanizer()

# Navigate to form
driver.get("https://example.com/form")
element = driver.find_element("id", "text-input")
element.click()

# Type with human-like behavior
humanizer.type_text("This was typed by a human!")
```

### GUI Automation
```python
import time
from keyboard_humanizer import KeyboardHumanizer

humanizer = KeyboardHumanizer()

# Wait for user to focus on desired application
print("Focus on target application, typing will start in 3 seconds...")
time.sleep(3)

# Type with human-like behavior
humanizer.type_text("Hello from keyboard humanizer!")
```

## 🎨 Visual Characteristics

The Keyboard Humanizer produces typing that exhibits:

- **Natural rhythm variations** - Speed fluctuates like real typing
- **Realistic error patterns** - Mistakes occur on difficult key combinations
- **Intelligent corrections** - Errors are noticed and fixed naturally
- **Context awareness** - Typing adapts to content type
- **Fatigue effects** - Performance degrades over time
- **Learning behavior** - Adapts to patterns over time

## 🔍 Technical Details

### Supported Error Types
- **Substitution** - Wrong character (adjacent keys)
- **Insertion** - Extra character added
- **Deletion** - Character missed
- **Transposition** - Character order swapped

### Timing Calculations
- Based on realistic WPM calculations
- Adjusted for character difficulty
- Modified by fatigue levels
- Influenced by key combinations

### Context Detection
- Code patterns (keywords, syntax)
- Email indicators (addresses, signatures)
- Formal writing markers
- Repetitive content analysis

## 📋 API Reference

### KeyboardHumanizer Class
- `type_text(text, **kwargs)` - Type text with human behavior
- `set_profile_by_name(name)` - Change typing profile
- `configure(**kwargs)` - Configure behavior settings
- `get_session_stats()` - Get typing statistics
- `reset_session()` - Reset session data
- `demo_mode(duration)` - Run interactive demo

### Available Profiles
- `professional`, `casual`, `beginner`, `gaming`, `programmer`, `elderly`, `mobile`

### Configuration Options
- `simulate_errors`, `use_copy_paste`, `add_thinking_pauses`, `simulate_fatigue`, `context_aware`, `learning_mode`

---

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built for Linux automation with focus on realistic human simulation. Perfect for testing, demonstrations, and automation that needs to pass human detection systems.

---

**⚡ Ready to type like a human? Get started with the examples above!**