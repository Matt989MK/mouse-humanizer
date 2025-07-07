import pytest
from humanmouse import HumanMouse, type_text, press_key, hotkey

def test_mouse_move_and_click():
    mouse = HumanMouse()
    screen_width, screen_height = mouse.screen_width, mouse.screen_height
    center = (screen_width // 2, screen_height // 2)
    mouse.move(center, duration=0.5)
    mouse.click(center)

def test_mouse_scroll():
    mouse = HumanMouse()
    mouse.scroll(5)
    mouse.scroll(-5)

def test_type_text():
    type_text("Hello, world!")

def test_press_key():
    press_key("enter")

def test_hotkey():
    hotkey("ctrl", "a")

