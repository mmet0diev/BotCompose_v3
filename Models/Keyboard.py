import time
import os
import pyautogui as pag
import keyboard as kb  # Swapping to kernel-level hardware hooks

pag.FAILSAFE = True      # Enables the upper-left corner slam shutdown switch

class Keyboard:

    hotkeys = []

    # The KB constructor
    def __init__(self, comp_name="KB", 
            events=[], 
            output_file="txt/kb_events.txt",
            hotkeys = []) -> None:
        self.comp_name = comp_name
        self.events = events
        self.output_file = output_file
        self.hotkeys = hotkeys

    # Press and release a given btn
    def press(self, btn: str):
        time.sleep(0.1)
        kb.press(btn)
        kb.release(btn)

    # Holds a given btn
    def hld(self, btn: str):
        kb.press(btn)

    # Releases a given btn
    def rel(self, btn: str):
        kb.release(btn)

    # Press and release a sequence of keys/btns
    def wrt(self, text: str, d: int = 0.1):
        time.sleep(1)
        kb.write(text, delay=d)

    # Clear the KB file contents
    def clear_file(self):
        if os.path.isfile(self.output_file):
            open(self.output_file, 'w').close()

    # Write to the output file
    def write_to_file(self):
        with open(self.output_file, 'w') as f:
            for evs in self.events:
                f.write(f"{evs}\n")

    # Stop recording the keyboard events (Updated to accept dynamic stop key)
    def stop_recording(self, hook_ref, stop_trigger="esc"):
        # Checks the chosen custom stop trigger key dynamically instead of 'esc' string literal
        while not kb.is_pressed(stop_trigger):
            time.sleep(0.05)
        kb.unhook(hook_ref)

    # Record the keyboard events (Updated to accept dynamic stop key)
    def record(self, stop_trigger="esc"):
        self.events = []
        self.clear_file()
        
        print(f"Recording started. Press '{stop_trigger.upper()}' to stop...")
        hook_ref = kb.hook(self.events.append)
        
        # Pass the dynamic key to the poll loop
        self.stop_recording(hook_ref, stop_trigger)
        
        print("Recording finished.")
        self.write_to_file()

    # Play the keyboard events
    def play(self):
        time.sleep(1)
        kb.play(self.events)

    # Check if a key is pressed (PERFECT AS IS - Handles variables cleanly!)
    def check_key_pressed(self, key: str):
        if kb.is_pressed(key):
            return True
        return False

    # toString of KB
    def __str__(self) -> str:
         return f"\nComponent: {self.comp_name}\nAdded hotkeys:{self.hotkeys}"