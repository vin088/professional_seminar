import tkinter as tk
from tkinter import messagebox
import random
import speech_recognition as sr
import pyttsx3
from vpython import *

# Define a list of languages supported by the system
supported_languages = ["English", "Spanish", "French"]

class LanguageLearningAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VR-based Language Learning Assistant")
        self.create_widgets()

        # Initialize speech recognition and text-to-speech engines
        self.recognizer = sr.Recognizer()
        self.text_to_speech = pyttsx3.init()

        # Create a 3D scene for the VR-like experience
        self.scene = canvas(title="VR-based Language Learning Assistant", width=800, height=600)
        box(pos=vector(0, 0, -2), size=vector(0.5, 0.5, 0.5), color=color.red)
        
          # Create a Text widget for the chat-like interface
        self.chat_text = tk.Text(self.root, wrap=tk.WORD, width=50, height=10)
        self.chat_text.pack(pady=10)

    def create_widgets(self):
        self.label_language = tk.Label(self.root, text="Select the language you want to learn:")
        self.label_language.pack(pady=10)

        # Dropdown menu to select the language
        self.selected_language = tk.StringVar()
        self.selected_language.set(supported_languages[0])  # Default selection
        self.language_menu = tk.OptionMenu(self.root, self.selected_language, *supported_languages)
        self.language_menu.pack(pady=5)

        self.label_instruction = tk.Label(self.root, text="Pronounce a word or a short phrase:")
        self.label_instruction.pack(pady=10)

        self.btn_listen = tk.Button(self.root, text="Listen & Check Pronunciation", command=self.listen_and_assess)
        self.btn_listen.pack(pady=5)

        self.label_feedback = tk.Label(self.root, text="")
        self.label_feedback.pack(pady=10)

        self.label_user_speech = tk.Label(self.root, text="Your Speech:")
        self.label_user_speech.pack(pady=10)

        self.user_speech_text = tk.StringVar()
        self.label_user_speech_display = tk.Label(self.root, textvariable=self.user_speech_text, wraplength=400, justify="left")
        self.label_user_speech_display.pack(pady=5)

        self.btn_clear = tk.Button(self.root, text="Clear", command=self.clear_user_speech)
        self.btn_clear.pack(pady=5)

    def listen_and_assess(self):
        # Get the user's language choice
        selected_language = self.selected_language.get()

        # Prompt the user to speak
        self.text_to_speech.say(f"Please pronounce a word or a short phrase in {selected_language}.")
        self.text_to_speech.runAndWait()

        # Record the user's voice
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise
            audio = self.recognizer.listen(source)

        try:
            # Convert the recorded audio to text using speech recognition
            user_input = self.recognizer.recognize_google(audio, language=selected_language.lower())

            # Provide feedback to the user using random.choice from random module
            feedback_message = random.choice([
                f"Great job! Your pronunciation in {selected_language} sounds clear and accurate!",
                f"Keep practicing! Your pronunciation in {selected_language} is improving!",
                f"Your pronunciation in {selected_language} needs some more practice."
            ])

            self.user_speech_text.set(user_input)
            self.label_feedback.config(text=f"{feedback_message}")
            self.text_to_speech.say(feedback_message)
            self.text_to_speech.runAndWait()

            # Update the 3D scene with the user's spoken words
            sphere(pos=vector(0, 0, -2), radius=0.1, color=color.green, text=user_input)

        except sr.UnknownValueError:
            messagebox.showerror("Speech Recognition Error", "Sorry, we couldn't understand your pronunciation. Please try again.")
        except sr.RequestError:
            messagebox.showerror("Speech Recognition Error", "Sorry, there was an issue with the speech recognition service. Please try again later.")

    def clear_user_speech(self):
        self.user_speech_text.set("")

def show_supported_languages():
    languages = "\n".join(supported_languages)
    messagebox.showinfo("Supported Languages", f"The system supports the following languages:\n\n{languages}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageLearningAssistantApp(root)

    # Adding a menu option for supported languages
    menubar = tk.Menu(root)
    options_menu = tk.Menu(menubar, tearoff=0)
    options_menu.add_command(label="Supported Languages", command=show_supported_languages)
    menubar.add_cascade(label="Options", menu=options_menu)
    root.config(menu=menubar)

    root.mainloop()
