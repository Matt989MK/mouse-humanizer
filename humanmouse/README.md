# humanmouse

Human-like mouse automation for Windows and Linux.

## Features
- Human-like mouse movement (bezier curves, jitter, variable speed)
- Click, hover, and move actions
- Randomized quirks: fidget, ADHD wander, overshoot/correct, rage click, double click
- Correction logic if the mouse lands in the wrong spot
- Cross-platform: works on both Windows and Linux

## Installation

### Local (editable)
```bash
pip install -e .
```

### From GitHub
```bash
pip install git+https://github.com/yourusername/humanmouse.git
```

## Usage

### Windows
```python
from humanmouse import HumanMouseController

mouse = HumanMouseController()
mouse.hover((500, 500))
mouse.click((600, 600))
mouse.move((800, 800))
```

### Linux
```python
from humanmouse import LinuxHumanMouseController

mouse = LinuxHumanMouseController()
mouse.hover((500, 500))
mouse.click((600, 600))
mouse.move((800, 800))
```

## License
MIT 