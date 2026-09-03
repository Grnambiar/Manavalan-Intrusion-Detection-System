import os
import tkinter as tk
from PIL import Image, ImageTk
import pygame
import json

# Initialize mixer with standard frequency
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class IntruderScreen:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("AARAADA?!")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        q_file = os.path.join(BASE_DIR, "questions.json")
        with open(q_file, "r") as f:
            self.data = json.load(f)

        self.q_index = 0
        self.active_channel = None
        self.build_alarm_screen()

    def play_sound(self, filename):
        file_path = os.path.join(BASE_DIR, "assets", "audio", filename)
        if not os.path.exists(file_path):
            print(f"[!] Audio missing: {file_path}")
            return
        try:
            sound = pygame.mixer.Sound(file_path)
            self.active_channel = sound.play()
            print(f"[*] Playing sound: {filename}")
        except Exception as e:
            print(f"[!] Audio playback error: {e}")

    def load_image(self, filename, size=(220, 220)):
        file_path = os.path.join(BASE_DIR, "assets", "stickers", filename)
        if not os.path.exists(file_path):
            print(f"[!] Sticker missing: {file_path}")
            return None
        try:
            img = Image.open(file_path).convert("RGBA")
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"[!] Error loading {filename}: {e}")
            return None

    def build_alarm_screen(self):
        # 1. Play Dialogue Audio
        self.play_sound("aarada.mp3")

        # Title
        self.label = tk.Label(self.root, text="AARAADAAA?!", font=("Impact", 44), fg="red", bg="black")
        self.label.pack(pady=15)

        # 2. Sticker row: Sticker 1 - Dialogue Text - Sticker 2
        sticker_frame = tk.Frame(self.root, bg="black")
        sticker_frame.pack(pady=10)

        self.photo1 = self.load_image("sticker1.png", size=(220, 220))
        if self.photo1:
            lbl1 = tk.Label(sticker_frame, image=self.photo1, bg="black")
            lbl1.image = self.photo1
            lbl1.pack(side=tk.LEFT, padx=15)

        dialogue_box = tk.Label(
            sticker_frame,
            text="Ente lap il thott\nkalikkunnoda?!",
            font=("Arial", 22, "bold"),
            fg="yellow",
            bg="#181818",
            padx=20,
            pady=15,
            relief=tk.RAISED
        )
        dialogue_box.pack(side=tk.LEFT, padx=15)

        self.photo2 = self.load_image("sticker2.png", size=(220, 220))
        if self.photo2:
            lbl2 = tk.Label(sticker_frame, image=self.photo2, bg="black")
            lbl2.image = self.photo2
            lbl2.pack(side=tk.LEFT, padx=15)

        self.sub_label = tk.Label(self.root, text="UNAUTHORIZED ACCESS DETECTED!", font=("Arial", 16, "bold"), fg="#ff3333", bg="black")
        self.sub_label.pack(pady=10)

        # PIN Entry
        self.pin_entry = tk.Entry(self.root, show="*", font=("Arial", 20), justify="center", width=12)
        self.pin_entry.pack(pady=10)
        self.pin_entry.focus()

        self.submit_btn = tk.Button(self.root, text="SUBMIT PIN", font=("Arial", 13, "bold"), bg="#222", fg="#00ff66", command=self.verify_pin)
        self.submit_btn.pack(pady=10)

    def verify_pin(self):
        entered_pin = self.pin_entry.get().strip()
        correct_pin = str(self.data.get("pin", "")).strip()

        if entered_pin == correct_pin:
            self.start_questions()
        else:
            self.label.config(text="WRONG PIN! AARAADA NEE?")
            self.play_sound("siren.mp3")
            self.pin_entry.delete(0, tk.END)

    def start_questions(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.q_label = tk.Label(self.root, text="", font=("Arial", 22, "bold"), fg="white", bg="black")
        self.q_label.pack(pady=40)

        self.ans_entry = tk.Entry(self.root, font=("Arial", 18), justify="center", width=25)
        self.ans_entry.pack(pady=10)
        self.ans_entry.focus()

        self.q_btn = tk.Button(self.root, text="Submit Answer", font=("Arial", 14), bg="#222", fg="#00ff66", command=self.check_answer)
        self.q_btn.pack(pady=10)

        self.show_next_question()

    def show_next_question(self):
        questions = self.data.get("questions", [])
        if self.q_index < len(questions):
            q = questions[self.q_index]["q"]
            self.q_label.config(text=f"Question {self.q_index + 1}: {q}")
            self.ans_entry.delete(0, tk.END)
        else:
            self.root.destroy()
            self.on_success()

    def check_answer(self):
        user_ans = self.ans_entry.get().strip().lower()
        valid_answers = [a.lower() for a in self.data["questions"][self.q_index]["answers"]]

        if user_ans in valid_answers:
            self.q_index += 1
            self.show_next_question()
        else:
            self.q_label.config(text="FRIENDSHIP FAILED! WHO ARE YOU?", fg="red")
            self.play_sound("failure.mp3")
