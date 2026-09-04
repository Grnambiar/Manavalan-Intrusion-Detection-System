# Manavalan-Intrusion-Detection-System

### Team Name:Obsolete

### Team Members

* Team Lead: Gauri Rajagopal - Muthoot Institute of Technology and Science
* Member 2: Geethika C  - Muthoot Institute of Technology and Science

### Project Description

An unapologetically theatrical, cross-platform, non-invasive laptop security guardian that catches unauthorized access when a laptop wakes from sleep. It verifies the owner using facial feature analysis and subjects suspicious snoopers to full-screen neon cyber-chaos, Malayalam dialogues (*"Aaraadaa?!"*), bouncing Manavalan stickers, and friendship trivia challenges.

### The Problem (that doesn't exist)

Standard operating system lock screens are boring, silent, and far too polite to friends and hostel-mates trying to snoop on your WhatsApp or steal your Netflix account the second you leave your desk to grab tea.

### The Solution (that nobody asked for)

Replace silent login prompts with a digital Manavalan who wakes up via OS power/session events, checks the webcam, and yells at intruders. If you're an unauthorized snooper, you face high-speed bouncing stickers, flashing retro-cyber grids, and escalating police sirens; if you're a friend, you must prove your loyalty by answering personal trivia questions to pass.

## Technical Details

### Technologies/Components Used

* **Languages used:** Python 3
* **Frameworks used:** Tkinter GUI Toolkit
* **Libraries used:**
* `OpenCV (cv2)` (Haar Cascade Face Detection, Histogram Extraction & Comparison)
* `pygame` (Low-latency audio engine for sound effects and siren escalation)
* `Pillow (PIL)` (Image handling, RGBA rendering, and sticker resizing)
* `numpy` (Histogram array normalization)
* `pywin32` / `wmi` (Windows session unlock and power event hooks)


 **Tools used:**
  * Linux D-Bus (`dbus-monitor` via `systemd-logind`)  
  * Windows Event Hooks (`win32gui`, `wmi`)
  * VS Code
  * Git / GitHub


### Implementation


#### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/lap-sentry.git
cd lap-sentry

# On Linux (Kali):
python3 -m venv venv
source venv/bin/activate
pip install "opencv-python<5" pygame Pillow numpy

# On Windows:
python -m venv venv
venv\Scripts\activate
pip install "opencv-python<5" pygame Pillow numpy pywin32

```

#### Run

```bash
# Manual / Demo mode (Any OS)
python main.py

# Run OS background listener on Kali/Linux (triggers on sleep/wake):
python linux_listener.py

# Run OS background listener on Windows (triggers on sleep/wake & unlock):
python windows_listener.py

```


### Project Documentation

#### Screenshots

<img width="1920" height="1080" alt="Screenshot From 2026-09-04 08-21-14" src="https://github.com/user-attachments/assets/3ad8bcbb-382e-4fd9-abf4-3ad31406e3f2" />
Initial Lockdown: Bouncing Manavalan sticker, live animated Matrix floor grid, and the initial Malayalam dialogue popup demanding the PIN.


<img width="1920" height="1080" alt="Screenshot From 2026-09-04 08-21-32" src="https://github.com/user-attachments/assets/7e038683-4798-43e1-b0eb-ef2920576d65" />
Wrong PIN Escaped State: Triggering police sirens, red alert banners, and accelerated bouncing sticker physics.


<img width="1920" height="1080" alt="Screenshot From 2026-09-04 08-21-46" src="https://github.com/user-attachments/assets/bfffa543-089c-4cb8-8de7-0fe3067e1310" />
Friendship Decryption Matrix: Successfully entering the PIN unlocks the secondary personal trivia question validation screen.

#### Diagrams

```
+-------------------------------------------------------------+
|               System Wake / Resume Trigger                  |
|     (systemd-logind on Linux  |  Win32/WMI on Windows)      |
+------------------------------+------------------------------+
                               |
                               v
               +---------------+---------------+
               |   OpenCV Webcam Verification  |
               +---------------+---------------+
                               |
            [Face Matched?]----+----[Unknown / No Match]
                   |                           |
                   v                           v
      +------------+-----------+  +------------+-----------+
      | Silent Access Granted  |  |  Trigger AARAADA GUI   |
      |   Normal Work Resumes  |  |  Play: aarada.mp3      |
      +------------------------+  +------------+-----------+
                                               |
                                               v
                                    +----------+----------+
                                    | PIN Verification    |
                                    +----------+----------+
                                               |
                          [Correct PIN]--------+--------[Wrong PIN]
                                |                             |
                                v                             v
                  +-------------+------------+  +-------------+------------+
                  | Friendship Trivia Matrix |  | Play siren.mp3 + Sticker |
                  | (questions.json check)   |  | Acceleration Alert       |
                  +-------------+------------+  +--------------------------+
                                |
                   [All Correct]| [Wrong Answer]
                                |       |
                                v       +--> Play failed.mp3
                  +-------------+------------+
                  | Lockdown Lifted          |
                  +--------------------------+

```

*Cross-Platform Architecture: D-Bus/Windows event listener hooks, OpenCV facial comparison engine, and tiered audio/visual UI escalation.*



### Project Demo

#### Video

[Link to Demo Video](https://youtube.com/)
*Walkthrough of waking from sleep on both Linux and Windows, background daemon event capture, face rejection, and audio/UI escalation upon entering an incorrect PIN.*


## Team Contributions

* **Geethika Chellaton**: Linux D-Bus hook listener (`linux_listener.py`), OpenCV face detection and histogram comparison engine (`face_engine.py`), systemd service daemon architecture, and backend state integration.
* **Gauri**: Windows OS event listener (`windows_listener.py`), Tkinter cyber-matrix canvas animations with bouncing sticker physics, cross-platform asset integration, audio escalation pipeline, and Windows environment testing.
