
import streamlit as st
import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random

from mic_recorder import st_mic_recorder  # Import mic-recorder
from time import ctime
from gtts import gTTS

# Initialize recognizer
r = sr.Recognizer()

def erza_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 1000000)
    #audio_file = 'audio' +str(r) + '.mp3'
    audio_file = f'audio{r}.mp3'
    tts.save(audio_file)
    #playsound.playsound(audio_file)

    # Streamlit's built-in audio player
    audio_bytes = open(audio_file, 'rb').read()
    st.audio(audio_bytes, format='audio/mp3')
    
    print(audio_string)
    os.remove(audio_file)
    
# def record_audio(ask = False):
#     with sr.Microphone() as source:
#         if ask:
#             erza_speak(ask)
#         audio = r.listen(source)
#         voice_data = ''
#         try:
#             voice_data = r.recognize_google(audio, language="en-uk")
#         except sr.UnknownValueError:
#             erza_speak('Sorry, I did not get that')
#         except sr.RequestError:
#             erza_speak('sorry my speach service is down')
#         return voice_data

def record_audio():
    # Streamlit's mic-recorder for microphone input
    audio_data = st_mic_recorder(record_audio=True, key="mic-recorder")
    
    if audio_data is not None:
        # Convert the audio data into an AudioFile object for speech recognition
        audio_file = sr.AudioFile(audio_data)
        with audio_file as source:
            audio = r.record(source)  # Record the audio from the file
            try:
                voice_data = r.recognize_google(audio, language="en-uk")
                st.write("You said: ", voice_data)
                return voice_data
            except sr.UnknownValueError:
                st.write("Sorry, I did not get that.")
            except sr.RequestError:
                st.write("Sorry, my speech service is down.")

    return ""
    
def respond(voice_data):
    if 'what is your name' in voice_data:
        erza_speak('My name is Erza')
    if 'what time is it' in voice_data:
        erza_speak(ctime())
    if 'search' in voice_data:
        search = record_audio('what do you want to search for')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        erza_speak('here is what I found for ' + search)
    if 'find location' in voice_data:
        location = record_audio('whast is the location')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        erza_speak('here is the location of ' + location)
    if 'where are you from' in voice_data:
        import ipinfo
        handler = ipinfo.getHandler(access_token='2f0b7d20b933b2')
        details = handler.getDetails()
        erza_speak("I'm from " + details.country_name)
    if 'go to sleep' in voice_data:
        erza_speak('bye')
        exit()

# Main loop
st.title("Erza Voice Assistant")
st.write("How can I help you?")

time.sleep(1)
erza_speak('How can I help you?')
while 1:  
    voice_data = record_audio()
    respond(voice_data)
