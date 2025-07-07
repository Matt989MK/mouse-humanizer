"""
Simple Keyboard Humanizer 
Makes typing indistinguishable from human behavior without complex profiles
"""

import time
import random
from typing import Optional, Dict, Any, List
from .typing_engine import TypingEngine, TypingStats


class KeyboardHumanizer:
    """Simple human-like keyboard typing"""
    
    def __init__(self):
        """Initialize with natural human typing behavior"""
        self.engine = TypingEngine()
        
        # Simple human settings - no profiles needed
        self.simulate_errors = True
        self.auto_correct = True
        self.use_copy_paste = True
        self.add_thinking_pauses = True
        self.simulate_fatigue = True
        self.context_aware = True
        
        print("Keyboard Humanizer initialized with natural human behavior")
    
    def type_text(self, text: str, **kwargs) -> bool:
        """
        Type text with natural human behavior
        
        Args:
            text: Text to type
            **kwargs: Optional overrides
                - simulate_errors: Override error simulation
                - use_copy_paste: Override copy-paste behavior
                - add_pauses: Override thinking pauses
                - speed_multiplier: Speed adjustment (1.0 = normal)
        
        Returns:
            bool: True if successful
        """
        # Apply temporary settings if provided
        original_settings = {}
        for key in ['simulate_errors', 'use_copy_paste', 'add_thinking_pauses']:
            if key in kwargs:
                original_settings[key] = getattr(self, key)
                setattr(self, key, kwargs[key])
        
        if 'speed_multiplier' in kwargs:
            original_wpm = self.engine.base_wpm
            self.engine.base_wpm = int(self.engine.base_wpm * kwargs['speed_multiplier'])
        
        try:
            # Context analysis for natural adaptation
            if self.context_aware:
                self._adapt_to_context(text)
            
            # Update fatigue if enabled
            if self.simulate_fatigue:
                self._update_fatigue()
            
            # Type the text naturally
            success = self._type_text_naturally(text)
            
            return success
            
        finally:
            # Restore original settings
            for key, value in original_settings.items():
                setattr(self, key, value)
            if 'speed_multiplier' in kwargs:
                self.engine.base_wpm = original_wpm
    
    def _adapt_to_context(self, text: str):
        """Adapt typing behavior based on text content"""
        # Detect content type and adjust naturally
        if self._is_code_text(text):
            # Code - more careful with symbols
            self.engine.base_wpm = int(self.engine.base_wpm * 0.8)
            self.engine.error_rate *= 0.7
        elif self._is_email_text(text):
            # Email - copy-paste likely for addresses
            self.use_copy_paste = True
        elif self._is_formal_text(text):
            # Formal - slightly more careful
            self.engine.base_wpm = int(self.engine.base_wpm * 0.9)
            self.engine.error_rate *= 0.8
        elif self._has_repetitive_content(text):
            # Repetitive - faster with more copy-paste
            self.engine.base_wpm = int(self.engine.base_wpm * 1.2)
            self.use_copy_paste = True
    
    def _is_code_text(self, text: str) -> bool:
        """Detect if text looks like code"""
        code_indicators = [
            'def ', 'class ', 'import ', 'from ', 'if ', 'for ', 'while ',
            '{', '}', '[', ']', '()', '=>', '==', '!=', '&&', '||',
            'function', 'const', 'let', 'var', 'return'
        ]
        return any(indicator in text for indicator in code_indicators)
    
    def _is_email_text(self, text: str) -> bool:
        """Detect if text contains email-like content"""
        email_indicators = [
            '@', 'Dear', 'Sincerely', 'Best regards', 'Hi ', 'Hello',
            'Subject:', 'From:', 'To:', '.com', '.org', '.net'
        ]
        return any(indicator in text for indicator in email_indicators)
    
    def _is_formal_text(self, text: str) -> bool:
        """Detect formal writing"""
        formal_indicators = [
            'furthermore', 'therefore', 'consequently', 'moreover',
            'however', 'nevertheless', 'accordingly', 'thus'
        ]
        return any(indicator in text.lower() for indicator in formal_indicators)
    
    def _has_repetitive_content(self, text: str) -> bool:
        """Detect repetitive content"""
        words = text.split()
        if len(words) < 5:
            return False
        unique_words = set(words)
        return len(unique_words) / len(words) < 0.7
    
    def _update_fatigue(self):
        """Update fatigue level naturally"""
        session_duration = time.time() - self.engine.session_start
        self.engine.update_fatigue(session_duration)
    
    def _type_text_naturally(self, text: str) -> bool:
        """Type text with natural human patterns"""
        # Split into sentences for natural pacing
        sentences = self._split_into_sentences(text)
        
        for i, sentence in enumerate(sentences):
            # Natural pause between sentences
            if i > 0 and self.add_thinking_pauses:
                pause = self._get_thinking_pause()
                if pause > 0:
                    time.sleep(pause)
            
            # Type the sentence
            if not self.engine.type_text(sentence, use_copy_paste=self.use_copy_paste):
                return False
            
            # Occasional spontaneous corrections
            if random.random() < 0.05 and len(sentence) > 10:
                self.engine.add_spontaneous_correction(sentence)
        
        return True
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text naturally for pacing"""
        sentences = []
        current = ""
        
        for char in text:
            current += char
            if char in '.!?' and len(current.strip()) > 3:
                sentences.append(current.strip())
                current = ""
        
        if current.strip():
            sentences.append(current.strip())
        
        return sentences if sentences else [text]
    
    def _get_thinking_pause(self) -> float:
        """Get natural thinking pause"""
        if random.random() < 0.15:  # 15% chance
            return random.uniform(0.3, 1.5)
        return 0.0
    
    def get_session_stats(self) -> TypingStats:
        """Get current session statistics"""
        return self.engine.get_session_stats()
    
    def reset_session(self):
        """Reset the typing session"""
        self.engine.stats = TypingStats()
        self.engine.session_start = time.time()
        self.engine.fatigue_level = 0.0
        self.engine.recent_chars = []
        self.engine.recent_timings = []
        print("Session reset")
    
    def configure(self, **kwargs):
        """Configure humanizer settings"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                print(f"Set {key} = {value}")
            else:
                print(f"Unknown setting: {key}")
    
    def get_current_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return {
            'simulate_errors': self.simulate_errors,
            'auto_correct': self.auto_correct,
            'use_copy_paste': self.use_copy_paste,
            'add_thinking_pauses': self.add_thinking_pauses,
            'simulate_fatigue': self.simulate_fatigue,
            'context_aware': self.context_aware
        }
    
    def print_stats(self):
        """Print current session statistics"""
        stats = self.get_session_stats()
        config = self.get_current_config()
        
        print("\n=== Keyboard Humanizer Session Stats ===")
        print(f"Characters typed: {stats.characters_typed}")
        print(f"Words typed: {stats.words_typed}")
        print(f"Current WPM: {stats.current_wpm:.1f}")
        print(f"Accuracy: {stats.accuracy:.1f}%")
        print(f"Errors made: {stats.errors_made}")
        print(f"Corrections made: {stats.corrections_made}")
        print(f"Session duration: {stats.session_duration:.1f}s")
        print(f"Fatigue level: {self.engine.fatigue_level:.1%}")
        print("=" * 40)


# Convenience function
def create_humanizer() -> KeyboardHumanizer:
    """Create a keyboard humanizer with natural human behavior"""
    return KeyboardHumanizer()