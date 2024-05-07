import edge_tts

from src.interfaces.ai_provider_interface import TextToAudioProvider


class MicrosoftEdgeProvider(TextToAudioProvider):
    def text_to_audio(self, text: str) -> bytes:
        try:
            communicate = edge_tts.Communicate(text, self.params["voice"])
            communicate.save_sync("output.wav")

            file = open("output.wav", "rb")

            return file.read()
        except Exception as e:
            raise e
