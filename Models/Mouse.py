import time
from pynput import mouse
import pyautogui as pag # Keep only for screenshots / image detection if needed

class Mouse:
    def __init__(self, comp_name="Mouse"):
        self.comp_name = comp_name
        # Initialize the native thread-safe controller
        self.controller = mouse.Controller()

    def getPos(self):
        # Thread-safe position retrieval
        self.pos = self.controller.position
        return f"Mouse coordinates: {self.pos}"

    def mv(self, x: int, y: int, dur=0):
        # Thread-safe absolute movement
        time.sleep(0.05) # Tiny buffer for system stability
        self.controller.position = (int(x), int(y))

    def clck(self, btn: str):
        time.sleep(0.1)
        btn_map = {
            "l": mouse.Button.left,
            "r": mouse.Button.right,
            "m": mouse.Button.middle
        }
        target_btn = btn_map.get(btn, mouse.Button.left)
        self.controller.click(target_btn, 1)

    def mvclck(self, x: int, y: int, btn: str):
        self.mv(x, y)
        time.sleep(0.1)
        self.clck(btn)

    def scroll(self, z: int):
        time.sleep(0.1)
        # pynput scroll takes (dx, dy). dy positive is up, negative is down
        self.controller.scroll(0, int(z))

    def hld(self, btn: str):
        btn_map = {"l": mouse.Button.left, "r": mouse.Button.right, "m": mouse.Button.middle}
        self.controller.press(btn_map.get(btn, mouse.Button.left))

    def rel(self, btn: str):
        btn_map = {"l": mouse.Button.left, "r": mouse.Button.right, "m": mouse.Button.middle}
        self.controller.release(btn_map.get(btn, mouse.Button.left))

    def drag(self, x1, y1, x2, y2, dur=1):
        # Quick thread-safe drag implementation
        self.mv(x1, y1)
        time.sleep(0.1)
        self.hld("l")
        time.sleep(0.1)
        self.mv(x2, y2)
        time.sleep(0.1)
        self.rel("l")

    def clck_img(self, img: str, btn: str="l", conf=0.6):
        # PyAutoGUI image location is fine as it only reads data rather than pushing inputs
        time.sleep(0.2)
        try:
            img_location = pag.locateOnScreen(img, confidence=conf)
            if img_location is not None:
                img_center = pag.center(img_location)
                self.mvclck(img_center[0], img_center[1], btn)
            else:
                print("image not detected")
        except Exception as e:
            print(f"[ERROR] Image detection failed: {e}")

    def __str__(self) -> str:
        return f"Component: {self.comp_name}"