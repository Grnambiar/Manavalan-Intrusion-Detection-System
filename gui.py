import os
import json
import tkinter as tk
from PIL import Image, ImageTk
import pygame

# Initialize pygame mixer with standard audio settings
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except Exception as e:
    print(f"[AUDIO INIT ERROR] {e}")

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

    def play_sound(self, rel_path):
        full_path = os.path.abspath(rel_path)
        print(f"[DEBUG] Attempting to play sound from: {full_path}")
        if not os.path.exists(full_path):
            print(f"[ERROR] Audio file does not exist: {full_path}")
            return
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"[AUDIO PLAY ERROR] {e}")

    def build_alarm_screen(self):
        # 1. Play dialogue
        self.play_sound(os.path.join("assets", "audio", "aarada.mp3"))

        self.label = tk.Label(self.root, text="AARAADAAA?!", font=("Impact", 45), fg="red", bg="black")
        self.label.pack(pady=20)

        # 2. Find sticker image in assets/stickers/
        sticker_folder = os.path.join("assets", "stickers")
        img_path = None
        if os.path.exists(sticker_folder):
            files = [f for f in os.listdir(sticker_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if files:
                img_path = os.path.join(sticker_folder, files[0])

        if img_path and os.path.exists(img_path):
            print(f"[DEBUG] Loading sticker from: {img_path}")
            try:
                raw_img = Image.open(img_path).convert("RGBA")
                raw_img = raw_img.resize((300, 300))
                # Store photo on self so Python garbage collector does not delete it
                self.photo = ImageTk.PhotoImage(raw_img)
                self.img_label = tk.Label(self.root, image=self.photo, bg="black")
                self.img_label.pack(pady=10)
            except Exception as e:
                print(f"[IMAGE LOAD ERROR] {e}")
        else:
            print(f"[ERROR] No valid image file found in {os.path.abspath(sticker_folder)}")

        self.sub_label = tk.Label(self.root, text="UNAUTHORIZED ACCESS DETECTED!", font=("Arial", 18), fg="yellow", bg="black")
        self.sub_label.pack(pady=10)

        # PIN input
        self.pin_entry = tk.Entry(self.root, show="*", font=("Arial", 20), justify="center")
        self.pin_entry.pack(pady=10)
        self.pin_entry.focus()

        self.submit_btn = tk.Button(self.root, text="SUBMIT PIN", font=("Arial", 14), command=self.verify_pin)
        self.submit_btn.pack(pady=10)

    def verify_pin(self):
        entered_pin = self.pin_entry.get().strip()
        if entered_pin == str(self.data.get("pin", "1234")):
            self.start_questions()
        else:
            self.label.config(text="WRONG PIN! AARAADA NEE?")
            self.play_sound(os.path.join("assets", "audio", "siren.mp3"))
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
        if self.q_index < len(self.data.get("questions", [])):
            q = self.data["questions"][self.q_index]["q"]
            self.q_label.config(text=f"Question {self.q_index + 1}: {q}", fg="white")
            self.ans_entry.delete(0, tk.END)
        else:
            self.root.destroy()
            self.on_success()

    def check_answer(self):
        user_ans = self.ans_entry.get().strip().lower()
        valid_answers = [str(a).strip().lower() for a in self.data["questions"][self.q_index].get("answers", [])]

        if user_ans in valid_answers:
            self.q_index += 1
            self.show_next_question()
        else:
            self.q_label.config(text="FRIENDSHIP FAILED! WHO ARE YOU?", fg="red")
            self.play_sound(os.path.join("assets", "audio", "failed.mp3"))
