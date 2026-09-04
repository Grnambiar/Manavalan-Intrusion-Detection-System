import win32api
import win32con
import win32gui
import win32ts
import time

# Power broadcast constants
WM_POWERBROADCAST = 0x0218
PBT_APMSUSPEND = 0x0004
PBT_APMRESUMESUSPEND = 0x0007
PBT_APMRESUMEAUTOMATIC = 0x0012

# Session change constants
WM_WTSSESSION_CHANGE = 0x02B1
WTS_SESSION_LOCK = 0x7
WTS_SESSION_UNLOCK = 0x8

class WindowsListener:
    def __init__(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.wnd_proc
        wc.lpszClassName = "LapSentryListener"
        hinst = wc.hInstance = win32api.GetModuleHandle(None)

        try:
            win32gui.RegisterClass(wc)
        except Exception:
            pass

        self.hwnd = win32gui.CreateWindow(
            wc.lpszClassName,
            "LapSentryHiddenWindow",
            0, 0, 0, 0, 0, 0, 0, hinst, None
        )

        win32ts.WTSRegisterSessionNotification(self.hwnd, win32ts.NOTIFY_FOR_THIS_SESSION)
        print("[*] Windows Listener registered successfully.")

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_POWERBROADCAST:
            if wparam == PBT_APMSUSPEND:
                print("\n[EVENT] Laptop going to sleep (PBT_APMSUSPEND)")
            elif wparam in (PBT_APMRESUMEAUTOMATIC, PBT_APMRESUMESUSPEND):
                print("\n[EVENT] WAKE EVENT DETECTED")

        elif msg == WM_WTSSESSION_CHANGE:
            if wparam == WTS_SESSION_LOCK:
                print("\n[EVENT] Screen locked (WTS_SESSION_LOCK)")
            elif wparam == WTS_SESSION_UNLOCK:
                print("\n[EVENT] WAKE EVENT DETECTED (WTS_SESSION_UNLOCK)")

        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def run(self):
        print("[*] Waiting for sleep/wake/lock events... (Press Ctrl+C to stop)")
        while True:
            win32gui.PumpWaitingMessages()
            time.sleep(0.1)

if __name__ == "__main__":
    listener = WindowsListener()
    listener.run()