import openai
import pyttsx3
import speech_recognition as sr
import time
from dotenv import load_dotenv
import os
import sounddevice

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def transcribe_audio_to_text(filename):
    recogniser = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio = recogniser.record(source)
    try:
        return recogniser.recognize_google(audio)
    except:
        print("Skipping unknown error")


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=4000,
        n=1,
        stop=None,
    )
    return response["choices"][0]["text"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        print("Say 'genius' to start recording your question")
        with sr.Microphone() as source:
            try:
                recognizer = sr.Recognizer()
                recognizer.energy_threshold = 150
                recognizer.dynamic_energy_threshold = True
                audio = recognizer.listen(source)
                transcription = recognizer.recognize_google(audio,  language = 'en-US')
                if transcription.lower() == "genius":
                    # Record audio
                    filename = "input.wav"
                    print("Say your question")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 5
                        audio = recognizer.listen(source)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        # Generate response using GPT-3
                        response = generate_response(text)
                        print(f"Genious: {response}")

                        # Speak response using text-to-speech
                        speak_text(response)
            except Exception as e:
                print(f"Error Occured: {e}")

if __name__ == "__main__":
    main()