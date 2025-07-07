# HumanCursor-Linux: A Python package for simulating human mouse movements on Linux

<div style="display:flex;flex-direction:row;">
  <img src="https://user-images.githubusercontent.com/108073687/234356166-719efddc-4618-4d32-b40e-2055d17b3edd.jpg" width="40%" height="300">
  <img src="https://media.giphy.com/media/D2D9BfjscHEG1DzBKu/giphy.gif" width="45%" height="300">
</div>

_**HumanCursor-Linux**_ is a Python package that allows you to _**simulate realistic human mouse movements**_ on Linux systems. It can be used for _**automating scripts**_ that require mouse interactions, such as _**web scraping**_, _**automated tasks**_, _**testing**_, or _**gaming**_. This version is specifically optimized for Linux environments and is compatible with xvfb (virtual framebuffer) for headless operation.

# Content:

- [Features](#features)
- [Requirements](#requirements)
- [How to install](#installation)
- [How to use](#usage)
  - [HCScripter](#hcscripter)
  - [WebCursor](#webcursor)
  - [SystemCursor](#systemcursor)
- [Linux-Specific Features](#linux-specific-features)
- [Virtual Display Support](#virtual-display-support)
- [Demonstration](#demonstration)

# Features

- HumanCursor-Linux uses a `natural motion algorithm` that mimics the way `humans` move the mouse cursor, with `variable speed`, `acceleration`, and `curvature`.
- Can perform various mouse actions, such as `clicking`, `dragging`, `scrolling`, and `hovering`.
- Designed specifically to `bypass security measures and bot detection software`.
- **Linux-optimized** with native X11 support and compatibility with virtual displays.
- **Xvfb compatible** for headless automation scenarios.
- Includes:
    - 🚀 `HCScripter` app to create physical cursor automated scripts without coding.
    - 🌐 `WebCursor` module for web cursor code automation.
        - Fully supported for `Chrome` and `Edge`, optimized for Linux browsers.
    - 🤖 `SystemCursor` module for physical cursor code automation using pynput and X11.
    

# Requirements

- ```Linux (Ubuntu 18.04+, Debian 9+, CentOS 7+, or similar)```
- ```Python >= 3.7```
  - [Download the installer](https://www.python.org/downloads/), or install via package manager.
- ```X11 development libraries```
  - Ubuntu/Debian: `sudo apt-get install libx11-dev libxtst-dev libxext-dev`
  - CentOS/RHEL: `sudo yum install libX11-devel libXtst-devel libXext-devel`
- ```For virtual display support```
  - Ubuntu/Debian: `sudo apt-get install xvfb`
  - CentOS/RHEL: `sudo yum install xorg-x11-server-Xvfb`

# Installation

To install, you can use pip:

    pip install --upgrade humancursor-linux

Or install from source:

    git clone https://github.com/riflosnake/HumanCursor.git
    cd HumanCursor
    pip install -e .

# Usage

## HCScripter

To quickly create an automated system script, you can use `HCScripter`, which registers mouse actions from point to point using key commands and creates a script file for you.

After installing `humancursor-linux` package, open up `terminal` and run:

```bash
python -m humancursor.HCScripter.launch
```

#### Linux-specific key bindings:
- Press `z` → `Move`
- Press `Ctrl` → `Click`
- Press and hold `Ctrl` → `Drag and drop`

## WebCursor

To use HumanCursor for Web on Linux, you need to import the `WebCursor` class, and create an instance:

```python
from humancursor import WebCursor

cursor = WebCursor(driver)
```

## SystemCursor

To use HumanCursor for your Linux system mouse, you need to import the `SystemCursor` class:

```python
from humancursor import SystemCursor

cursor = SystemCursor()
```

The `SystemCursor` class uses `pynput` and X11 libraries for native Linux mouse control, providing better performance and compatibility than pyautogui.

# Linux-Specific Features

## Native X11 Support
- Direct X11 calls for improved performance
- Better compatibility with Linux desktop environments (GNOME, KDE, XFCE)
- Support for multi-monitor setups

## Virtual Display Compatibility
- Full xvfb support for headless operations
- Automatic display detection and configuration
- Seamless integration with CI/CD pipelines

## Enhanced Security
- Respects Linux security policies
- Compatible with SELinux and AppArmor
- Proper handling of user permissions

# Virtual Display Support

For headless automation, you can use xvfb:

```bash
# Start virtual display
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &

# Run your script
python your_script.py

# Or use the built-in virtual display manager
python -c "
from humancursor.utilities.virtual_display import VirtualDisplay
with VirtualDisplay():
    # Your automation code here
    pass
"
```

# DEMONSTRATION:

#### SystemCursor (Linux)
```bash
python -m humancursor.test.system
```

#### WebCursor (Linux)
```bash
python -m humancursor.test.web
```

#### Code examples:

```python
# Linux-specific features
cursor.move_to([450, 600])  # Native X11 mouse movement
cursor.click_on([170, 390], button='left')  # Specify mouse button
cursor.scroll([500, 400], direction='down', clicks=3)  # Native scroll support

# Virtual display example
from humancursor.utilities.virtual_display import VirtualDisplay
with VirtualDisplay(width=1920, height=1080):
    cursor.move_to([960, 540])  # Center of virtual screen
    cursor.click_on([960, 540])
```

# Troubleshooting

## Permission Issues
If you encounter permission errors, you may need to add your user to the input group:
```bash
sudo usermod -a -G input $USER
```

## Display Issues
For SSH sessions without X11 forwarding:
```bash
export DISPLAY=:0
# Or use virtual display as shown above
```

## Dependencies
Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-tk python3-dev libx11-dev libxtst-dev

# CentOS/RHEL
sudo yum install tkinter python3-devel libX11-devel libXtst-devel
```

# License

HumanCursor-Linux is licensed under the MIT License. See LICENSE for more information.