# 🎭 Human Behavior Features

## Overview

This library's sole purpose is to make automated mouse movement and keyboard typing indistinguishable from real human behavior. It achieves this through natural randomization, realistic timing, and human-like errors and corrections.

## 🖱️ Mouse Movement Humanization

### 1. Natural Movement Curves
**Where:** `humancursor/system_cursor.py` → `_move_human_like()`
**How:** Instead of straight lines, movements follow natural bezier curves with random control points
**When:** Every mouse movement (unless `steady=True`)

```python
# Creates natural arc-like movements
control_points = self._generate_control_points(start, end, curve_intensity)
curve_points = self._interpolate_curve(control_points, num_points)
```

### 2. Speed Variation Based on Distance
**Where:** `humancursor/system_cursor.py` → `_move_human_like()`
**How:** 
- Short movements (<50px): 30% slower (more precise)
- Long movements (>500px): 30% faster 
- Random ±30% speed variation added
**When:** Every movement calculation

```python
if distance < 50:
    base_speed = 0.7  # Slower for precise movements
elif distance > 500:
    base_speed = 1.3  # Faster for long movements

speed = base_speed * (1 + random.uniform(-0.3, 0.3))
```

### 3. Micro-Jitter (Hand Tremor Simulation)
**Where:** `humancursor/system_cursor.py` → `_add_human_imperfections()`
**How:** Adds tiny random movements (0.5-1px) to simulate natural hand tremor
**When:** Every point along the movement curve

```python
jitter_x = random.gauss(0, jitter_intensity)
jitter_y = random.gauss(0, jitter_intensity)
# Reduced at start/end of movement for realism
```

### 4. Natural Overshoots and Corrections
**Where:** `humancursor/system_cursor.py` → `_add_overshoot_correction()`
**How:** 8% chance to overshoot target by 3-12 pixels, then naturally correct back
**When:** After reaching target position (if error occurs)

```python
if random.random() < self.error_chance:  # 8% chance
    overshoot_distance = random.uniform(3, 12)
    # Move to overshoot position, pause, then correct
```

### 5. Micro-Pauses and Hesitations
**Where:** `humancursor/system_cursor.py` → `_move_human_like()`
**How:** 12% chance of small pauses (0.05-0.2s) before movements
**When:** Before starting any movement

```python
if random.random() < self.micro_pause_chance:  # 12%
    time.sleep(random.uniform(0.05, 0.2))
```

### 6. Fatigue Simulation
**Where:** `humancursor/system_cursor.py` → `_move_human_like()`
**How:** Gradual speed reduction and increased errors over 2+ hours of use
**When:** Calculated each movement based on session duration

```python
session_time = time.time() - self.session_start
self.fatigue_level = min(0.3, session_time / 7200)  # Max 30% over 2 hours
speed *= (1 - self.fatigue_level * 0.5)  # Slower when fatigued
```

### 7. Click Humanization
**Where:** `humancursor/system_cursor.py` → `click_on()`
**How:** 
- Variable click duration (0.05-0.15s)
- Pre-click pauses (15% chance, 0.05-0.2s)
- Natural timing variations
**When:** Every click operation

### 8. Resolution Independence
**Where:** `humancursor/system_cursor.py` → `_detect_screen_resolution()`
**How:** Automatically detects screen resolution and ensures all coordinates stay within bounds
**When:** During initialization and every movement

```python
# Ensure coordinates are within screen bounds
x = max(0, min(self.screen_width - 1, int(x)))
y = max(0, min(self.screen_height - 1, int(y)))
```

## ⌨️ Keyboard Typing Humanization

### 1. Natural Typing Rhythm
**Where:** `keyboard_humanizer/core/typing_engine.py` → `calculate_char_delay()`
**How:** Variable delays between keystrokes based on character difficulty and natural patterns
**When:** Between every character typed

```python
# Base timing from realistic WPM (45 words/min = 225 chars/min)
base_delay = 60 / (self.base_wpm * 5)
delay = base_delay + random.uniform(-0.3, 0.3) * base_delay
```

### 2. Character Difficulty Simulation
**Where:** `keyboard_humanizer/core/typing_engine.py` → `_get_char_difficulty_multiplier()`
**How:** Different delays for different character types:
- Uppercase: 30% slower (shift coordination)
- Special symbols: 80% slower (!@#$%^&*)
- Numbers/punctuation: 20% slower
- Awkward key combinations: 40% slower
**When:** Every character based on current and previous character

### 3. Realistic Typing Errors
**Where:** `keyboard_humanizer/core/typing_engine.py` → `generate_error()`
**How:** Four types of realistic errors with 2% base rate:
- **Substitution:** Wrong character (adjacent keys) - "helko" instead of "hello"
- **Insertion:** Extra character - "helllo" instead of "hello"  
- **Deletion:** Missing character - "helo" instead of "hello"
- **Transposition:** Swapped characters - "hellow" instead of "hello"
**When:** During character typing based on error probability

### 4. Intelligent Error Correction
**Where:** `keyboard_humanizer/core/typing_engine.py` → `should_correct_error()`
**How:** 80% of errors get corrected with realistic backspacing and retyping
**When:** After an error is made (brief pause, then correction)

```python
# Backspace to remove error
for _ in range(backspaces):
    self.controller.press(Key.backspace)
    time.sleep(random.uniform(0.05, 0.15))
# Then type correct character
```

### 5. Thinking Pauses
**Where:** `keyboard_humanizer/core/typing_engine.py` → `add_thinking_pause()`
**How:** Natural pauses during typing:
- Quick pause: 0.2-0.8s (60% of pauses)
- Medium pause: 0.8-2.0s (30% of pauses)  
- Long pause: 2.0-5.0s (10% of pauses)
**When:** Random intervals and at sentence boundaries

### 6. Context-Aware Behavior
**Where:** `keyboard_humanizer/core/humanizer.py` → `_analyze_text_context()`
**How:** Adjusts typing behavior based on content type:
- **Code:** 20% slower, more careful with symbols
- **Email:** Copy-paste for email addresses
- **Formal text:** 10% slower, fewer errors
- **Repetitive:** 20% faster, more copy-paste
**When:** Before typing each text block

### 7. Copy-Paste Intelligence
**Where:** `keyboard_humanizer/core/typing_engine.py` → `_should_copy_paste()`
**How:** Automatically detects content that humans typically copy-paste:
- Email addresses, URLs
- Repeated words/phrases
- Long technical terms (6+ characters)
**When:** During text analysis, 30-40% chance for qualifying content

### 8. Spontaneous Corrections
**Where:** `keyboard_humanizer/core/typing_engine.py` → `add_spontaneous_correction()`
**How:** 5% chance to go back 2-8 characters to fix earlier "errors"
**When:** Randomly during longer text blocks

## 🔧 Technical Implementation Details

### Error Rate Calculation
```python
error_chance = self.error_rate * (1 + self.fatigue_level * 2)
if char.isupper() or char in special_chars:
    error_chance *= 1.5
```

### Movement Timing
```python
delay = 0.001 + random.uniform(0, 0.003)  # 1-4ms between points
delay *= (1 + self.fatigue_level * 0.5)   # Slower when fatigued
```

### Natural Curve Generation
```python
# Control points create natural arc
cp1_x = start[0] + dx * 0.33  # 1/3 along path
cp2_x = start[0] + dx * 0.67  # 2/3 along path
# Add perpendicular offset for curve
offset = random.uniform(-20, 20) * intensity
```

## 🎯 Key Humanization Principles

### 1. **Variability Over Consistency**
Humans are naturally inconsistent. The library adds randomness to every aspect:
- Speed varies by ±30%
- Timing has micro-variations
- Errors occur unpredictably
- Pauses happen randomly

### 2. **Context Sensitivity** 
Behavior changes based on situation:
- Distance affects movement speed
- Character type affects typing speed
- Content type affects behavior patterns
- Fatigue accumulates over time

### 3. **Natural Error Patterns**
Mistakes follow realistic patterns:
- Adjacent key substitutions
- Common finger slips
- Overshoots on long movements
- Incomplete corrections

### 4. **Progressive Changes**
Behavior evolves during use:
- Fatigue builds gradually
- Recent actions influence future ones
- Movement history affects patterns
- Timing adapts to context

## 🚫 What We DON'T Do

- **No display management** - We never create, modify, or kill displays
- **No complex profiles** - Behavior is naturally randomized without user configuration
- **No external dependencies** - Works with standard Python libraries
- **No system modifications** - Only simulates input, doesn't change system settings

## ✅ Compatibility

- **All screen resolutions** - Automatically detects and adapts
- **All Linux desktop environments** - Works with X11 and most window managers  
- **Fallback methods** - Uses pynput primarily, X11 as backup
- **Headless operation** - Works without GUI (for servers)

This creates typing and mouse movement that is virtually indistinguishable from real human behavior, with natural variations, realistic errors, and context-appropriate timing.