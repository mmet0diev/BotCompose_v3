import os
import time
from Models.Keyboard import Keyboard
from Models.Mouse import Mouse
import pyautogui as pag

class Bot:
    imgs_path = os.path.join(os.getcwd(), "imgs")
    if not os.path.isdir(imgs_path):
        try: os.makedirs(imgs_path, exist_ok=True)
        except Exception: imgs_path = os.getcwd()

    def get_imgs_num(self) -> int:
        try:
            return len(os.listdir(self.imgs_path))
        except:
            print('[WARN] "imgs" path/folder not found')
            return 0

    def __init__(
        self,
        comp_name="Bot",
        events=[],
        m=None,
        kb=None,
        imgs_num=None
    ) -> None:
        self.comp_name = comp_name
        self.events = events
        self.m = m if m is not None else Mouse()
        self.kb = kb if kb is not None else Keyboard()
        self.imgs_num = imgs_num if imgs_num is not None else self.get_imgs_num()
        
        # This will hold the queue instance passed by the controller later
        self.command_queue = None

    def _send_to_queue(self, cmd_string: str):
        # Fallback: if queue isn't linked yet, print or drop safely instead of crashing
        if self.command_queue is not None:
            self.command_queue.put(("file_cmd", cmd_string))
        else:
            print(f"[QUEUE WARN] Queue not bound. Dropped: {cmd_string}")

    # --- Mouse API Proxies ---
    def getPos(self): return self.m.getPos()
    def mv(self, x: int, y: int, dur=0): self._send_to_queue(f"mv {x} {y}")
    def clck(self, btn: str): self._send_to_queue(f"clck {btn}")
    def mvclck(self, x: int, y: int, btn: str): self._send_to_queue(f"mvclck {x} {y} {btn}")
    def scroll(self, z: int): self._send_to_queue(f"scroll {z}")
    def mouse_hld(self, btn: str): self._send_to_queue(f"hld mouse {btn}")
    def mouse_rel(self, btn: str): self._send_to_queue(f"rel mouse {btn}")
    def drag(self, x1, y1, x2, y2, dur=2): self._send_to_queue(f"drag {x1} {y1} {x2} {y2} {dur}")
    def clckimg(self, img: str, btn="l", conf=0.6): self._send_to_queue(f"clckimg {img} {btn} {conf}")

    # --- Keyboard API Proxies ---
    def kb_hld(self, btn: str): self._send_to_queue(f"hld kb {btn}")
    def kb_rel(self, btn: str): self._send_to_queue(f"rel kb {btn}")
    def press(self, btn: str): self._send_to_queue(f"press {btn}")
    def wrt(self, text: str, d: float = 0.1): self._send_to_queue(f"wrt {text}")
    def sleep(self, secs=2.0): time.sleep(secs)

    # File mode repeat
    def repeat_lines(self, f, reps, n_lines, stop_trigger="esc"):
        commands = []
        for i in range(n_lines):
            try:
                line = next(f).strip()
                if not line: continue
                cmd = line.split(" ")
                commands.append((cmd[0], cmd[1:]))
            except StopIteration:
                break
            
        for j in range(reps):
            if self.kb.check_key_pressed(stop_trigger):
                print(f"[STOP] Loop sequence interrupted via key '{stop_trigger.upper()}'.")
                break
                
            for func, args in commands:
                arg_str = " ".join(map(str, args))
                self._send_to_queue(f"{func} {arg_str}")
                if func == "sleep":
                    time.sleep(float(args[0]))
                else:
                    time.sleep(0.02)

    # Manual mode repeat
    def repeat_man(self, command: list, reps: int = 2, stop_trigger="esc"):
        time.sleep(1)
        parts = command[1:]
        for i in range(reps):
            index = 0
            if self.kb.check_key_pressed(stop_trigger):
                print(f"[STOP] Manual loop sequence interrupted via key '{stop_trigger.upper()}'.")
                break
                
            while index < len(parts):
                cmd = command[index]
                if cmd == "mv":
                    self.mv(float(parts[index+1]), float(parts[index+2]))
                    index += 3
                elif cmd == "clck":
                    self.clck(parts[index+1])
                    index += 2
                elif cmd == "mvclck":
                    self.mvclck(float(parts[index+1]), float(parts[index+2]), parts[index+3])
                    index += 4
                elif cmd == "scroll":
                    self.scroll(int(parts[index+1]))
                    index += 2
                elif cmd == "press":
                    self.press(parts[index+1])
                    index += 2
                elif cmd == "hld":
                    self._send_to_queue(f"hld {parts[index+1]} {parts[index+2]}")
                    index += 3
                elif cmd == "drag":
                    self.drag(int(parts[index+1]), int(parts[index+2]), int(parts[index+3]), int(parts[index+4]))
                    index += 5
                elif cmd == "clckimg":
                    self.clckimg(img=parts[index+1])
                    index += 2
                else:
                    index += 1
            time.sleep(0.05)

    def rec_mouse(self, output_file="txt/mouse_events.txt"):
        self.m.output_file = output_file
        self.m.record()

    def play_mouse(self): self.m.play()
    def rec_kb(self, output_file="txt/kb_events.txt"):
        self.kb.output_file = output_file
        self.kb.record()
        
    def play_kb(self): self.kb.play()

    def take_shot(self, delay=0.5):
        time.sleep(delay)
        shot_name = f"screenshot{self.imgs_num}.png"
        pag.screenshot(os.path.join(self.imgs_path, shot_name))
        self.imgs_num += 1

    def __str__(self) -> str:
        return f"Component: {self.comp_name}"