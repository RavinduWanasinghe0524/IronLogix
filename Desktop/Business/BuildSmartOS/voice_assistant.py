"""
Voice Assistant for BuildSmartOS
Supports voice commands in Sinhala, Tamil, and English
"""
import speech_recognition as sr
import pyttsx3
import threading
import queue

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.command_queue = queue.Queue()
        
        # Configure speech engine
        self.engine.setProperty('rate', 150)  # Speed
        self.engine.setProperty('volume', 0.9)  # Volume
        
        # Command keywords in multiple languages
        self.commands = {
            'english': {
                'add': ['add', 'add product', 'add to cart'],
                'remove': ['remove', 'delete', 'remove from cart'],
                'checkout': ['checkout', 'pay', 'bill', 'complete'],
                'search': ['search', 'find', 'look for'],
                'total': ['total', 'amount', 'how much'],
                'help': ['help', 'commands', 'what can you do']
            },
            'sinhala': {
                'add': ['එකතු', 'එකතු කරන්න'],
                'remove': ['ඉවත්', 'මකන්න'],
                'checkout': ['ගෙවීම', 'බිල'],
                'search': ['සොයන්න', 'හොයන්න'],
                'total': ['එකතුව', 'මුදල'],
                'help': ['උදව්', 'පෙන්වන්න']
            },
            'tamil': {
                'add': ['சேர்', 'சேர்க்க'],
                'remove': ['நீக்கு', 'அகற்று'],
                'checkout': ['பணம் செலுத்து', 'பில்'],
                'search': ['தேடு', 'கண்டுபிடி'],
                'total': ['மொத்தம்', 'தொகை'],
                'help': ['உதவி', 'கட்டளைகள்']
            }
        }
    
    def speak(self, text, language='english'):
        """Convert text to speech"""
        try:
            # Set voice based on language (if available)
            voices = self.engine.getProperty('voices')
            
            # Use first available voice (can be extended for language-specific voices)
            if voices:
                self.engine.setProperty('voice', voices[0].id)
            
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"Speech error: {e}")
    
    def listen(self, language='english', timeout=5):
        """Listen for voice command"""
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio, language=self._get_language_code(language))
                
                print(f"Recognized: {text}")
                return True, text.lower()
                
        except sr.WaitTimeoutError:
            return False, "Timeout - no speech detected"
        except sr.UnknownValueError:
            return False, "Could not understand audio"
        except sr.RequestError as e:
            return False, f"Recognition service error: {e}"
        except Exception as e:
            return False, f"Error: {e}"
    
    def _get_language_code(self, language):
        """Get Google Speech Recognition language code"""
        codes = {
            'english': 'en-US',
            'sinhala': 'si-LK',
            'tamil': 'ta-IN'
        }
        return codes.get(language, 'en-US')
    
    def parse_command(self, text, language='english'):
        """Parse voice command and extract intent"""
        text = text.lower()
        
        for intent, keywords in self.commands.get(language, {}).items():
            for keyword in keywords:
                if keyword in text:
                    # Extract additional information (e.g., product name, quantity)
                    remainder = text.replace(keyword, '').strip()
                    return {
                        'intent': intent,
                        'text': remainder,
                        'original': text
                    }
        
        return {
            'intent': 'unknown',
            'text': text,
            'original': text
        }
    
    def start_continuous_listening(self, callback, language='english'):
        """Start continuous listening mode"""
        if self.is_listening:
            return False, "Already listening"
        
        self.is_listening = True
        thread = threading.Thread(target=self._listen_loop, args=(callback, language))
        thread.daemon = True
        thread.start()
        
        return True, "Voice assistant started"
    
    def _listen_loop(self, callback, language):
        """Continuous listening loop"""
        self.speak("Voice assistant activated", language)
        
        while self.is_listening:
            success, text = self.listen(language, timeout=10)
            
            if success:
                # Parse command
                command = self.parse_command(text, language)
                
                # Add to queue
                self.command_queue.put(command)
                
                # Call callback
                if callback:
                    callback(command)
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        self.speak("Voice assistant deactivated")
    
    def get_command(self):
        """Get next command from queue"""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None

# Global instance
_voice_assistant = None

def get_voice_assistant():
    """Get or create voice assistant instance"""
    global _voice_assistant
    if _voice_assistant is None:
        _voice_assistant = VoiceAssistant()
    return _voice_assistant

# Quick functions
def speak(text, language='english'):
    """Quick speak function"""
    assistant = get_voice_assistant()
    assistant.speak(text, language)

def listen_once(language='english'):
    """Quick listen function"""
    assistant = get_voice_assistant()
    return assistant.listen(language)
