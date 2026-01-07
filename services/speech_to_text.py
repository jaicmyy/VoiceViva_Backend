from faster_whisper import WhisperModel
import os

model = None

def get_model():
    global model
    if model is None:
        print("⏳ Loading Whisper Model...")
        model = WhisperModel("small", compute_type="int8")
        print("✅ Whisper Model Loaded")
    return model

def transcribe_audio(audio_path: str) -> str:
    # Ensure audio file exists
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return ""

    try:
        model_instance = get_model()
        segments, _ = model_instance.transcribe(audio_path)

        transcript = []
        for segment in segments:
            transcript.append(segment.text)

        text = " ".join(transcript).strip()
        print(f"📝 Transcript: {text}")
        return text

    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return ""
