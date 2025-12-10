# Language	Code
# English	en
# Hindi	hi
# Telugu	te
# Tamil	ta
# Kannada	kn
# Malayalam	ml
# Marathi	mr
# Bengali	bn
# Gujarati	gu
# Punjabi	pa
# Urdu	ur
# Russian	ru
# Spanish	es
# French	fr
# German	de
# Italian	it
# Japanese	ja
# Korean	ko
# Chinese (Simplified)	zh-cn
# Chinese (Traditional)	zh-tw
# Arabic	ar
# Portuguese	pt
# Turkish	tr
# Indonesian	id
# Thai	th
# Vietnamese	vi
# Dutch	nl
# Greek	el
# Hebrew	he








from googletrans import Translator
from gtts import gTTS
import playsound
import os
import uuid

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

text = "how are you?"
target_lang = "bn"

translated_text = translate_text(text, target_lang)
print("Translated:", translated_text)

# Speak the translated text
speak(translated_text, target_lang)
