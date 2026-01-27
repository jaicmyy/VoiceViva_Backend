from faster_whisper import WhisperModel
import os

model = None

def get_model():
    global model
    if model is None:
        try:
            print("Loading Whisper Model (CPU Mode)...")
            model = WhisperModel("small", device="cpu", compute_type="int8")
            print("Whisper Model Loaded")
        except Exception as e:
            print(f"Failed to load Whisper Model: {e}")
            return None
    return model

def transcribe_audio(audio_path: str) -> str:
    # Ensure audio file exists
    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}")
        return ""

    try:
        model_instance = get_model()
        segments, _ = model_instance.transcribe(audio_path, language="en")

        transcript = []
        for segment in segments:
            transcript.append(segment.text)

        text = " ".join(transcript).strip()
        
        # STRICT ENGLISH CHECK: Remove any non-ASCII characters
        # This prevents storing Devanagari, Tamil, etc.
        import re
        # Allow Basic Latin, Latin-1 Supplement (for accents), and common punctuation
        # But for strict English, mostly ASCII is preferred.
        
        # Calculate ratio of non-ascii characters
        if not text: return ""
        
        non_ascii_count = sum(1 for c in text if ord(c) > 127)
        total_count = len(text)
        
        if total_count > 0 and (non_ascii_count / total_count) > 0.2:
             print(f"Detected non-English text ({non_ascii_count}/{total_count} chars). Rejected.")
             return "Audio not clear or not in English."

        # Double check: Remove remaining non-ascii just in case
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
        
        print(f"Transcript: {cleaned_text}")
        return cleaned_text

    except Exception as e:
        print(f"Transcription failed: {e}")
        return ""  # Return empty string so partial data can be saved
