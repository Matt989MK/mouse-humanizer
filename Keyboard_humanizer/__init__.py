"""
Keyboard Humanizer - Ultra-Realistic Human Typing Simulation for Linux

Provides realistic human typing behavior including:
- Natural typing rhythms and speeds
- Human errors and corrections (backspaces)
- Variable pacing and natural hesitations
- Random copy/paste behaviors
- Context-aware typing patterns
- Fatigue effects over time

Compatible with Linux systems using pynput and X11.
Just acts naturally human without complex configuration.
"""

from .core.humanizer import KeyboardHumanizer, create_humanizer
from .core.typing_engine import TypingEngine, TypingStats

__version__ = "1.0.0"
__author__ = "Linux Automation Team"
__license__ = "MIT"

__all__ = [
    'KeyboardHumanizer',
    'TypingEngine', 
    'TypingStats',
    'create_humanizer'
]