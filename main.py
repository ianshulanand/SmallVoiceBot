
import streamlit as st
import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random

#from streamlit_mic_recorder import st_mic_recorder  # Import mic-recorder
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
from io import BytesIO

from time import ctime
from gtts import gTTS

# Initialize recognizer
r = sr.Recognizer()

# Initialize audio data storage
audio_data = None

# Audio processor class for streamlit-webrtc
class AudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        global audio_data
        # This function gets called with the microphone stream in each frame
        audio_data = frame.to_bytes()  # Convert the frame to bytes
        return frame
    
def erza_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 1000000)
    #audio_file = 'audio' +str(r) + '.mp3'
    audio_file = f'audio{r}.mp3'
    tts.save(audio_file)

    # Streamlit's built-in audio player
    audio_bytes = open(audio_file, 'rb').read()
    st.audio(audio_bytes, format='audio/mp3')
    
    print(audio_string)
    os.remove(audio_file)
    


# Function to process the recorded audio and convert it into text using Google Speech Recognition
def record_audio():
    global audio_data
    if audio_data:
        # Convert audio data to an AudioFile object
        with sr.AudioFile(BytesIO(audio_data)) as source:
            audio = r.record(source)
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
        erza_speak('Goodbye!')
        exit()

# Main loop
st.title("Erza Voice Assistant")
st.write("Click the button to start the voice assistant")

# Start the webrtc streamer for capturing audio
webrtc_streamer(key="example", mode=WebRtcMode.SENDRECV, audio_processor_factory=AudioProcessor)


time.sleep(1)

# Start interaction on button click
if st.button("Start Voice Assistant"):
    erza_speak('How can I help you?')
    while 1:  
        voice_data = record_audio()
        if voice_data:
            respond(voice_data)
