import time
import tkinter as tk
from face_engine import load_owner_encodings, check_for_owner
from gui import IntruderScreen

print("Loading owner face profiles...")
owner_encodings = load_owner_encodings()
print(f"Loaded {len(owner_encodings)} profiles.")

def on_access_granted():
    print("Welcome, verified friend!")

def trigger_check():
    print("\n[!] Trigger activated. Checking face...")
    is_owner = check_for_owner(owner_encodings)

    if is_owner:
        print("[✓] Owner recognized. Normal login allowed.")
    else:
        print("[X] Intruder detected! Launching Manavalan UI...")
        root = tk.Tk()
        app = IntruderScreen(root, on_access_granted)
        root.mainloop()

if __name__ == "__main__":
    print("\n1. Arm Away Mode (Waits 5 seconds, then checks)")
    print("2. Instant Trigger (Demo Mode)")
    choice = input("Select: ")

    if choice == "1":
        print("Arming... Step away from the laptop.")
        time.sleep(5)
        trigger_check()
    else:
        trigger_check()
