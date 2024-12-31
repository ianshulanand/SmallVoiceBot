import streamlit as st
import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
import subprocess

#from streamlit_mic_recorder import st_mic_recorder  # Import mic-recorder
#from streamlit_webrtc import webrtc_streamer, WebRtcMode
from audio_recorder_streamlit import audio_recorder
from io import BytesIO

from time import ctime
from gtts import gTTS

# Initialize recognizer
r = sr.Recognizer()

def erza_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 1000000)
    #audio_file = 'audio' +str(r) + '.mp3'
    mp3_file = f'audio{r}.mp3' #mp3 audio file
    tts.save(mp3_file) # save mp3 audio file
    playsound.playsound(mp3_file)

    # Convert the MP3 to WAV for compatibility
    wav_file = f'audio{r}.wav' # We'll convert MP3 to WAV
    try:
        # Convert MP3 to WAV using ffmpeg
        subprocess.run(['ffmpeg', '-i', mp3_file, wav_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Successfully converted {mp3_file} to {wav_file}")

        # Play the WAV file in Streamlit
        audio_bytes = open(wav_file, 'rb').read()
        st.audio(audio_bytes, format='audio/wav')

        # os.remove(audio_file)  # Remove MP3 after conversion
    
        # audio_file=wav_file
        # # Streamlit's built-in audio player
        # audio_bytes = open(audio_file, 'rb').read()
        # st.audio(audio_bytes, format='audio/wav')
    
        print(audio_string)

    except subprocess.CalledProcessError as e:
        st.error("Error during MP3 to WAV conversion!")
        print(f"Error: {e}")

    finally:
        # Clean up temporary files
        if os.path.exists(mp3_file):
            os.remove(mp3_file)
        if os.path.exists(wav_file):
            os.remove(wav_file)

        #os.remove(audio_file)

def record_audio(ask = False):

    # Convert audio data to an AudioFile object
    audio_data = audio_recorder()
    if audio_data:
        st.audio(audio_data, format="audio/wav")
    
    with sr.AudioFile(BytesIO(audio_data)) as source:

        if ask:
            erza_speak(ask)

        audio = r.record(source)
        voice_data = ''

        try:
            voice_data = r.recognize_google(audio, language="en-uk")
            st.write("You said: ", voice_data)
            #return voice_data
        except sr.UnknownValueError:
            erza_speak('Sorry, I did not get that')
            st.write("Sorry, I did not get that.")
            
        except sr.RequestError:
            erza_speak('sorry my speach service is down')
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
