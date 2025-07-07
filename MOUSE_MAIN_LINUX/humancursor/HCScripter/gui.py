import os
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from time import time
from typing import List, Tuple, Optional
import threading
import subprocess

try:
    from pynput import mouse, keyboard
    from pynput.mouse import Button
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("Warning: pynput not available. GUI functionality limited.")


class HCSWindowLinux:
    """Linux-compatible HCS GUI window with enhanced functionality"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HCS - Linux Edition")
        self.coordinates = []
        
        # Linux-compatible styling
        self.bg = '#2e3440'  # Nord theme dark background
        self.fg = '#d8dee9'  # Nord theme light foreground
        self.accent = '#5e81ac'  # Nord theme blue accent
        
        self.root.geometry("380x420")
        self.root.config(bg=self.bg)
        self.root.resizable(False, False)
        
        # Try to set window to stay on top (Linux-compatible)
        try:
            self.root.wm_attributes('-topmost', True)
        except tk.TclError:
            # Fallback for some Linux window managers
            pass
        
        self._setup_styles()
        self._setup_widgets()
        self._setup_listeners()
        
        self.file = None
        self.dest = None
        
        self.ctrl_pressed = False
        self.press_time = 0.0
        self.index = -1
        self.recording = False
        
        self.hold_time_threshold = 0.5
        
        # Mouse and keyboard listeners
        self.mouse_listener = None
        self.keyboard_listener = None
        
        self.update_coordinates()
        
    def _setup_styles(self):
        """Setup Linux-compatible styles"""
        self.style = ttk.Style()
        
        # Configure styles for Linux
        try:
            available_themes = self.style.theme_names()
            if 'clam' in available_themes:
                self.style.theme_use('clam')
            elif 'alt' in available_themes:
                self.style.theme_use('alt')
                
            # Configure colors
            self.style.configure('TLabel', 
                               background=self.bg, 
                               foreground=self.fg,
                               font=('Ubuntu', 11))
            self.style.configure('TButton',
                               font=('Ubuntu', 10))
            self.style.configure('TEntry',
                               fieldbackground='#3b4252',
                               foreground=self.fg)
                               
        except Exception as e:
            print(f"Warning: Could not set theme: {e}")
    
    def _setup_widgets(self):
        """Setup GUI widgets with Linux optimizations"""
        # Title and instructions
        title_frame = tk.Frame(self.root, bg=self.bg)
        title_frame.pack(pady=10)
        
        title_label = ttk.Label(title_frame, 
                               text="HumanCursor Scripter - Linux", 
                               font=('Ubuntu', 14, 'bold'))
        title_label.pack()
        
        instructions = ttk.Label(title_frame,
                                text="Record mouse movements with:\nZ = Move | Ctrl = Click | Ctrl+Hold = Drag",
                                font=('Ubuntu', 9),
                                justify=tk.CENTER)
        instructions.pack(pady=5)
        
        # Current position display
        pos_frame = tk.Frame(self.root, bg=self.bg)
        pos_frame.pack(pady=5)
        
        self.pos_label = ttk.Label(pos_frame, text="Mouse Position")
        self.pos_label.pack()
        
        self.coordinates_label = ttk.Label(pos_frame, text="x: 0, y: 0")
        self.coordinates_label.pack()
        
        # Recording status
        status_frame = tk.Frame(self.root, bg=self.bg)
        status_frame.pack(pady=5)
        
        self.status_label = ttk.Label(status_frame, 
                                     text="Recording: OFF", 
                                     font=('Ubuntu', 10, 'bold'))
        self.status_label.pack()
        
        # Actions recorded counter
        self.actions_label = ttk.Label(status_frame, text="Actions recorded: 0")
        self.actions_label.pack()
        
        # File configuration
        file_frame = tk.Frame(self.root, bg=self.bg)
        file_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(file_frame, text="Script Name:").pack(anchor=tk.W)
        self.file_name = ttk.Entry(file_frame, width=30)
        self.file_name.pack(fill=tk.X, pady=2)
        self.file_name.insert(0, f"recorded_script_{random.randint(1000, 9999)}")
        
        ttk.Label(file_frame, text="Save Directory:").pack(anchor=tk.W, pady=(10, 0))
        
        dir_frame = tk.Frame(file_frame, bg=self.bg)
        dir_frame.pack(fill=tk.X)
        
        self.entry_var = tk.StringVar()
        self.destination = ttk.Entry(dir_frame, textvariable=self.entry_var, width=25)
        self.destination.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Set default directory
        default_dir = os.path.expanduser("~/Desktop")
        if not os.path.exists(default_dir):
            default_dir = os.path.expanduser("~")
        self.entry_var.set(default_dir)
        
        self.browse_button = ttk.Button(dir_frame, text="Browse", 
                                       command=self.browse_directory, width=8)
        self.browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg=self.bg)
        button_frame.pack(pady=15)
        
        self.toggle_button = ttk.Button(button_frame, text="Start Recording", 
                                       command=self.toggle_recording, width=15)
        self.toggle_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear", 
                                      command=self.clear_recording, width=10)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.finish_button = ttk.Button(button_frame, text="Save Script", 
                                       command=self.finish_recording, width=12)
        self.finish_button.pack(side=tk.LEFT, padx=5)
        
        # Status indicator
        indicator_frame = tk.Frame(self.root, bg=self.bg)
        indicator_frame.pack(pady=10)
        
        self.indicator = tk.Canvas(indicator_frame, width=60, height=40, 
                                  background=self.bg, highlightthickness=0)
        self.indicator.pack()
        
        self.indicator_color = "#bf616a"  # Nord red for inactive
        self.draw_indicator()
        
        # Linux-specific information
        info_frame = tk.Frame(self.root, bg=self.bg)
        info_frame.pack(pady=5)
        
        if PYNPUT_AVAILABLE:
            info_text = "✓ Linux input capture ready"
            info_color = "#a3be8c"  # Nord green
        else:
            info_text = "⚠ Limited functionality (install pynput)"
            info_color = "#ebcb8b"  # Nord yellow
            
        info_label = tk.Label(info_frame, text=info_text, 
                             bg=self.bg, fg=info_color, font=('Ubuntu', 9))
        info_label.pack()
        
        # Bind events
        self.root.bind("<Button-1>", self.remove_focus)
        
    def _setup_listeners(self):
        """Setup input listeners for Linux"""
        if not PYNPUT_AVAILABLE:
            return
            
        # These will be started/stopped with recording
        self.mouse_listener = None
        self.keyboard_listener = None
    
    def __call__(self):
        """Returns recorded data when called as function"""
        self.root.mainloop()
        return self.coordinates, self.file, self.dest
    
    def get_current_position(self) -> Tuple[int, int]:
        """Get current mouse position using Linux-compatible method"""
        try:
            if PYNPUT_AVAILABLE:
                controller = mouse.Controller()
                pos = controller.position
                return (int(pos[0]), int(pos[1]))
            else:
                # Fallback: try using xdotool if available
                try:
                    result = subprocess.run(['xdotool', 'getmouselocation'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        # Parse output like "x:123 y:456 screen:0 window:789"
                        parts = result.stdout.strip().split()
                        x = int(parts[0].split(':')[1])
                        y = int(parts[1].split(':')[1])
                        return (x, y)
                except (subprocess.SubprocessError, IndexError, ValueError):
                    pass
                    
                # Final fallback
                return (0, 0)
                
        except Exception:
            return (0, 0)
    
    def browse_directory(self):
        """Open directory browser with Linux compatibility"""
        try:
            folder_selected = filedialog.askdirectory(
                title="Select directory to save script",
                initialdir=self.entry_var.get()
            )
            if folder_selected:
                self.entry_var.set(folder_selected)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open directory browser: {e}")
    
    def draw_indicator(self):
        """Draw recording status indicator"""
        self.indicator.delete("all")
        # Draw circular indicator
        self.indicator.create_oval(15, 10, 45, 40, fill=self.indicator_color, outline="")
        
        # Add status text
        if self.recording:
            self.indicator.create_text(30, 25, text="REC", fill="white", font=('Ubuntu', 8, 'bold'))
    
    def remove_focus(self, event):
        """Remove focus from entry widgets when clicking window"""
        if event.widget not in [self.file_name, self.destination]:
            self.root.focus_force()
    
    def toggle_recording(self):
        """Toggle recording state"""
        if not PYNPUT_AVAILABLE:
            messagebox.showwarning("Warning", 
                                 "Input capture not available. Please install pynput:\n"
                                 "pip install pynput")
            return
            
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording mouse and keyboard input"""
        try:
            self.recording = True
            self.indicator_color = "#a3be8c"  # Nord green for active
            self.draw_indicator()
            
            self.status_label.config(text="Recording: ON")
            self.toggle_button.config(text="Stop Recording")
            
            # Start listeners
            self.mouse_listener = mouse.Listener(
                on_click=self.on_mouse_click,
                suppress=False
            )
            
            self.keyboard_listener = keyboard.Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release,
                suppress=False
            )
            
            self.mouse_listener.start()
            self.keyboard_listener.start()
            
            print("Recording started - Use Z for move, Ctrl for click/drag")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not start recording: {e}")
            self.recording = False
    
    def stop_recording(self):
        """Stop recording input"""
        try:
            self.recording = False
            self.indicator_color = "#bf616a"  # Nord red for inactive
            self.draw_indicator()
            
            self.status_label.config(text="Recording: OFF")
            self.toggle_button.config(text="Start Recording")
            
            # Stop listeners
            if self.mouse_listener:
                self.mouse_listener.stop()
                self.mouse_listener = None
                
            if self.keyboard_listener:
                self.keyboard_listener.stop()
                self.keyboard_listener = None
                
            print("Recording stopped")
            
        except Exception as e:
            print(f"Error stopping recording: {e}")
    
    def on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events (not used for recording, just for reference)"""
        # We don't record raw mouse clicks, only keyboard-triggered actions
        pass
    
    def on_key_press(self, key):
        """Handle key press events"""
        if not self.recording:
            return
            
        try:
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                if not self.ctrl_pressed:
                    self.ctrl_pressed = True
                    self.press_time = time()
                    pos = self.get_current_position()
                    self.coordinates.append([pos])
                    self.index += 1
                    self.update_actions_count()
                    print(f"Click start recorded at {pos}")
                    
            elif hasattr(key, 'char') and key.char == 'z':
                pos = self.get_current_position()
                self.coordinates.append(list(pos))
                self.index += 1
                self.update_actions_count()
                print(f"Move recorded to {pos}")
                
        except Exception as e:
            print(f"Error handling key press: {e}")
    
    def on_key_release(self, key):
        """Handle key release events"""
        if not self.recording:
            return
            
        try:
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                if self.ctrl_pressed:
                    self.ctrl_pressed = False
                    pos = self.get_current_position()
                    
                    # Determine if it was a click or drag based on hold time
                    if time() - self.press_time > self.hold_time_threshold:
                        # Drag - add end position
                        self.coordinates[self.index].append(pos)
                        print(f"Drag end recorded at {pos}")
                    else:
                        # Click - replace with single position
                        self.coordinates[self.index] = list(self.coordinates[self.index][0])
                        print(f"Click recorded at {self.coordinates[self.index]}")
                        
                    self.press_time = 0.0
                    
        except Exception as e:
            print(f"Error handling key release: {e}")
    
    def clear_recording(self):
        """Clear all recorded actions"""
        if messagebox.askyesno("Clear Recording", "Are you sure you want to clear all recorded actions?"):
            self.coordinates.clear()
            self.index = -1
            self.update_actions_count()
            print("Recording cleared")
    
    def update_actions_count(self):
        """Update the actions counter"""
        self.actions_label.config(text=f"Actions recorded: {len(self.coordinates)}")
    
    def finish_recording(self):
        """Finish recording and save script"""
        if self.recording:
            self.stop_recording()
            
        # Validate inputs
        self.file = self.file_name.get().strip()
        self.dest = self.destination.get().strip()
        
        if not self.file:
            self.file = f'humancursor_linux_{random.randint(1, 10000)}'
            
        if not self.dest or not os.path.exists(self.dest):
            messagebox.showerror("Error", "Please select a valid destination directory")
            return
            
        if not self.coordinates:
            messagebox.showwarning("Warning", "No actions recorded. Record some actions first.")
            return
            
        try:
            # Generate script
            script_content = self.generate_script()
            
            # Save script
            script_path = os.path.join(self.dest, f"{self.file}.py")
            with open(script_path, 'w') as f:
                f.write(script_content)
                
            messagebox.showinfo("Success", 
                              f"Script saved successfully!\n"
                              f"File: {script_path}\n"
                              f"Actions: {len(self.coordinates)}")
            
            print(f"Script saved to: {script_path}")
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save script: {e}")
    
    def generate_script(self) -> str:
        """Generate Python script from recorded actions"""
        script_lines = [
            "#!/usr/bin/env python3",
            "# Generated by HumanCursor Scripter - Linux Edition",
            "# Make sure to install: pip install humancursor-linux",
            "",
            "import time",
            "from humancursor import SystemCursor",
            "",
            "def main():",
            "    # Initialize cursor for Linux",
            "    cursor = SystemCursor()",
            "    print('Starting recorded script...')",
            "    ",
            "    # Add small delay before starting",
            "    time.sleep(2)",
            "    "
        ]
        
        # Add recorded actions
        for i, action in enumerate(self.coordinates):
            script_lines.append(f"    # Action {i + 1}")
            
            if isinstance(action, list) and len(action) == 2 and isinstance(action[0], tuple):
                # Drag and drop
                start_pos = action[0]
                end_pos = action[1]
                script_lines.append(f"    cursor.drag_and_drop({list(start_pos)}, {list(end_pos)})")
                script_lines.append("    time.sleep(0.5)")
                
            elif isinstance(action, list) and len(action) == 1:
                # Click
                pos = action[0] if isinstance(action[0], (list, tuple)) else action
                script_lines.append(f"    cursor.click_on({list(pos)})")
                script_lines.append("    time.sleep(0.3)")
                
            else:
                # Move
                script_lines.append(f"    cursor.move_to({action})")
                script_lines.append("    time.sleep(0.2)")
                
        script_lines.extend([
            "    ",
            "    print('Script completed!')",
            "",
            "",
            "if __name__ == '__main__':",
            "    main()"
        ])
        
        return "\n".join(script_lines)
    
    def update_coordinates(self):
        """Update displayed mouse coordinates"""
        try:
            x, y = self.get_current_position()
            self.coordinates_label.config(text=f"x: {x}, y: {y}")
        except Exception:
            self.coordinates_label.config(text="x: ?, y: ?")
            
        # Schedule next update
        self.root.after(50, self.update_coordinates)  # 20 FPS update rate
    
    def __del__(self):
        """Cleanup when window is destroyed"""
        if self.recording:
            self.stop_recording()