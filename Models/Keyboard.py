import time
from pynput import keyboard

class Keyboard:
    def __init__(self, comp_name="KB"):
        self.comp_name = comp_name
        self.events = []
        self.controller = keyboard.Controller()
        self.stop_requested = False
        self.listener = None

    # --- 🚀 RESTORED GENERATION FUNCTIONS (Thread-Safe via pynput) ---

    def press(self, btn: str):
        """Press and release a single key instantly."""
        time.sleep(0.05)
        # Handle special layout keys (like enter, space, esc) or alphanumeric characters
        key = getattr(keyboard.Key, btn, btn)
        try:
            self.controller.press(key)
            time.sleep(0.01)
            self.controller.release(key)
        except Exception as e:
            print(f"[KB ERROR] Failed to press '{btn}': {e}")

    def hld(self, btn: str):
        """Hold a key down physically until rel() is explicitly called."""
        key = getattr(keyboard.Key, btn, btn)
        try:
            self.controller.press(key)
        except Exception as e:
            print(f"[KB ERROR] Failed to hold '{btn}': {e}")

    def rel(self, btn: str):
        """Release a key that was being held down."""
        key = getattr(keyboard.Key, btn, btn)
        try:
            self.controller.release(key)
        except Exception as e:
            print(f"[KB ERROR] Failed to release '{btn}': {e}")

    def wrt(self, text: str, d: float = 0.2):
        """Types out a string of text character by character with a minor delay."""
        time.sleep(0.5)  # Yield gap before typing begins
        # Replace underscores with spaces if your text file formatting layout uses them
        processed_text = text.replace("_", " ")
        for char in processed_text:
            try:
                self.controller.type(char)
                time.sleep(d)
            except Exception as e:
                print(f"[KB ERROR] Typestream character drop '{char}': {e}")


    # --- 🛠️ BACKWARD COMPATIBILITY & MONITOR HANDLES ---

    def start_interruption_monitor(self, stop_trigger="esc"):
        """Non-blocking background monitor layer used by the controller worker."""
        self.stop_requested = False
        
        def on_press(key):
            try:
                key_name = key.char
            except AttributeError:
                key_name = key.name

            if key_name == stop_trigger:
                print(f"\n[STOP] Emergency stop trigger '{stop_trigger.upper()}' caught.")
                self.stop_requested = True
                return False

        self.stop_interruption_monitor() # Clear any dangling hooks
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def stop_interruption_monitor(self):
        if self.listener and self.listener.running:
            self.listener.stop()
        self.listener = None
        self.stop_requested = False

    def check_key_pressed(self, key: str = None):
        """Fallback status checker interface allowing legacy loops to tick safely."""
        return self.stop_requested


    # --- Pynput Record & Playback (Your Original Code) ---
    def record(self, stop_trigger="esc"):
        self.events = []
        print(f"Recording keyboard. Press '{stop_trigger.upper()}' to stop...")

        def on_press(key):
            try: key_name = key.char
            except AttributeError: key_name = key.name

            if key_name == stop_trigger:
                return False
            self.events.append(('hld', key, time.time()))

        def on_release(key):
            try: key_name = key.char
            except AttributeError: key_name = key.name

            if key_name == stop_trigger:
                return False
            self.events.append(('rel', key, time.time()))

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        
        print("Keyboard recording finished.")

    def play(self):
        if not self.events:
            print("No keyboard events recorded to play.")
            return

        print("Playing back keyboard macro...")
        last_time = self.events[0][-1]

        for action, key, timestamp in self.events:
            time.sleep(max(0, timestamp - last_time))
            last_time = timestamp

            if action == 'hld':
                self.controller.press(key)
            elif action == 'rel':
                self.controller.release(key)