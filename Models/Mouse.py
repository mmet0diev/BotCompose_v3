import time
import pyautogui as pag # Keep for screenshots / image detection and fallback

# Try to import pynput.mouse; if unavailable, fall back to pyautogui implementations
USE_PYNPUT = True
try:
    from pynput import mouse
except Exception:
    mouse = None
    USE_PYNPUT = False

class Mouse:
    def __init__(self, comp_name="Mouse"):
        self.comp_name = comp_name
        # Initialize the native thread-safe controller when available
        self.controller = mouse.Controller() if USE_PYNPUT else None

    def getPos(self):
        # Thread-safe position retrieval
        if USE_PYNPUT and self.controller is not None:
            self.pos = self.controller.position
            return f"Mouse coordinates: {self.pos}"
        else:
            pos = pag.position()
            return f"Mouse coordinates: {pos}"

    def mv(self, x: int, y: int, dur=0):
        # Thread-safe absolute movement
        time.sleep(0.02)
        if USE_PYNPUT and self.controller is not None:
            self.controller.position = (int(x), int(y))
        else:
            # pyautogui handles durations and works across platforms
            pag.moveTo(int(x), int(y), duration=dur if dur else 0)

    def clck(self, btn: str):
        time.sleep(0.05)
        if USE_PYNPUT and self.controller is not None:
            btn_map = {
                "l": mouse.Button.left,
                "r": mouse.Button.right,
                "m": mouse.Button.middle
            }
            target_btn = btn_map.get(btn, mouse.Button.left)
            self.controller.click(target_btn, 1)
        else:
            # pyautogui uses 'left'/'right' strings
            btn_map = {"l": "left", "r": "right", "m": "middle"}
            pag.click(button=btn_map.get(btn, "left"))

    def mvclck(self, x: int, y: int, btn: str):
        self.mv(x, y)
        time.sleep(0.1)
        self.clck(btn)

    def scroll(self, z: int):
        time.sleep(0.05)
        if USE_PYNPUT and self.controller is not None:
            # pynput scroll takes (dx, dy). dy positive is up, negative is down
            self.controller.scroll(0, int(z))
        else:
            # pyautogui.scroll uses y offset
            pag.scroll(int(z))

    def hld(self, btn: str):
        if USE_PYNPUT and self.controller is not None:
            btn_map = {"l": mouse.Button.left, "r": mouse.Button.right, "m": mouse.Button.middle}
            self.controller.press(btn_map.get(btn, mouse.Button.left))
        else:
            btn_map = {"l": "left", "r": "right", "m": "middle"}
            pag.mouseDown(button=btn_map.get(btn, "left"))

    def rel(self, btn: str):
        if USE_PYNPUT and self.controller is not None:
            btn_map = {"l": mouse.Button.left, "r": mouse.Button.right, "m": mouse.Button.middle}
            self.controller.release(btn_map.get(btn, mouse.Button.left))
        else:
            btn_map = {"l": "left", "r": "right", "m": "middle"}
            pag.mouseUp(button=btn_map.get(btn, "left"))

    def drag(self, x1, y1, x2, y2, dur=1):
        # Quick thread-safe drag implementation
        if USE_PYNPUT and self.controller is not None:
            self.mv(x1, y1)
            time.sleep(0.05)
            self.hld("l")
            time.sleep(0.05)
            self.mv(x2, y2)
            time.sleep(0.05)
            self.rel("l")
        else:
            # Use pyautogui drag which handles durations nicely
            pag.moveTo(int(x1), int(y1))
            pag.dragTo(int(x2), int(y2), duration=dur)

    def clck_img(self, img: str, btn: str="l", conf=0.6):
        # PyAutoGUI image location is fine as it only reads data rather than pushing inputs
        time.sleep(0.2)
        try:
            img_location = pag.locateOnScreen(img, confidence=conf)
            if img_location is not None:
                img_center = pag.center(img_location)
                # Use underlying implementations for movement+click
                if USE_PYNPUT and self.controller is not None:
                    self.mvclck(img_center[0], img_center[1], btn)
                else:
                    pag.moveTo(img_center[0], img_center[1])
                    btn_map = {"l": "left", "r": "right", "m": "middle"}
                    pag.click(button=btn_map.get(btn, "left"))
            else:
                print("image not detected")
        except Exception as e:
            print(f"[ERROR] Image detection failed: {e}")

    def __str__(self) -> str:
        return f"Component: {self.comp_name}"