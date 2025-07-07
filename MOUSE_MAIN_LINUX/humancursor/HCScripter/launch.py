#!/usr/bin/env python3
"""
HumanCursor Scripter - Linux Edition Launcher
Launches the GUI for recording mouse movements and generating scripts
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir.parent.parent))

try:
    from humancursor.HCScripter.gui import HCSWindowLinux
except ImportError as e:
    print(f"Error importing GUI: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install pynput tkinter")
    sys.exit(1)


def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    # Check tkinter
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    # Check pynput (optional but recommended)
    try:
        import pynput
    except ImportError:
        print("Warning: pynput not available. Limited functionality.")
        print("Install with: pip install pynput")
    
    # Check if running on Linux
    if not sys.platform.startswith('linux'):
        print("Warning: This version is optimized for Linux systems.")
        print(f"Current platform: {sys.platform}")
    
    if missing_deps:
        print("Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nInstall missing dependencies and try again.")
        return False
        
    return True


def check_permissions():
    """Check if we have necessary permissions for input capture"""
    import getpass
    
    # Check if running as root (not recommended but sometimes necessary)
    if os.geteuid() == 0:
        print("Warning: Running as root. This is not recommended for security reasons.")
        print("Try running as a regular user and add your user to the 'input' group:")
        print("sudo usermod -a -G input $USER")
        print("Then log out and log back in.")
        
    # Check display environment
    if not os.environ.get('DISPLAY'):
        print("Warning: No DISPLAY environment variable set.")
        print("Make sure you're running in a graphical environment or set up X11 forwarding.")
        return False
        
    return True


def setup_linux_environment():
    """Setup Linux-specific environment settings"""
    try:
        # Try to set up input permissions
        user = os.environ.get('USER')
        if user:
            print(f"Running as user: {user}")
            
        # Check for virtual display if needed
        display = os.environ.get('DISPLAY')
        if display:
            print(f"Using display: {display}")
        else:
            print("No display detected. GUI may not work properly.")
            
        return True
        
    except Exception as e:
        print(f"Warning: Could not setup Linux environment: {e}")
        return True  # Continue anyway


def main():
    """Main launcher function"""
    print("=" * 50)
    print("HumanCursor Scripter - Linux Edition")
    print("=" * 50)
    print()
    
    # Check system compatibility
    if not check_dependencies():
        sys.exit(1)
        
    if not check_permissions():
        print("Continuing anyway, but some features may not work...")
        print()
        
    setup_linux_environment()
    
    print("Starting GUI...")
    print("Instructions:")
    print("1. Click 'Start Recording' to begin")
    print("2. Use keyboard shortcuts to record actions:")
    print("   - Press 'Z' to record mouse position")
    print("   - Press 'Ctrl' to record click")
    print("   - Hold 'Ctrl' longer to record drag & drop")
    print("3. Click 'Save Script' when finished")
    print()
    
    try:
        # Launch the GUI
        app = HCSWindowLinux()
        coordinates, file_name, file_destination = app()
        
        # Process results if the window was closed normally
        if coordinates and file_name and file_destination:
            print(f"\nRecording completed!")
            print(f"Actions recorded: {len(coordinates)}")
            print(f"Script saved as: {file_name}.py")
            print(f"Location: {file_destination}")
            
            # Generate and save the script
            script_content = generate_script_content(coordinates)
            script_path = os.path.join(file_destination, f"{file_name}.py")
            
            try:
                with open(script_path, 'w') as f:
                    f.write(script_content)
                print(f"Script successfully written to: {script_path}")
                
                # Make script executable
                os.chmod(script_path, 0o755)
                print("Script made executable")
                
            except Exception as e:
                print(f"Error saving script: {e}")
                
        else:
            print("Recording cancelled or no actions recorded.")
            
    except KeyboardInterrupt:
        print("\nLauncher interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"Error running GUI: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're running in a graphical environment")
        print("2. Install missing dependencies: pip install pynput tkinter")
        print("3. Add your user to input group: sudo usermod -a -G input $USER")
        print("4. Check X11 permissions if using SSH")
        sys.exit(1)


def generate_script_content(coordinates):
    """Generate the script content from coordinates"""
    imports = '''#!/usr/bin/env python3
# Generated by HumanCursor Scripter - Linux Edition
# Make sure humancursor-linux is installed: pip install humancursor-linux

import time
from humancursor import SystemCursor

'''

    main_function = '''def main():
    """Execute recorded mouse actions"""
    # Initialize SystemCursor for Linux
    cursor = SystemCursor()
    print('Starting recorded script...')
    
    # Wait a moment before starting
    time.sleep(2)
    
'''

    # Generate code for each recorded action
    actions_code = ""
    for i, coordinate in enumerate(coordinates):
        actions_code += f"    # Action {i + 1}\n"
        
        if isinstance(coordinate, tuple):
            # Simple click
            actions_code += f"    cursor.click_on({list(coordinate)}, clicks=1, click_duration=0, steady=False)\n"
        elif isinstance(coordinate, list):
            if len(coordinate) == 2 and all(isinstance(c, (int, tuple)) for c in coordinate):
                # Move action
                actions_code += f"    cursor.move_to({coordinate}, duration=None, steady=False)\n"
            elif len(coordinate) == 2:
                # Drag and drop
                actions_code += f"    cursor.drag_and_drop({coordinate[0]}, {coordinate[1]}, duration=None, steady=False)\n"
            else:
                # Click with position list
                actions_code += f"    cursor.click_on({coordinate}, clicks=1, click_duration=0, steady=False)\n"
        
        actions_code += "    time.sleep(0.3)  # Brief pause between actions\n\n"

    end_function = '''    print('Script completed successfully!')

if __name__ == '__main__':
    main()
'''

    return imports + main_function + actions_code + end_function


def show_help():
    """Show help information"""
    print("HumanCursor Scripter - Linux Edition")
    print("Usage: python -m humancursor.HCScripter.launch [options]")
    print()
    print("Options:")
    print("  --help, -h     Show this help message")
    print("  --version      Show version information")
    print("  --check-deps   Check dependencies only")
    print()
    print("Requirements:")
    print("  - Linux operating system")
    print("  - Python 3.7+")
    print("  - tkinter (usually included with Python)")
    print("  - pynput (install with: pip install pynput)")
    print("  - X11 display environment")
    print()
    print("Troubleshooting:")
    print("  - Add user to input group: sudo usermod -a -G input $USER")
    print("  - For headless: export DISPLAY=:0 or use xvfb")
    print("  - Check permissions: ls -la /dev/input/")


if __name__ == '__main__':
    # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--help', '-h']:
            show_help()
            sys.exit(0)
        elif arg == '--version':
            print("HumanCursor Scripter - Linux Edition v1.1.5")
            sys.exit(0)
        elif arg == '--check-deps':
            print("Checking dependencies...")
            if check_dependencies() and check_permissions():
                print("All checks passed!")
            else:
                print("Some issues found. See messages above.")
            sys.exit(0)
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information")
            sys.exit(1)
    
    # Run main launcher
    main()