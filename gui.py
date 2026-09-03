import os
import json
import tkinter as tk
from PIL import Image, ImageTk
import pygame

# Initialize audio mixer
try:
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
except Exception as e:
    print(f"[!] Audio init error: {e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class IntruderScreen:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("AARAADA?!")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#0a0a12")

        q_file = os.path.join(BASE_DIR, "questions.json")
        with open(q_file, "r") as f:
            self.data = json.load(f)

        self.q_index = 0
        self.current_photo = None

        self.build_alarm_screen()

    def play_sound(self, filename):
        file_path = os.path.join(BASE_DIR, "assets", "audio", filename)
        if not os.path.exists(file_path):
            print(f"[!] Audio missing: {file_path}")
            return
        try:
            pygame.mixer.stop()
            sound = pygame.mixer.Sound(file_path)
            sound.play()
            print(f"[*] Playing sound: {filename}")
        except Exception as e:
            print(f"[!] Audio playback error: {e}")

    def load_image(self, filename, size=(240, 240)):
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
        # 1. Play dialogue on face failure
        self.play_sound("aarada.mp3")

        # Top Warning Banner (Only for alarm screen)
        self.banner = tk.Label(
            self.root,
            text="🚨 UNAUTHORIZED LAPTOP INVASION DETECTED 🚨",
            font=("Impact", 18),
            fg="#0a0a12",
            bg="#ffcc00",
            pady=6
        )
        self.banner.pack(fill=tk.X)

        # Title Header
        self.header_label = tk.Label(
            self.root,
            text="AARAADAAA?!",
            font=("Impact", 44),
            fg="#ff1744",
            bg="#0a0a12"
        )
        self.header_label.pack(pady=(10, 5))

        # 1. Sticker on Top
        self.sticker_label = tk.Label(self.root, bg="#0a0a12")
        self.current_photo = self.load_image("sticker1.png")
        if self.current_photo:
            self.sticker_label.config(image=self.current_photo)
        self.sticker_label.pack(pady=5)

        # 2. Dialogue Directly Below Sticker
        self.bubble = tk.Label(
            self.root,
            text="Ente lap-il thottu kalikkunnoda neee?!\nPIN para da!",
            font=("Arial Black", 16),
            fg="#00e5ff",
            bg="#1b1b2f",
            padx=25,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
            highlightbackground="#ff0055",
            highlightthickness=2,
            justify=tk.CENTER
        )
        self.bubble.pack(pady=10)

        # 3. PIN & Answer Portion Directly Below Dialogue
        card = tk.Frame(self.root, bg="#121224", padx=25, pady=12, relief=tk.GROOVE, bd=3)
        card.pack(pady=10)

        self.sub_label = tk.Label(
            card,
            text="ENTER LAPTOP PIN",
            font=("Arial", 12, "bold"),
            fg="#00ffcc",
            bg="#121224"
        )
        self.sub_label.pack(pady=(0, 6))

        self.pin_entry = tk.Entry(
            card,
            show="●",
            font=("Consolas", 22, "bold"),
            justify="center",
            width=10,
            bg="#05050d",
            fg="#ffea00",
            insertbackground="white",
            relief=tk.SUNKEN,
            bd=2
        )
        self.pin_entry.pack(pady=4)
        self.pin_entry.focus()
        self.pin_entry.bind("<Return>", lambda event: self.verify_pin())

        self.submit_btn = tk.Button(
            card,
            text="SUBMIT PIN",
            font=("Impact", 13),
            bg="#ff0055",
            fg="white",
            activebackground="#ff3377",
            activeforeground="white",
            cursor="hand2",
            padx=20,
            pady=4,
            command=self.verify_pin
        )
        self.submit_btn.pack(pady=(10, 4))

    def verify_pin(self):
        entered_pin = self.pin_entry.get().strip()
        correct_pin = str(self.data.get("pin", "")).strip()

        if entered_pin == correct_pin:
            self.start_questions()
        else:
            self.pin_entry.delete(0, tk.END)

            # Swap to sticker2.png on wrong PIN
            new_sticker = self.load_image("sticker2.png")
            if new_sticker:
                self.current_photo = new_sticker
                self.sticker_label.config(image=self.current_photo)

            self.header_label.config(text="WRONG PIN! AARAADA NEE?!", fg="#ff0000")
            self.bubble.config(
                text="PIN polum ariyilla!\nNee aaraada naaye?! Police-ine vilikkum!",
                fg="#ff3366",
                bg="#2a0815"
            )
            self.sub_label.config(text="INVALID PIN - TRY AGAIN!", fg="#ff1744")

            # Play siren on wrong PIN
            self.play_sound("siren.mp3")

    def start_questions(self):
        pygame.mixer.stop()
        for widget in self.root.winfo_children():
            widget.destroy()

        # No yellow band here — clean dark theme
        header = tk.Label(
            self.root,
            text="PIN ACCEPTED ✓ PROVE YOUR FRIENDSHIP",
            font=("Impact", 28),
            fg="#00e676",
            bg="#0a0a12",
            pady=25
        )
        header.pack(fill=tk.X)

        # Question Board Card
        q_card = tk.Frame(self.root, bg="#1a1a2e", padx=40, pady=30, relief=tk.RIDGE, bd=4)
        q_card.pack(pady=20)

        self.q_label = tk.Label(
            q_card,
            text="",
            font=("Arial Black", 18),
            fg="#ffea00",
            bg="#1a1a2e",
            wraplength=650,
            justify=tk.CENTER
        )
        self.q_label.pack(pady=(0, 20))

        self.ans_entry = tk.Entry(
            q_card,
            font=("Arial", 18),
            justify="center",
            width=24,
            bg="#0f0f1d",
            fg="#00e5ff",
            insertbackground="white",
            relief=tk.SUNKEN,
            bd=3
        )
        self.ans_entry.pack(pady=10)
        self.ans_entry.focus()
        self.ans_entry.bind("<Return>", lambda event: self.check_answer())

        self.q_btn = tk.Button(
            q_card,
            text="VERIFY ANSWER",
            font=("Impact", 14),
            bg="#00e676",
            fg="#0a0a12",
            activebackground="#69f0ae",
            activeforeground="#0a0a12",
            cursor="hand2",
            padx=25,
            pady=5,
            command=self.check_answer
        )
        self.q_btn.pack(pady=15)

        self.status_msg = tk.Label(
            self.root,
            text="Answer correctly to bypass lockdown.",
            font=("Arial", 13, "bold"),
            fg="#8888aa",
            bg="#0a0a12"
        )
        self.status_msg.pack(pady=10)

        self.show_next_question()

    def show_next_question(self):
        questions = self.data.get("questions", [])
        if self.q_index < len(questions):
            q = questions[self.q_index]["q"]
            self.q_label.config(text=f"Question {self.q_index + 1}:\n{q}")
            self.status_msg.config(text=f"Progress: {self.q_index}/{len(questions)} verified", fg="#00e5ff")
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
            # Play failed.mp3 when a personal question mistake is made
            self.status_msg.config(text="WRONG ANSWER! FRIENDSHIP PROTOCOL FAILED!", fg="#ff1744")
            self.play_sound("failure.mp3")
