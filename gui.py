import tkinter as tk
from PIL import Image, ImageTk
import pygame
import json

pygame.mixer.init()

class IntruderScreen:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("AARAADA?!")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        with open("questions.json", "r") as f:
            self.data = json.load(f)

        self.q_index = 0
        self.build_alarm_screen()

    def play_sound(self, sound_path):
        try:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except:
            pass

    def build_alarm_screen(self):
        self.play_sound("assets/aaraada.mp3")

        self.label = tk.Label(self.root, text="AARAADAAA?!", font=("Impact", 45), fg="red", bg="black")
        self.label.pack(pady=20)

        # Load sticker
        try:
            img = Image.open("assets/manavalan.png").resize((300, 300))
            self.photo = ImageTk.PhotoImage(img)
            self.img_label = tk.Label(self.root, image=self.photo, bg="black")
            self.img_label.pack(pady=10)
        except:
            pass

        self.sub_label = tk.Label(self.root, text="UNAUTHORIZED ACCESS DETECTED!", font=("Arial", 18), fg="yellow", bg="black")
        self.sub_label.pack(pady=10)

        # PIN input
        self.pin_entry = tk.Entry(self.root, show="*", font=("Arial", 20), justify="center")
        self.pin_entry.pack(pady=10)
        self.pin_entry.focus()

        self.submit_btn = tk.Button(self.root, text="SUBMIT PIN", font=("Arial", 14), command=self.verify_pin)
        self.submit_btn.pack(pady=10)

    def verify_pin(self):
        if self.pin_entry.get() == self.data["pin"]:
            self.start_questions()
        else:
            self.label.config(text="WRONG PIN! AARAADA NEE?")
            self.play_sound("assets/siren.mp3")
            self.pin_entry.delete(0, tk.END)

    def start_questions(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.q_label = tk.Label(self.root, text="", font=("Arial", 22), fg="white", bg="black")
        self.q_label.pack(pady=40)

        self.ans_entry = tk.Entry(self.root, font=("Arial", 18), justify="center")
        self.ans_entry.pack(pady=10)
        self.ans_entry.focus()

        self.q_btn = tk.Button(self.root, text="Next", font=("Arial", 14), command=self.check_answer)
        self.q_btn.pack(pady=10)

        self.show_next_question()

    def show_next_question(self):
        if self.q_index < len(self.data["questions"]):
            q = self.data["questions"][self.q_index]["q"]
            self.q_label.config(text=f"Question {self.q_index + 1}: {q}")
            self.ans_entry.delete(0, tk.END)
        else:
            self.root.destroy()
            self.on_success()

    def check_answer(self):
        user_ans = self.ans_entry.get().strip().lower()
        valid_answers = self.data["questions"][self.q_index]["answers"]

        if user_ans in valid_answers:
            self.q_index += 1
            self.show_next_question()
        else:
            self.q_label.config(text="FRIENDSHIP FAILED! WHO ARE YOU?", fg="red")
            self.play_sound("assets/siren.mp3")
