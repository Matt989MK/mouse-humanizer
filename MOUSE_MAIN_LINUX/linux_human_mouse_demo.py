from linux_human_mouse_controller import LinuxHumanMouseController
import random
import time


def main():
    mouse = LinuxHumanMouseController()
    screen_width, screen_height = mouse.screen_width, mouse.screen_height
    print("🖱️ Linux Human Mouse Demo (with LinuxHumanMouseController quirks)")
    print("This will move your mouse randomly in a human-like way. Move your mouse to a safe area!")
    time.sleep(3)

    actions = ['move', 'click_left', 'click_right', 'hover']
    for i in range(18):
        action = random.choice(actions)
        pos = (random.randint(100, screen_width-100), random.randint(100, screen_height-100))
        print(f"Action {i+1}/18: {action} at {pos}")
        if action == 'move':
            mouse.move(pos)
        elif action == 'click_left':
            mouse.click(pos, button='left')
        elif action == 'click_right':
            mouse.click(pos, button='right')
        elif action == 'hover':
            mouse.hover(pos)
        time.sleep(random.uniform(0.7, 1.5))
    print("Demo complete!")

if __name__ == "__main__":
    main() 