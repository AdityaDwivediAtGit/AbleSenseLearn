import speech_recognition as sr
import pyttsx3
import threading
import queue
from config import Config

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.command_queue = queue.Queue()
        
        # Configure voice
        self.engine.setProperty('rate', Config.VOICE_RATE)
        volumes = self.engine.getProperty('volume')
        self.engine.setProperty('volume', Config.VOICE_VOLUME)

    def speak(self, text):
        """Text-to-Speech output."""
        try:
            # Re-init engine in thread if needed for stability in Streamlit
            # Note: pyttsx3 can be tricky with threads. 
            # For Streamlit, we might prefer gTTS or client-side JS solutions for stability,
            # but we'll attempt local server-side playback first as requested.
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")

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

    def start_wake_word_listener(self):
        """
        Background thread to listen for a wake word (e.g., 'Hey Buddy').
        """
        # Note: In Streamlit, long-running background threads can be tricky due to reruns.
        # We might implement this as a session_state flag check or specific 'Listen Mode'.
        pass 
