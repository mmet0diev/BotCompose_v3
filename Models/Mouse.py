import time
import os
import pyautogui as pag

class Mouse:

    def __init__(self,
            comp_name="Mouse",
            events=[],
            output_file="txt/mouse_events.txt") -> None:
        self.comp_name = comp_name
        self.events = events
        self.output_file = output_file
        self.pos = pag.position()

    # Get mouse position
    def getPos(self):
        self.pos = pag.position()
        return f"Mouse coordinates: {self.pos}"

    # Move mouse
    def mv(self, x: int, y: int, dur=0):
        time.sleep(0.1)
        pag.moveTo(x, y, duration=dur)

    # Click
    def clck(self, btn: str):
        time.sleep(0.2)
        if btn == "l":
            pag.click()
        elif btn == "r":
            pag.click(button="right")
        elif btn == "m":
            pag.click(button="middle")
        else:
            print("Invalid mouse btn.")

    # Move + click
    def mvclck(self, x: int, y: int, btn: str):
        time.sleep(0.2)
        pag.moveTo(x, y, duration=0)
        time.sleep(0.1)

        if btn == "l":
            pag.click()
        elif btn == "r":
            pag.click(button="right")
        elif btn == "m":
            pag.click(button="middle")
        else:
            print("Unknown mouse btn.")

    # Scroll
    def scroll(self, z: int):
        time.sleep(0.2)
        pag.scroll(z)

    # Hold button
    def hld(self, btn: str):
        time.sleep(0.2)
        btn_map = {"l": "left", "r": "right", "m": "middle"}
        pag.mouseDown(button=btn_map.get(btn, "left"))

    # Release button
    def rel(self, btn: str):
        btn_map = {"l": "left", "r": "right", "m": "middle"}
        pag.mouseUp(button=btn_map.get(btn, "left"))

    # Drag
    def drag(self, x1, y1, x2, y2, dur=1):
        time.sleep(0.5)
        pag.moveTo(x1, y1)
        pag.dragTo(x2, y2, duration=dur)

    # Click image
    def clck_img(self, img: str, btn: str="l", conf=0.6):
        time.sleep(0.2)
        try:
            img_location = pag.locateOnScreen(img, confidence=conf)
            if img_location is not None:
                img_center = pag.center(img_location)
                print(img_center)
                self.mvclck(img_center[0], img_center[1], btn)
            else:
                print("Image not found.")
        except Exception as e:
            print(f"Exception caught:\n {e}")

    # File ops
    def write_to_file(self):
        if os.path.isfile(self.output_file):
            with open(self.output_file, 'w') as f:
                for evs in self.events:
                    f.write(f"{evs}\n")

    def clear_file(self):
        open(self.output_file, 'w').close()

    # Stop recording (ESC)
    def stop_recording(self):
        while not pag.keyDown('esc'):
            time.sleep(0.05)

    # ❗ Removed record/play (pyautogui cannot replace these)
    def record(self):
        print("Recording not supported with pyautogui.")

    def play(self):
        print("Playback not supported with pyautogui.")

    def __str__(self) -> str:
        return f"Component: {self.comp_name}"