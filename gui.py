import os
import json
import random
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

# Dynamic neon palette
NEON_COLORS = [
    "#ff0055", "#00ffff", "#ffea00", "#76ff03", 
    "#d500f9", "#ff3d00", "#00e5ff", "#ff007f"
]

class IntruderScreen:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("AARAADA?! - CYBER LOCKDOWN")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#040008")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        q_file = os.path.join(BASE_DIR, "questions.json")
        with open(q_file, "r") as f:
            self.data = json.load(f)

        self.q_index = 0
        self.color_cycle_idx = 0
        self.grid_offset = 0

        # Flying sticker state variables
        self.sticker_photo = None
        self.sticker_w = 260
        self.sticker_h = 260
        self.sticker_x = random.randint(60, max(70, self.screen_width - self.sticker_w - 60))
        self.sticker_y = random.randint(60, max(70, self.screen_height - self.sticker_h - 60))
        self.vx = random.choice([-10, -8, 8, 10])
        self.vy = random.choice([-9, -7, 7, 9])

        # Interactive Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_width,
            height=self.screen_height,
            bg="#030007",
            highlightthickness=8,
            highlightbackground="#ff0055"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Generate floating cyber particles
        self.particles = []
        for _ in range(40):
            self.particles.append({
                "x": random.randint(0, self.screen_width),
                "y": random.randint(0, self.screen_height),
                "size": random.randint(2, 5),
                "speed": random.uniform(1.5, 4.0),
                "color": random.choice(NEON_COLORS)
            })

        self.load_flying_sticker("sticker1.png")
        self.build_alarm_screen()
        
        # Start Animation Engines
        self.animate_scene()

    def load_flying_sticker(self, filename):
        file_path = os.path.join(BASE_DIR, "assets", "stickers", filename)
        if not os.path.exists(file_path):
            print(f"[!] Sticker missing: {file_path}")
            return
        try:
            img = Image.open(file_path).convert("RGBA")
            img = img.resize((self.sticker_w, self.sticker_h), Image.Resampling.LANCZOS)
            self.sticker_photo = ImageTk.PhotoImage(img)
            self.canvas.delete("flying_sticker")
            self.canvas.create_image(
                self.sticker_x,
                self.sticker_y,
                image=self.sticker_photo,
                anchor="nw",
                tags="flying_sticker"
            )
        except Exception as e:
            print(f"[!] Error loading flying sticker: {e}")

    def animate_scene(self):
        """Unified 30 FPS Render Loop for Matrix Grid, Particles, and Sticker."""
        self.canvas.delete("grid_line")
        self.canvas.delete("particle")
        self.canvas.delete("sticker_aura")

        # 1. Perspective Matrix Grid Floor
        self.grid_offset = (self.grid_offset + 3) % 40
        horizon = int(self.screen_height * 0.45)

        for y in range(horizon, self.screen_height, 40):
            draw_y = y + self.grid_offset
            if draw_y < self.screen_height:
                self.canvas.create_line(
                    0, draw_y, self.screen_width, draw_y,
                    fill="#150528", width=1, tags="grid_line"
                )

        # Radial Perspective Lines
        cx = self.screen_width // 2
        for x in range(0, self.screen_width + 100, 120):
            self.canvas.create_line(
                cx, horizon, x, self.screen_height,
                fill="#1c0736", width=1, tags="grid_line"
            )

        # 2. Drifting Neon Cyber-Sparks
        for p in self.particles:
            p["y"] -= p["speed"]
            if p["y"] < 0:
                p["y"] = self.screen_height
                p["x"] = random.randint(0, self.screen_width)

            self.canvas.create_oval(
                p["x"], p["y"], p["x"] + p["size"], p["y"] + p["size"],
                fill=p["color"], outline="", tags="particle"
            )

        # 3. Holographic Aura behind the Bouncing Sticker
        aura_padding = 20
        self.canvas.create_oval(
            self.sticker_x - aura_padding,
            self.sticker_y - aura_padding,
            self.sticker_x + self.sticker_w + aura_padding,
            self.sticker_y + self.sticker_h + aura_padding,
            outline=NEON_COLORS[self.color_cycle_idx % len(NEON_COLORS)],
            width=3,
            tags="sticker_aura"
        )

        # 4. Update Bouncing Physics
        self.sticker_x += self.vx
        self.sticker_y += self.vy

        if self.sticker_x <= 10:
            self.sticker_x = 10
            self.vx = abs(self.vx)
        elif self.sticker_x + self.sticker_w >= self.screen_width - 10:
            self.sticker_x = self.screen_width - self.sticker_w - 10
            self.vx = -abs(self.vx)

        if self.sticker_y <= 10:
            self.sticker_y = 10
            self.vy = abs(self.vy)
        elif self.sticker_y + self.sticker_h >= self.screen_height - 10:
            self.sticker_y = self.screen_height - self.sticker_h - 10
            self.vy = -abs(self.vy)

        self.canvas.coords("flying_sticker", self.sticker_x, self.sticker_y)

        # Ensure Layer Order: Grid -> Particles -> Aura -> Sticker -> HUD
        self.canvas.tag_lower("sticker_aura")
        self.canvas.tag_lower("particle")
        self.canvas.tag_lower("grid_line")
        self.canvas.tag_raise("flying_sticker")
        self.canvas.tag_raise("hud_card")

        # 5. Cycle Neon RGB Border
        active_color = NEON_COLORS[self.color_cycle_idx % len(NEON_COLORS)]
        self.canvas.configure(highlightbackground=active_color)
        if hasattr(self, "alarm_card") and self.alarm_card.winfo_exists():
            self.alarm_card.configure(highlightbackground=active_color)

        self.color_cycle_idx += 1
        self.root.after(33, self.animate_scene)

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

    def build_alarm_screen(self):
        self.play_sound("aarada.mp3")

        # Futuristic HUD Card
        self.alarm_card = tk.Frame(
            self.canvas,
            bg="#0d0214",
            highlightbackground="#ff0055",
            highlightcolor="#00ffff",
            highlightthickness=4,
            padx=45,
            pady=30
        )

        self.banner_lbl = tk.Label(
            self.alarm_card,
            text="⚡ NEURAL LOCK // UNAUTHORIZED INVASION ⚡",
            font=("Impact", 16),
            fg="#ffea00",
            bg="#0d0214"
        )
        self.banner_lbl.pack(pady=(0, 6))

        self.header_label = tk.Label(
            self.alarm_card,
            text="AARAADAAA?!",
            font=("Impact", 46),
            fg="#ff0055",
            bg="#0d0214"
        )
        self.header_label.pack(pady=4)

        self.bubble = tk.Label(
            self.alarm_card,
            text="Ente lap-il thottu kalikkunnoda neee?!\nPIN para da!",
            font=("Consolas", 15, "bold"),
            fg="#00ffff",
            bg="#180426",
            padx=25,
            pady=12,
            relief=tk.RIDGE,
            bd=2,
            highlightbackground="#ff007f",
            highlightthickness=1,
            justify=tk.CENTER
        )
        self.bubble.pack(pady=12)

        pin_frame = tk.Frame(self.alarm_card, bg="#0d0214")
        pin_frame.pack(pady=10)

        self.sub_label = tk.Label(
            pin_frame,
            text="ENTER ENCRYPTED PIN",
            font=("Consolas", 11, "bold"),
            fg="#76ff03",
            bg="#0d0214"
        )
        self.sub_label.pack(pady=(0, 5))

        self.pin_entry = tk.Entry(
            pin_frame,
            show="●",
            font=("Consolas", 24, "bold"),
            justify="center",
            width=12,
            bg="#000000",
            fg="#ffea00",
            insertbackground="#00ffff",
            relief=tk.FLAT,
            highlightbackground="#00ffff",
            highlightthickness=2
        )
        self.pin_entry.pack(pady=6)
        self.pin_entry.focus()
        self.pin_entry.bind("<Return>", lambda event: self.verify_pin())

        self.submit_btn = tk.Button(
            pin_frame,
            text="OVERRIDE SYSTEM",
            font=("Impact", 15),
            bg="#ff0055",
            fg="#ffffff",
            activebackground="#00ffff",
            activeforeground="#000000",
            cursor="hand2",
            padx=30,
            pady=6,
            bd=0,
            command=self.verify_pin
        )
        self.submit_btn.pack(pady=10)

        self.canvas.create_window(
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

            # Swap to sticker 2 and boost speed
            self.load_flying_sticker("sticker2.png")
            self.vx = 16 if self.vx > 0 else -16
            self.vy = 14 if self.vy > 0 else -14

            self.header_label.config(text="WRONG PIN! POLICE VILIKKUM!", fg="#ff0000")
            self.bubble.config(
                text="PIN polum ariyilla!\nNee aaraada naaye?! Friendship terminated!",
                fg="#ff0055",
                bg="#260010"
            )
            self.sub_label.config(text="ACCESS DENIED // RETRY", fg="#ff0000")
            self.play_sound("siren.mp3")

    def start_questions(self):
        pygame.mixer.stop()
        self.canvas.delete("hud_card")

        self.q_card = tk.Frame(
            self.canvas,
            bg="#090014",
            highlightbackground="#00ffea",
            highlightcolor="#ffea00",
            highlightthickness=4,
            padx=45,
            pady=30
        )

        header = tk.Label(
            self.q_card,
            text="PIN ACCEPTED // INITIATE FRIENDSHIP MATRIX",
            font=("Impact", 22),
            fg="#00ffea",
            bg="#090014"
        )
        header.pack(pady=(0, 20))

        self.q_label = tk.Label(
            self.q_card,
            text="",
            font=("Consolas", 16, "bold"),
            fg="#ffea00",
            bg="#18042b",
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
            fg="#00e5ff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            highlightbackground="#00ffea",
            highlightthickness=2
        )
        self.ans_entry.pack(pady=15)
        self.ans_entry.focus()
        self.ans_entry.bind("<Return>", lambda event: self.check_answer())

        self.q_btn = tk.Button(
            self.q_card,
            text="TRANSMIT ANSWER",
            font=("Impact", 14),
            bg="#00ffea",
            fg="#090014",
            activebackground="#ffea00",
            activeforeground="#000000",
            cursor="hand2",
            padx=30,
            pady=5,
            bd=0,
            command=self.check_answer
        )
        self.q_btn.pack(pady=10)

        self.status_msg = tk.Label(
            self.q_card,
            text="Neural challenge active. Verify identity.",
            font=("Consolas", 11, "bold"),
            fg="#aa88dd",
            bg="#090014"
        )
        self.status_msg.pack(pady=(10, 0))

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
            self.q_label.config(text=f"CHALLENGE {self.q_index + 1}:\n{q}")
            self.status_msg.config(text=f"Decryption Progress: {self.q_index}/{len(questions)} Complete", fg="#00ffff")
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
            self.status_msg.config(text="SIGNATURE MISMATCH! ACCESS DENIED!", fg="#ff0055")
            fail_sound = "failed.mp3" if os.path.exists(os.path.join(BASE_DIR, "assets", "audio", "failed.mp3")) else "failure.mp3"
            self.play_sound(fail_sound)
