
import streamlit as st
import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random

#import os
import numpy as np
#import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components

#from streamlit_mic_recorder import st_mic_recorder  # Import mic-recorder
#from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase

from io import BytesIO

from time import ctime
from gtts import gTTS

# Initialize recognizer
r = sr.Recognizer()

# Initialize audio data storage
audio_data = None

def st_audiorec():

    # get parent directory relative to current directory
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    st.write(parent_dir)
    # Custom REACT-based component for recording client audio in browser
    build_dir = os.path.join(parent_dir, "")
    # specify directory and initialize st_audiorec object functionality
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)

    # Create an instance of the component: STREAMLIT AUDIO RECORDER
    raw_audio_data = st_audiorec()  # raw_audio_data: stores all the data returned from the streamlit frontend
    wav_bytes = None                # wav_bytes: contains the recorded audio in .WAV format after conversion

    # the frontend returns raw audio data in the form of arraybuffer
    # (this arraybuffer is derived from web-media API WAV-blob data)

    if isinstance(raw_audio_data, dict):  # retrieve audio data
        with st.spinner('retrieving audio-recording...'):
            ind, raw_audio_data = zip(*raw_audio_data['arr'].items())
            ind = np.array(ind, dtype=int)  # convert to np array
            raw_audio_data = np.array(raw_audio_data)  # convert to np array
            sorted_ints = raw_audio_data[ind]
            stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            # wav_bytes contains audio data in byte format, ready to be processed further
            wav_bytes = stream.read()

    return wav_bytes
    
# # Audio processor class for streamlit-webrtc
# class AudioProcessor(AudioProcessorBase):
#     def recv(self, frame):
#         global audio_data
#         # This function gets called with the microphone stream in each frame
#         audio_data = frame.to_bytes()  # Convert the frame to bytes
#         return frame
    
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

    # TUTORIAL: How to use STREAMLIT AUDIO RECORDER?
    # by calling this function an instance of the audio recorder is created
    # once a recording is completed, audio data will be saved to audio_data

    audio_data = st_audiorec() # tadaaaa! yes, that's it! :D

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
# TITLE and Creator information
st.markdown('Implemented by '
        '[AA](https://www.linkedin.com/in/stefanrmmr/) - '
        'view project source code on '
                
        '[GitHub](https://github.com/stefanrmmr/streamlit-audio-recorder)')
st.write('\n\n')
st.write("Click the button to start the voice assistant")

# Start the webrtc streamer for capturing audio
#webrtc_streamer(key="example", mode=WebRtcMode.SENDRECV, audio_processor_factory=AudioProcessor)


time.sleep(1)

# Start interaction on button click
if st.button("Start Voice Assistant"):
    erza_speak('How can I help you?')
    while 1:  
        voice_data = record_audio()
        if voice_data:
            respond(voice_data)
