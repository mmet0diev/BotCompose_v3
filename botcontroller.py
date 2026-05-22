import os
import sys
import threading
import time
from screeninfo import get_monitors
from Models.Bot import Bot

monitor = get_monitors()[0]  # Assuming the first monitor
width = monitor.width
height = monitor.height

def get_screen_resolution():
    return f"x={width} y={height}"

bot = Bot()

# Global flag to track active runs across threads safely
is_running = False

def read_from_file(src_path: str):
    global is_running
    is_running = True

    def check_interrupt():
        """Helper to quickly check keypress status without locking up."""
        global is_running
        if not is_running or bot.kb.check_key_pressed("esc"):
            is_running = False
            return True
        return False

    def execute_commands():
        global is_running
        try:
            with open(src_path, "r") as f:
                for line in f:
                    # Check interrupt immediately at loop step
                    if check_interrupt():
                        print("Execution stopped by user.")
                        break
                        
                    if line.strip() != "":
                        command = line.strip().split(" ")
                        func = command[0]
                        args = command[1:]
                        
                        match func:
                            case "mv":
                                x, y = map(float, args)
                                bot.mv(x, y)
                            case "clck":
                                btn = args[0]
                                bot.clck(btn)
                            case "mvclck":
                                x, y = map(float, args[:2])
                                btn = args[2]
                                bot.mvclck(x, y, btn)
                            case "scroll":
                                n = int(args[0])
                                bot.scroll(n)
                            case "press":
                                key = args[0]
                                bot.press(key)
                            case "hld":
                                comp, btn = args[0], args[1]
                                if comp == 'mouse':
                                    bot.mouse_hld(btn=btn)
                                elif comp == 'kb':
                                    bot.kb_hld(btn=btn)
                            case "rel":
                                comp, btn = args[0], args[1]
                                if comp == 'mouse':
                                    bot.mouse_rel(btn=btn)
                                elif comp == 'kb':
                                    bot.kb_rel(btn=btn)
                            case "clckimg":
                                if len(args) == 1:
                                    bot.clckimg(args[0])
                                elif len(args) == 2:
                                    bot.clckimg(args[0], btn=args[1])
                                elif len(args) == 3:
                                    bot.clckimg(args[0], btn=args[1], conf=float(args[2]))
                            case "drag":
                                if len(args) == 4:
                                    x1, y1, x2, y2 = map(int, args)
                                    bot.drag(x1, y1, x2, y2)
                                elif len(args) == 5:
                                    x1, y1, x2, y2 = map(int, args[:4])
                                    bot.drag(x1, y1, x2, y2, int(args[4]))
                            case "wrt":
                                bot.wrt(" ".join(args))
                            case "sleep":
                                secs = float(args[0])
                                # Instead of locking up the engine block for seconds,
                                # we slice sleep into 100ms intervals to continuously check for 'esc'
                                steps = int(secs / 0.1)
                                for _ in range(steps):
                                    if check_interrupt():
                                        break
                                    time.sleep(0.1)
                            case "shoot":
                                if len(args) == 0:
                                    bot.take_shot()
                                elif len(args) == 1:
                                    bot.take_shot(delay=float(args[0]))
                            case "play":
                                if args[0] == "mouse":
                                    bot.play_mouse()
                                elif args[0] == "kb":
                                    bot.play_kb()
                            case "repeat":
                                reps = int(args[0])
                                next_lines = int(args[1])
                                bot.repeat_lines(f=f, reps=reps, n_lines=next_lines)
                            case _:
                                print(f"Invalid command/syntax: {func}")
                                
                    # One secondary safety check directly after action processing
                    if check_interrupt():
                        print("Execution stopped.")
                        break
        except FileNotFoundError:
            print(f"File not found: {src_path}")
        except Exception as e:
            print(f"Invalid command or syntax error:\n{e}")
        finally:
            is_running = False

    execution_thread = threading.Thread(target=execute_commands, daemon=True)
    execution_thread.start()


def manual_input(cmd: str):
    def execute_commands():
        cmds = cmd.strip().split(" ")
        func = cmds[0]
        args = cmds[1:]
        try:
            match func:
                case "mv":
                    x, y = map(float, args)
                    bot.mv(x, y)
                case "clck":
                    bot.clck(args[0])
                case "mvclck":
                    x, y = map(float, args[:2])
                    bot.mvclck(x, y, args[2])
                case "scroll":
                    bot.scroll(int(args[0]))
                case "press":
                    bot.press(btn=args[0])
                case "hld":
                    comp, btn = args[0], args[1]
                    if comp == 'mouse': bot.mouse_hld(btn=btn)
                    elif comp == 'kb': bot.kb_hld(btn=btn)
                case "rel":
                    comp, btn = args[0], args[1]
                    if comp == 'mouse': bot.mouse_rel(btn=btn)
                    elif comp == 'kb': bot.kb_rel(btn=btn)
                case "clckimg":
                    if len(args) == 1: bot.clckimg(args[0])
                    elif len(args) == 2: bot.clckimg(args[0], btn=args[1])
                    elif len(args) == 3: bot.clckimg(args[0], btn=args[1], conf=float(args[2]))
                case "drag":
                    if len(args) == 4:
                        bot.drag(*map(int, args))
                    elif len(args) == 5:
                        bot.drag(*map(int, args[:4]), int(args[4]))
                case "wrt":
                    bot.wrt(" ".join(args))
                case "sleep":
                    secs = float(args[0]) if len(args) > 0 else 1.0
                    time.sleep(secs)
                case "shoot":
                    if len(args) == 0: bot.take_shot()
                    elif len(args) == 1: bot.take_shot(delay=float(args[0]))
                case "play":
                    if args[0] == "mouse": bot.play_mouse()
                    elif args[0] == "kb": bot.play_kb()
                case "repeat":
                    if len(args) > 0:
                        bot.repeat_man(command=cmds[2:], reps=int(args[0]))
                case _:
                    print(f"Invalid command: {func}")
        except Exception as e:
            print(e)
            
    execution_thread = threading.Thread(target=execute_commands, daemon=True)
    execution_thread.start()

def replay_mouse(reps=1):
    for _ in range(reps):
        if not is_running: break
        bot.play_mouse()

def replay_kb(reps=1):
    for _ in range(reps):
        if not is_running: break
        bot.play_kb()