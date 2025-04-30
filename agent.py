import speech_recognition as sr  # type: ignore
import pyttsx3 # type: ignore
import google.generativeai as genai # type: ignore
import os # type: ignore
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
speaker = pyttsx3.init()

# Configure Gemini API
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

genai.configure(
    api_key=GOOGLE_API_KEY
)
model = genai.GenerativeModel(
    'gemini-2.0-flash'
)

def listen_to_user():
    """Listen to microphone input and return audio."""
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Audio captured.")
            return audio
        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")
            return None

def recognize_speech(audio):
    """Convert audio to text."""
    if audio is None:
        return ""
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return ""
    except sr.RequestError as e:
        print(f"Speech Recognition API error: {e}")
        return ""

def get_gemini_response(user_text):
    """Generate a response from the Gemini API."""
    try:
        prompt = (
            f"You are a deep friendly Health Assistant. "
            f"First think and then Respond short but exact , speak with deep felling and deep emotions , dont speak any symbol and special letter to: {user_text}"
        )
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "I'm not sure how to respond."
    except Exception as e:
        print(f"Error communicating with Gemini: {e}")
        return "Sorry, something went wrong."

def speak(text):
    """Speak out the given text."""
    speaker.say(text)
    speaker.runAndWait()

def main():
    """Main loop for the voice assistant."""
    print(" Voice Health Assistant is ready!")
    print("Speak clearly. Say 'goodbye' or 'bye' to exit.\n")

    while True:
        audio = listen_to_user()
        user_text = recognize_speech(audio)
        
        if user_text:
            print(f"You said: {user_text}")
            if any(exit_word in user_text.lower() for exit_word in ["goodbye", "bye", "exit", "quit"]):
                speak("Goodbye! Take care!")
                print("Session ended.")
                break

            response = get_gemini_response(user_text)
            print(f"Assistant: {response}")
            speak(response)

if __name__ == "__main__":
    main()
    