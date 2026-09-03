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
        self.root.configure(bg="#050005")

        # Screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        q_file = os.path.join(BASE_DIR, "questions.json")
        with open(q_file, "r") as f:
            self.data = json.load(f)

        self.q_index = 0
        self.bg_photo = None
        self.border_state = False

        # Canvas acts as master layer for full-screen wallpaper + HUD overlays
        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_width,
            height=self.screen_height,
            bg="#050005",
            highlightthickness=8,
            highlightbackground="#ff003c"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.build_alarm_screen()
        self.animate_neon_pulse()

    def animate_neon_pulse(self):
        """Pulsing cyber-red neon border effect around the entire screen."""
        glow_colors = ["#ff003c", "#ff1744", "#990022", "#3a000e", "#ff1744"]
        current_color = glow_colors[int(self.border_state) % len(glow_colors)]
        self.canvas.configure(highlightbackground=current_color)
        self.border_state = (self.border_state + 1) % len(glow_colors)
        self.root.after(350, self.animate_neon_pulse)

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

    def render_fullscreen_background(self, filename):
        """Loads and stretches the sticker across the entire screen as wallpaper."""
        file_path = os.path.join(BASE_DIR, "assets", "stickers", filename)
        if not os.path.exists(file_path):
            print(f"[!] Sticker missing: {file_path}")
            return
        try:
            img = Image.open(file_path).convert("RGBA")
            img = img.resize((self.screen_width, self.screen_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
            self.canvas.delete("bg_layer")
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="bg_layer")
        except Exception as e:
            print(f"[!] Error setting background image: {e}")

    def build_alarm_screen(self):
        self.play_sound("aarada.mp3")
        self.render_fullscreen_background("sticker1.png")

        # Overlay HUD Card for Controls
        self.alarm_card = tk.Frame(
            self.canvas,
            bg="#090209",
            highlightbackground="#ff003c",
            highlightcolor="#ff003c",
            highlightthickness=3,
            padx=35,
            pady=25
        )
        
        # Banner Header inside HUD
        self.banner_lbl = tk.Label(
            self.alarm_card,
            text="⚠ SYSTEM BREACH // UNAUTHORIZED INVASION ⚠",
            font=("Impact", 15),
            fg="#ffcc00",
            bg="#090209"
        )
        self.banner_lbl.pack(pady=(0, 6))

        # Main Title
        self.header_label = tk.Label(
            self.alarm_card,
            text="AARAADAAA?!",
            font=("Impact", 42),
            fg="#ff003c",
            bg="#090209"
        )
        self.header_label.pack(pady=4)

        # Dialogue
        self.bubble = tk.Label(
            self.alarm_card,
            text="Ente lap-il thottu kalikkunnoda neee?!\nPIN para da!",
            font=("Consolas", 15, "bold"),
            fg="#00ffff",
            bg="#160319",
            padx=20,
            pady=10,
            relief=tk.RIDGE,
            bd=2,
            highlightbackground="#ff0055",
            highlightthickness=1,
            justify=tk.CENTER
        )
        self.bubble.pack(pady=10)

        # PIN Entry sub-frame
        pin_frame = tk.Frame(self.alarm_card, bg="#090209")
        pin_frame.pack(pady=10)

        self.sub_label = tk.Label(
            pin_frame,
            text="ENTER ACCESS PIN",
            font=("Consolas", 11, "bold"),
            fg="#ff0055",
            bg="#090209"
        )
        self.sub_label.pack(pady=(0, 5))

        self.pin_entry = tk.Entry(
            pin_frame,
            show="●",
            font=("Consolas", 24, "bold"),
            justify="center",
            width=10,
            bg="#000000",
            fg="#ffea00",
            insertbackground="#00ffff",
            relief=tk.FLAT,
            highlightbackground="#ff003c",
            highlightthickness=2
        )
        self.pin_entry.pack(pady=6)
        self.pin_entry.focus()
        self.pin_entry.bind("<Return>", lambda event: self.verify_pin())

        self.submit_btn = tk.Button(
            pin_frame,
            text="VERIFY PIN",
            font=("Impact", 14),
            bg="#ff003c",
            fg="#ffffff",
            activebackground="#ff3366",
            activeforeground="#ffffff",
            cursor="hand2",
            padx=25,
            pady=5,
            bd=0,
            command=self.verify_pin
        )
        self.submit_btn.pack(pady=10)

        # Center the HUD card on top of the full-screen sticker
        self.hud_window = self.canvas.create_window(
            self.screen_width // 2,
            self.screen_height // 2,
            window=self.alarm_card,
            tags="hud_card"
        )

    def verify_pin(self):
        entered_pin = self.pin_entry.get().strip()
        correct_pin = str(self.data.get("pin", "")).strip()

        if entered_pin == correct_pin:
            self.start_questions()
        else:
            self.pin_entry.delete(0, tk.END)

            # Swap full-screen wallpaper to sticker2 on failed attempt
            self.render_fullscreen_background("sticker2.png")

            self.header_label.config(text="WRONG PIN! AARAADA NEE?!", fg="#ff0000")
            self.bubble.config(
                text="PIN polum ariyilla!\nNee aaraada naaye?! Police-ine vilikkum!",
                fg="#ff3366",
                bg="#26000d"
            )
            self.sub_label.config(text="INVALID PIN - TRY AGAIN!", fg="#ff1744")
            self.play_sound("siren.mp3")

    def start_questions(self):
        pygame.mixer.stop()
        self.canvas.delete("hud_card")

        # Questions HUD Container
        self.q_card = tk.Frame(
            self.canvas,
            bg="#090209",
            highlightbackground="#00ffcc",
            highlightcolor="#00ffcc",
            highlightthickness=3,
            padx=45,
            pady=30
        )

        header = tk.Label(
            self.q_card,
            text="PIN ACCEPTED // PROVE FRIENDSHIP PROTOCOL",
            font=("Impact", 22),
            fg="#00ffcc",
            bg="#090209"
        )
        header.pack(pady=(0, 20))

        self.q_label = tk.Label(
            self.q_card,
            text="",
            font=("Consolas", 16, "bold"),
            fg="#ffea00",
            bg="#160319",
            wraplength=600,
            justify=tk.CENTER,
            padx=20,
            pady=15,
            relief=tk.RIDGE,
            bd=2
        )
        self.q_label.pack(pady=10)

        self.ans_entry = tk.Entry(
            self.q_card,
            font=("Consolas", 18),
            justify="center",
            width=26,
            bg="#000000",
            fg="#00ffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            highlightbackground="#00ffcc",
            highlightthickness=2
        )
        self.ans_entry.pack(pady=15)
        self.ans_entry.focus()
        self.ans_entry.bind("<Return>", lambda event: self.check_answer())

        self.q_btn = tk.Button(
            self.q_card,
            text="AUTHENTICATE",
            font=("Impact", 14),
            bg="#00ffcc",
            fg="#090209",
            activebackground="#66ffee",
            activeforeground="#090209",
            cursor="hand2",
            padx=30,
            pady=5,
            bd=0,
            command=self.check_answer
        )
        self.q_btn.pack(pady=10)

        self.status_msg = tk.Label(
            self.q_card,
            text="Answer accurately to unlock the system.",
            font=("Consolas", 11, "bold"),
            fg="#8888aa",
            bg="#090209"
        )
        self.status_msg.pack(pady=(10, 0))

        # Re-center Questions card on screen
        self.canvas.create_window(
            self.screen_width // 2,
            self.screen_height // 2,
            window=self.q_card,
            tags="hud_card"
        )

        self.show_next_question()

    def show_next_question(self):
        questions = self.data.get("questions", [])
        if self.q_index < len(questions):
            q = questions[self.q_index]["q"]
            self.q_label.config(text=f"QUESTION {self.q_index + 1}:\n{q}")
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
            self.status_msg.config(text="WRONG ANSWER! FRIENDSHIP PROTOCOL FAILED!", fg="#ff1744")
            # Checks for both failed.mp3 and failure.mp3 automatically
            fail_sound = "failed.mp3" if os.path.exists(os.path.join(BASE_DIR, "assets", "audio", "failed.mp3")) else "failure.mp3"
            self.play_sound(fail_sound)
