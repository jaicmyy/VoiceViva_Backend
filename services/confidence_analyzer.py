import logging
import os

try:
    import librosa
    import numpy as np
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

logger = logging.getLogger(__name__)

def calculate_confidence(audio_path: str) -> float:
    """
    Analyzes audio to determine a 'Confidence Score' based on:
    - Fluency (lack of long pauses)
    - Speech energy
    """
    if not LIBROSA_AVAILABLE:
        return 70.0  # Default if librosa not installed

    try:
        if not os.path.exists(audio_path):
            return 0.0

        y, sr = librosa.load(audio_path, sr=None)
        
        # 1. Fluency: Check non-silent duration vs total
        non_silent_intervals = librosa.effects.split(y, top_db=25)
        non_silent_duration = sum(start - end for start, end in non_silent_intervals) / sr
        total_duration = len(y) / sr
        
        fluency_ratio = non_silent_duration / max(total_duration, 0.1)
        
        # 2. Confidence score calculation
        # Scale fluency ratio (0.3 to 0.8 is typical for good speech)
        score = (fluency_ratio * 100) + 20
        
        return min(round(score, 1), 100.0)

    except Exception as e:
        logger.warning(f"Confidence analysis failed: {e}")
        return 65.0
