import os
import time
from Models.Keyboard import Keyboard
from Models.Mouse import Mouse
import pyautogui as pag


class Bot:
    # imgs folder path
    try:
        imgs_path = os.path.join(os.getcwd(), "imgs")
    except Exception as e:
        imgs_path = os.getcwd()
        print("Folder/Directory not found.")

    # get initial number of image files in imgs folder
    def get_imgs_num(self) -> int:
        try:
            imgs_list = os.listdir(self.imgs_path)
            return len(imgs_list)
        except:
            print('"imgs" path/folder not found')

    # Bot constructor
    def __init__(
        self,
        comp_name="Bot",
        events=[],
        m=Mouse(),
        kb=Keyboard(),
        imgs_num=None
    ) -> None:
        self.comp_name = comp_name
        self.events = events
        self.m = m
        self.kb = kb
        if imgs_num is None:
            self.imgs_num = self.get_imgs_num()
        else:
            self.imgs_num = imgs_num


    # Mouse controls:
    # More of a testing function
    def getPos(self):
        self.m.getPos()

    # Move the mouse to xy
    def mv(self, x: int, y: int, dur=0):
        # print("mv called")
        self.m.mv(x=x, y=y, dur=dur)


    # Click a left, right, middle(scroll) mouse btn
    def clck(self, btn: str):
        self.m.clck(btn=btn)

    # A combination of mv() and clck()
    def mvclck(self, x: int, y: int, btn: str):
        self.m.mvclck(x=x, y=y, btn=btn)

    # Scroll the scroller z units + for up - for down
    def scroll(self, z: int):
        self.m.scroll(z=z)

    # Hold a given mouse btn
    def mouse_hld(self, btn: str):
        self.m.hld(btn=btn)

    # Drag the mouse to chosen coords
    def drag(self, x1, y1, x2, y2, dur=2):
        self.m.drag(x1=x1, y1=y1, x2=x2, y2=y2, dur=dur)

    # Release a given mouse btn
    def mouse_rel(self, btn: str):
        self.m.rel(btn=btn)

    # Click imgage function (from Mouse)
    def clckimg(self, img: str, btn="l", conf=0.6):
        self.m.clck_img(img=img, btn=btn, conf=conf)

    # Hold a given keyboard btn
    def kb_hld(self, btn: str):
        self.kb.hld(btn=btn)

    # Release a given keyboard btn
    def kb_rel(self, btn: str):
        self.kb.rel(btn=btn)

    # Keyboard controls:
    # Press a key/btn
    def press(self, btn: str):
        self.kb.press(btn=btn)

    # Press and release a sequence of keys/btns
    def wrt(self, text: str, d: int = 0.1):
        self.kb.wrt(text=text, d=d)

    # Puts the bot in "sleep" for secs time
    def sleep(self, secs=2.0):
        time.sleep(secs)

    # File mode repeat
    def repeat_lines(self, f, reps, n_lines):
        commands = []  # initialize the repeated commands list
        for i in range(n_lines):  # read the next n lines of commands
            line = next(f).strip()  # read the current line as str
            cmd = line.strip().split(" ")
            func = cmd[0]
            args = cmd[1:]
            commands.append((func, args))
        for j in range(reps):  # repeat the commands reps times
            if self.kb.check_key_pressed("esc"):
                print("Execution stopped.")
                break
            for func, args in commands:
                match func:
                    case "mv":
                        x, y = map(float, args)
                        self.mv(x, y)
                    case "clck":
                        btn = args[0]
                        self.clck(btn)
                    case "mvclck":
                        x, y = map(float, args[:2])
                        btn = args[2]
                        self.mvclck(x, y, btn)
                    case "scroll":
                        n = int(args[0])
                        self.scroll(n)
                    case "press":
                        key = args[0]
                        self.press(key)
                    case "hld":
                        comp = args[0]
                        if comp == "mouse":
                            key = args[0]
                            btn = args[1]
                            self.mouse_hld(btn=btn)
                        if comp == "kb":
                            key = args[0]
                            btn = args[1]
                            self.kb_hld(btn=btn)
                    case "rel":
                        comp = args[0]
                        btn = args[1]
                        if comp == "mouse":
                            key = args[0]
                            self.mouse_rel(btn=btn)
                        if comp == "kb":
                            key = args[0]
                            btn = args[1]
                            self.kb.rel(btn=btn)
                    case "wrt":
                        text = " ".join(args)
                        self.wrt(text)
                    case "sleep":
                        secs = float(args[0])
                        self.sleep(secs)
                    case "drag":
                        if(len(args) == 4):
                            x1 = int(args[0])
                            y1 = int(args[1])
                            x2 = int(args[2])
                            y2 = int(args[3])
                            self.drag(x1, y1, x2, y2)
                        elif(len(args) == 5):
                            x1 = int(args[0])
                            y1 = int(args[1])
                            x2 = int(args[2])
                            y2 = int(args[3])
                            dur = int(args[4])
                            self.drag(x1, y1, x2, y2, dur)
                        else:
                            print("Invalid arguments passed.")
                    case "clckimg":
                        if len(args) == 1:
                            img_path = args[0]
                            self.clckimg(img_path)
                        elif len(args) == 2:
                            img_path = args[0]
                            btn = args[1]
                            self.clckimg(img_path, btn=btn)
                        elif len(args) == 3:
                            img_path = args[0]
                            btn = args[1]
                            conf = float(args[2])
                            self.clckimg(img_path, btn=btn, conf=conf)
                    case "shoot":
                        self.take_shot()
                    case "play":
                        if args[0] == "mouse":
                            self.play_mouse()
                        elif args[0] == "kb":
                            self.play_kb()
                    case "repeat":
                        print("Cannot nest repeats")
                    case _:
                        print(f"Invalid command(s)/syntax: {func}")

    # Manual mode repeat (more of a testing function)
    def repeat_man(self, command: list, reps: int = 2):
        time.sleep(1)
        parts = command[1:]
        for i in range(reps):
            index = 0
            if self.kb.check_key_pressed("esc"):
                print("Execution stopped.")
                break
            while index < len(parts):
                cmd = command[index]
                if cmd == "mv":
                    coords = (parts[index], parts[index+1])
                    x = float(coords[0])
                    y = float(coords[1])
                    self.mv(x=x, y=y)
                    index += 3
                elif cmd == "clck":
                    btn = parts[index]
                    self.clck(btn=btn)
                    index += 2
                elif cmd == "mvclck":
                    coords = (parts[index], parts[index + 1])
                    x = float(coords[0])
                    y = float(coords[1])
                    btn = parts[index + 2]
                    self.mvclck(x=x, y=y, btn=btn)
                    index += 4
                elif cmd == "scroll":
                    n = int(parts[index])
                    self.scroll(n)
                    index += 2
                elif cmd == "press":
                    key = parts[index]
                    self.press(key)
                    index += 2
                elif cmd == "hld":
                    comp = parts[index]
                    if (comp == "mouse"):
                        key = parts[index + 1]
                        self.mouse_hld(key)
                        index += 3
                    elif comp == "kb":
                        key = parts[index + 1]
                        self.kb_hld(key)
                        index += 2
                elif cmd == "drag":
                    if(len(parts) == 4):
                        x1 = int(parts[0])
                        y1 = int(parts[1])
                        x2 = int(parts[2])
                        y2 = int(parts[3])
                        self.drag(x1, y1, x2, y2)
                        index+=4
                    elif(len(parts) == 5):
                        x1 = int(parts[0])
                        y1 = int(parts[1])
                        x2 = int(parts[2])
                        y2 = int(parts[3])
                        dur = int(parts[4])
                        self.drag(x1, y1, x2, y2, dur)
                        index+=5
                    else:
                        print("Invalid arguments passed.")
                elif cmd == "clckimg":
                    if len(parts) == 1:
                        img_path = parts[index]
                        self.clckimg(img=img_path)
                        index+=2
                    elif len(parts) == 2:
                        img_path = parts[index]
                        btn = parts[index+1]
                        self.clckimg(img=img_path, btn=btn)
                        index+=3
                    elif len(parts) == 3:
                        img_path = parts[index]
                        btn = parts[index+1]
                        conf = parts[index+2]
                        self.clckimg(img=img_path, btn=btn, conf=conf)
                        index+=4
                    else:
                        print("Invalid number of args.")
                elif cmd == "play":
                    comp = parts[index]
                    if comp == "mouse":
                        self.play_mouse()
                    elif comp == "kb":
                        self.play_kb()
                    index+=2
                elif cmd == "repeat":
                    print("Cannot nest repeats in man mode.")
                else:
                    index += 1
                # Stop the loop if necessary
                if self.kb.check_key_pressed("esc"):
                    break

    # Call the record function from the Mouse
    def rec_mouse(self, output_file="txt/mouse_events.txt"):
        self.m.output_file = output_file
        self.m.record()

    # Call the play function from the Mouse
    def play_mouse(self):
        self.m.play()

    # Call the record function from KB
    def rec_kb(self, output_file="txt/kb_events.txt"):
        self.kb.output_file = output_file
        self.kb.record()

    # Call the play function from KB
    def play_kb(self):
        self.kb.play()

    # Takes a screenshot and saves it to imgs folder
    def take_shot(self, delay=0.5):
        time.sleep(delay)
        pag.screenshot(f"{self.imgs_path}\\screenshot{self.imgs_num}.png")
        self.imgs_num += 1


    # toString for Model (Bot)
    def __str__(self) -> str:
        return f"Component: {self.comp_name}"
