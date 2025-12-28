import speech_recognition as sr
import pyttsx3
import threading
import queue
import os
from gtts import gTTS
from config import Config
import tempfile
from utils.debug import debug_trace

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        # Try initializing pyttsx3, but don't crash if it fails (common in linux/cloud)
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', Config.VOICE_RATE)
            self.engine.setProperty('volume', Config.VOICE_VOLUME)
            self.pyttsx3_available = True
        except Exception as e:
            print(f"Warning: pyttsx3 initialization failed ({e}). Using gTTS only.")
            self.engine = None
            self.pyttsx3_available = False

    @debug_trace
    def speak(self, text):
        """
        Converts text to speech and returns the path to the audio file.
        Returns: (audio_file_path, is_temp_file)
        """
        try:
            # Priority 1: gTTS (Better quality, works in cloud)
            # Create a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                temp_path = fp.name
                
            tts = gTTS(text=text, lang='en')
            tts.save(temp_path)
            return temp_path, True
            
        except Exception as e:
            print(f"gTTS failed ({e}), trying pyttsx3...")
            
            # Priority 2: pyttsx3 (Offline fallback)
            if self.pyttsx3_available and self.engine:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
                        temp_path = fp.name
                    # Saving to file instead of saying immediately
                    self.engine.save_to_file(text, temp_path)
                    self.engine.runAndWait()
                    return temp_path, True
                except Exception as e2:
                    print(f"pyttsx3 failed: {e2}")
            
            return None, False

    @debug_trace
    def listen_for_command(self):
        """
        One-shot listening for a command (used when button pressed).
        Returns the text recognized.
        """
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Mic Error: {e}")
            return None

