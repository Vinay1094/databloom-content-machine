import numpy as np
import soundfile as sf
import os
from kokoro import KPipeline


class TTSEngine:
    def __init__(self, lang_code='a', voice='af_heart'):
        """
        Initialize Kokoro TTS Pipeline.
        lang_code: 'a' = American English
        voice: 'af_heart' is a high-quality default female voice
        """
        print("Initializing Kokoro TTS Pipeline...")
        self.pipeline = KPipeline(lang_code=lang_code)
        self.voice = voice

    def generate_audio(self, text, output_path="output/voiceover.wav"):
        """Generate a voiceover WAV file from text using Kokoro TTS."""
        print("Generating voiceover audio...")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Split pattern handles sentences so the model doesn't run out of memory
        generator = self.pipeline(
            text,
            voice=self.voice,
            speed=1,
            split_pattern=r'\n+'
        )

        audio_chunks = []
        for i, (gs, ps, audio) in enumerate(generator):
            audio_chunks.append(audio)

        if not audio_chunks:
            print("Failed to generate audio.")
            return None

        # Combine all audio chunks into one continuous track
        final_audio = np.concatenate(audio_chunks)
        sf.write(output_path, final_audio, 24000)
        print(f"Voiceover saved to {output_path}")
        return output_path
