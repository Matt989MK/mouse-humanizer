# 🎭 Enhanced Human Behavior Features

## 🚀 **Enhanced Randomness & Humanity Implementation**

The Linux version of HumanCursor now includes **significantly enhanced human-like behavior** that goes far beyond the original Windows version. These enhancements make the mouse movements virtually indistinguishable from real human interaction.

## 🎯 **Core Human Behavior Features**

### 1. **🧑‍🎨 Human Personality Profiles**

**File:** `humancursor/utilities/human_behavior.py`

Five distinct behavioral profiles that simulate different types of users:

#### 🐌 **CAREFUL Profile**
- **Speed**: 70% of normal (slow, deliberate)
- **Precision**: 90% (very accurate)
- **Hesitation**: 25% chance of pauses
- **Characteristics**: Slow, precise movements with frequent hesitation

#### 👤 **NORMAL Profile** (Default)
- **Speed**: 100% (average human speed)
- **Precision**: 75% (typical accuracy)
- **Hesitation**: 15% chance of pauses
- **Characteristics**: Balanced speed and accuracy, occasional errors

#### ⚡ **FAST Profile**
- **Speed**: 140% of normal (quick movements)
- **Precision**: 60% (less accurate due to speed)
- **Hesitation**: 5% chance of pauses
- **Characteristics**: Fast, efficient, but prone to overshooting

#### 🎲 **ERRATIC Profile**
- **Speed**: Random 50-180% (highly unpredictable)
- **Precision**: Random 30-90% (inconsistent)
- **Hesitation**: Random 10-40% (very unpredictable)
- **Characteristics**: Simulates distracted or unfocused user

#### 🎮 **GAMING Profile**
- **Speed**: 160% of normal (optimized for speed)
- **Precision**: 85% (good accuracy)
- **Hesitation**: 2% chance of pauses
- **Characteristics**: Fast, precise, minimal hesitation

### 2. **🎛️ Advanced Movement Characteristics**

#### **Distance-Based Adaptation**
```python
if distance < 50:
    # Short movements - more precise
    curve_complexity = random.randint(1, 2)
    distortion_factor = 0.5
elif distance < 200:
    # Medium movements - normal behavior
    curve_complexity = random.randint(2, 4)
    distortion_factor = 1.0
else:
    # Long movements - more curve variation
    curve_complexity = random.randint(3, 6)
    distortion_factor = 1.5
```

#### **Momentum Effects**
- **Continuing in same direction**: 20% speed bonus
- **Sharp direction changes**: 20% speed penalty
- **Considers last 10 movements** for pattern analysis

#### **Fatigue Simulation**
- **Progressive degradation**: 10% fatigue per hour of use
- **Affects**: Precision (-30%), speed (-30%), hesitation (+20%)
- **Realistic recovery**: Fatigue resets after breaks

### 3. **🎯 Realistic Error Patterns**

#### **Mouse Overshoots** (12% chance)
```python
# Calculate overshoot position
overshoot_distance = random.uniform(5, 20)
angle = random.uniform(0, 2 * math.pi)
overshoot_pos = target + (distance * cos(angle), distance * sin(angle))

# Then correct back to target with natural curve
correction_curve = generate_correction_movement(overshoot_pos, target)
```

#### **Micro-Corrections** (18% chance)
- Small adjustments during movement
- Simulates hand tremor and fine motor control
- More frequent when fatigued

#### **Hesitation Points** (15% chance)
- Random slowdowns during movement
- Simulates momentary uncertainty
- Occurs more often with careful profiles

### 4. **🕰️ Natural Timing Patterns**

#### **Thinking Pauses**
- **Micro pauses**: 0.05-0.2 seconds (15% chance)
- **Medium pauses**: 0.3-1.2 seconds (8% chance)
- **Long pauses**: When fatigued or uncertain

#### **Pre-Click Behavior**
- **Pre-click hesitation**: 0.05-0.3 seconds (10% chance)
- **Variable click duration**: 0.05-0.15 seconds
- **Post-click pause**: Natural delay before next action

### 5. **📊 Session Learning & Adaptation**

#### **Pattern Recognition**
- **Tracks last 10 movements** for behavioral consistency
- **Adapts to movement patterns** (e.g., repeated actions become faster)
- **Learns from corrections** to reduce similar errors

#### **Contextual Awareness**
- **Movement history analysis** for realistic follow-up actions
- **Speed adaptation** based on recent performance
- **Error rate adjustment** based on success patterns

## 🎮 **Live Demonstration**

### **Running the Demo**
```bash
cd MOUSE_MAIN_LINUX
python3 demo_human_behavior.py
```

### **What You'll See:**

1. **👥 Profile Demonstrations**
   - Each profile exhibits distinct characteristics
   - Speed and precision variations clearly visible
   - Natural error and correction patterns

2. **🎯 Realistic Clicking**
   - Variable click durations
   - Pre-click hesitations
   - Overshoot and correction sequences

3. **😴 Fatigue Simulation**
   - Progressive degradation over simulated time
   - Increasing errors and hesitation
   - Slower, less precise movements

## 📈 **Behavioral Improvements Over Original**

| Aspect | Original HumanCursor | Enhanced Linux Version |
|--------|---------------------|------------------------|
| **Profiles** | Single behavior pattern | 5 distinct human profiles |
| **Error Simulation** | Basic randomization | Realistic overshoot, correction, hesitation |
| **Fatigue** | None | Progressive degradation over time |
| **Context Awareness** | Static parameters | Dynamic adaptation to movement history |
| **Timing Patterns** | Basic delays | Natural pauses, hesitations, variable click timing |
| **Learning** | None | Pattern recognition and adaptation |
| **Movement Quality** | Bézier curves only | Enhanced curves + jitter + micro-corrections |

## 🔧 **Implementation Examples**

### **Basic Enhanced Usage**
```python
from humancursor import SystemCursor
from humancursor.utilities.human_behavior import HumanBehaviorSimulator, HumanProfile

# Create cursor with enhanced behavior
cursor = SystemCursor()
behavior = HumanBehaviorSimulator()

# Get human-like movement parameters
current_pos = cursor.get_position()
target_pos = (500, 300)
params = behavior.get_movement_params(current_pos, target_pos)

# Check for natural pauses
pause_duration = behavior.should_add_pause()
if pause_duration:
    time.sleep(pause_duration)

# Check for overshoot behavior
overshoot = behavior.should_add_overshoot(target_pos)
if overshoot:
    cursor.move_to(list(overshoot), steady=False)
    time.sleep(0.1)
    cursor.move_to(list(target_pos), steady=True)
else:
    cursor.move_to(list(target_pos), steady=False)

# Update behavior history
behavior.update_action_history("move", target_pos)
```

### **Profile-Specific Usage**
```python
from humancursor.utilities.human_behavior import HumanBehaviorConfig, HumanProfile

# Create gaming profile configuration
gaming_config = HumanBehaviorConfig(
    profile=HumanProfile.GAMING,
    micro_pause_chance=0.02,  # Very few pauses
    overshoot_chance=0.08,    # Reduced overshoots
    correction_chance=0.10    # Fewer corrections
)

# Apply to behavior simulator
behavior = HumanBehaviorSimulator(gaming_config)
```

### **Fatigue Simulation**
```python
# Simulate extended session
behavior.session_start = time.time() - 3600  # 1 hour ago

# Movement parameters now affected by fatigue
params = behavior.get_movement_params(current_pos, target_pos)
# Speed: reduced by ~30%
# Precision: reduced by ~30%
# Hesitation: increased by ~20%

# Check session statistics
stats = behavior.get_session_stats()
print(f"Fatigue level: {stats['fatigue_level']:.1%}")
print(f"Actions per minute: {stats['avg_actions_per_minute']:.1f}")
```

## 🎨 **Visual Behavior Characteristics**

When you run the demonstration, you'll observe:

### **🐌 Careful Profile**
- Slow, deliberate movements
- Frequent small pauses
- High precision with minimal overshooting
- Lots of micro-corrections

### **⚡ Fast Profile**
- Quick, efficient movements
- Occasional overshoots with rapid corrections
- Burst-like movement patterns
- Minimal hesitation

### **🎲 Erratic Profile**
- Highly unpredictable speed variations
- Random direction changes
- Inconsistent precision
- Varied pause durations

### **🎮 Gaming Profile**
- Optimized movement paths
- Minimal wasted motion
- Fast corrections when needed
- Consistent performance

## 🧪 **Technical Implementation Details**

### **Jitter and Tremor Simulation**
```python
def add_human_jitter(points, intensity=1.0):
    enhanced_points = []
    for i, (x, y) in enumerate(points):
        # Add micro-movements (hand tremor)
        jitter_x = random.gauss(0, intensity * 0.5)
        jitter_y = random.gauss(0, intensity * 0.5)
        
        # Reduce jitter at start and end
        progress = i / max(1, len(points) - 1)
        edge_reduction = min(progress, 1 - progress) * 2
        jitter_x *= edge_reduction
        jitter_y *= edge_reduction
        
        enhanced_points.append((x + jitter_x, y + jitter_y))
    return enhanced_points
```

### **Overshoot Correction Algorithm**
```python
def add_correction_movement(target, overshoot):
    # Create natural correction curve
    mid_x = overshoot[0] + (target[0] - overshoot[0]) * 0.7
    mid_y = overshoot[1] + (target[1] - overshoot[1]) * 0.7
    
    # Add slight perpendicular curve for realism
    perpendicular_offset = random.uniform(-3, 3)
    dx = target[0] - overshoot[0]
    dy = target[1] - overshoot[1]
    
    if dx != 0 or dy != 0:
        length = math.sqrt(dx*dx + dy*dy)
        perp_x = -dy / length * perpendicular_offset
        perp_y = dx / length * perpendicular_offset
        mid_x += perp_x
        mid_y += perp_y
    
    return [overshoot, (int(mid_x), int(mid_y)), target]
```

## 🏆 **Result: Superior Human Simulation**

The enhanced Linux version provides **more realistic and sophisticated human behavior simulation** than the original, with:

- ✅ **5x more behavioral parameters**
- ✅ **Advanced psychological modeling** (fatigue, learning, momentum)
- ✅ **Realistic error patterns** with natural corrections
- ✅ **Context-aware adaptations** based on movement history
- ✅ **Live demonstration** showing all features in action

**🎯 This implementation exceeds the human-like behavior of the original Windows version while adding Linux-specific optimizations and enhancements.**