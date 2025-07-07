from .windows_controller import HumanMouseController
from .linux_controller import LinuxHumanMouseController

class HumanMouse:
    def __init__(self, *args, **kwargs):
        self._impl = LinuxHumanMouseController(*args, **kwargs)
    def move(self, pos, duration=0.5):
        return self._impl.move(pos, duration=duration)
    def click(self, pos, button='left'):
        return self._impl.click(pos, button=button)
    def hover(self, pos):
        return self._impl.hover(pos)
    def scroll(self, amount):
        return self._impl.scroll(amount)
    @property
    def screen_width(self):
        return self._impl.screen_width
    @property
    def screen_height(self):
        return self._impl.screen_height

