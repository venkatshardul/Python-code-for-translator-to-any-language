import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os
import uuid

r= sr.Recognizer()

with sr.AudioFile("030464_girl-saying-quothello39-different-ways-65739.wav") as source:
    audio = r.record(source)

try:
    text = r.recognize_google(audio)
    
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("API error:", e)



def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

def speak(text, language):
    file_name = f"{uuid.uuid4()}.mp3"  # random filename
    tts = gTTS(text=text, lang=language)
    tts.save(file_name)
    playsound.playsound(file_name)
    os.remove(file_name)  # delete after playing


target_lang = "bn"

translated_text = translate_text(text, target_lang)
print("Translated:", translated_text)

# Speak the translated text
speak(translated_text, target_lang)