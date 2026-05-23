import time
import os
import pyautogui as pag
pag.FAILSAFE = True      # Enables the upper-left corner slam shutdown switch
pag.PAUSE = 0.15          # Adds a mandatory 150ms processing pause after EVERY movement step

class Keyboard:

    hotkeys = []

    def __init__(self, comp_name="KB",
            events=[],
            output_file="txt/kb_events.txt",
            hotkeys=[]) -> None:
        self.comp_name = comp_name
        self.events = events
        self.output_file = output_file
        self.hotkeys = hotkeys

    # Press and release
    def press(self, btn: str):
        time.sleep(0.1)
        pag.press(btn)

    # Hold key
    def hld(self, btn: str):
        pag.keyDown(btn)

    # Release key
    def rel(self, btn: str):
        pag.keyUp(btn)

    # Write text
    def wrt(self, text: str, d: float = 0.1):
        time.sleep(1)
        pag.write(text, interval=d)

    # Clear file
    def clear_file(self):
        if os.path.isfile(self.output_file):
            open(self.output_file, 'w').close()

    # Write events (kept unchanged)
    def write_to_file(self):
        with open(self.output_file, 'w') as f:
            for evs in self.events:
                f.write(f"{evs}\n")

    # Stop recording (ESC)
    def stop_recording(self):
        while not pag.keyDown('esc'):
            time.sleep(0.05)

    # ❌ Not supported with pyautogui
    def record(self):
        print("Recording not supported with pyautogui.")

    def play(self):
        print("Playback not supported with pyautogui.")

    # Check if key is pressed
    def check_key_pressed(self, key: str):
        return pag.keyDown(key)

    # toString
    def __str__(self) -> str:
        return f"\nComponent: {self.comp_name}\nAdded hotkeys:{self.hotkeys}"
