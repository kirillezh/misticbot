import speech_recognition as sr
import subprocess
import os

class Converter:

    def __init__(self, path_to_file: str, language: str = "ru-RU"):
        self.language = language
        subprocess.run(['ffmpeg', '-v', 'quiet', '-i', path_to_file, path_to_file.replace(".ogg", ".wav")])
        self.wav_file = path_to_file.replace(".ogg", ".wav")

    def audio_to_text(self) -> str:
        r = sr.Recognizer()

        with sr.AudioFile(self.wav_file) as source:
            audio = r.record(source)
            r.adjust_for_ambient_noise(source)

        result = r.recognize_google(audio, language=self.language, show_all=True)
        if(result == []):
            return None
        res = self.localisation(result['alternative'][0]['transcript'])
        return res

    def localisation(self, text):
        from src.locales import localisation
        for i, j in localisation['ua']['local_v2t'].items():
            text = text.replace(i, j)
        return text

    def __del__(self):
        os.remove(self.wav_file)
