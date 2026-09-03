import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_PY = os.path.join(BASE_DIR, "main.py")
PYTHON_BIN = sys.executable

def listen_for_events():
    print("[*] Listening for system resume / unlock events via D-Bus...")
    
    cmd = [
        "dbus-monitor",
        "--system",
        "type='signal',interface='org.freedesktop.login1.Manager',member='PrepareForSleep'"
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    was_asleep = False

    # Copy current environment and explicitly assign DISPLAY and XAUTHORITY
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    if "XAUTHORITY" not in env:
        env["XAUTHORITY"] = os.path.expanduser("~/.Xauthority")

    for line in process.stdout:
        line = line.strip()

        if "boolean true" in line:
            was_asleep = True
            print("\n[!] Laptop sleeping... System armed.")

        elif "boolean false" in line and was_asleep:
            was_asleep = False
            print("\n[!] Laptop woke up! Launching AARAADA...")
            subprocess.run([PYTHON_BIN, MAIN_PY, "--trigger"], env=env)

if __name__ == "__main__":
    listen_for_events()
