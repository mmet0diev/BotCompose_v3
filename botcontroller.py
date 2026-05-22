import os
import sys
import threading
from screeninfo import get_monitors
from Models.Bot import Bot

monitor = get_monitors()[0]  # Assuming the first monitor
width = monitor.width
height = monitor.height

def get_screen_resolution():
    return f"x={width} y={height}"

bot = Bot()

def read_from_file(src_path: str):
    # "Press 'esc' to stop command(s) execution.
    def execute_commands():
        try:
            with open(src_path, "r") as f:
                for line in f:
                    if bot.kb.check_key_pressed("esc"):
                        print("Execution stopped.")
                        break
                    if line != "":
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
                                comp = args[0]
                                btn = args[1]
                                if comp == 'mouse':
                                    bot.mouse_hld(btn=btn)
                                elif comp == 'kb':
                                    bot.kb_hld(btn=btn)
                            case "rel":
                                comp = args[0]
                                btn = args[1]
                                if comp == 'mouse':
                                    bot.mouse_rel(btn=btn)
                                elif comp == 'kb':
                                    bot.kb_rel(btn=btn)
                            case "clckimg":
                                if len(args) == 1:
                                    img_path = args[0]
                                    bot.clckimg(img_path)
                                elif len(args) == 2:
                                    img_path = args[0]
                                    btn = args[1]
                                    bot.clckimg(img_path, btn=btn)
                                elif len(args) == 3:
                                    img_path = args[0]
                                    btn = args[1]
                                    conf = float(args[2])
                                    bot.clckimg(img_path, btn=btn, conf=conf)
                            case "drag":
                                if (len(args) == 4):
                                    x1 = int(args[0])
                                    y1 = int(args[1])
                                    x2 = int(args[2])
                                    y2 = int(args[3])
                                    bot.drag(x1, y1, x2, y2)
                                elif (len(args) == 5):
                                    x1 = int(args[0])
                                    y1 = int(args[1])
                                    x2 = int(args[2])
                                    y2 = int(args[3])
                                    dur = int(args[4])
                                    bot.drag(x1, y1, x2, y2, dur)
                                else:
                                    print("Invalid arguments passed.")
                            case "wrt":
                                text = " ".join(args)
                                bot.wrt(text)
                            case "sleep":
                                secs = float(args[0])
                                bot.sleep(secs)
                            case "shoot":
                                if len(args) == 0:
                                    bot.take_shot()
                                elif len(args) == 1:
                                    d = float(args[0])
                                    bot.take_shot(delay=d)
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
                                print(f"Invalid command(s)/syntax: {func}")
                    else:
                        print("Empty line")
                f.close()
        except FileNotFoundError:
            print(f"File not found: {src_path}")
        except Exception as e:
            print(f"Invalid command(s)/syntax or file:\n{e}")

    # Create and start a new thread for executing commands
    execution_thread = threading.Thread(target=execute_commands)
    execution_thread.start()


# Manually issue commands from the terminal(similar to REPL / interactive mode)
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
                    btn = args[0]
                    bot.press(btn=btn)
                case "hld":
                    comp = args[0]
                    btn = args[1]
                    if comp == 'mouse':
                        bot.mouse_hld(btn=btn)
                    elif comp == 'kb':
                        bot.kb_hld(btn=btn)
                case "rel":
                    comp = args[0]
                    btn = args[1]
                    if comp == 'mouse':
                        bot.mouse_rel(btn=btn)
                    elif comp == 'kb':
                        bot.kb_rel(btn=btn)
                case "clckimg":
                    if len(args) == 1:
                        img_path = args[0]
                        bot.clckimg(img_path)
                    elif len(args) == 2:
                        img_path = args[0]
                        btn = args[1]
                        bot.clckimg(img_path, btn=btn)
                    elif len(args) == 3:
                        img_path = args[0]
                        btn = args[1]
                        conf = float(args[2])
                        bot.clckimg(img_path, btn=btn, conf=conf)
                case "drag":
                    if (len(args) == 4):
                        x1 = int(args[0])
                        y1 = int(args[1])
                        x2 = int(args[2])
                        y2 = int(args[3])
                        bot.drag(x1, y1, x2, y2)
                    elif (len(args) == 5):
                        x1 = int(args[0])
                        y1 = int(args[1])
                        x2 = int(args[2])
                        y2 = int(args[3])
                        dur = int(args[4])
                        bot.drag(x1, y1, x2, y2, dur)
                    else:
                        print("Invalid arguments passed.")
                case "wrt":
                    text = " ".join(args)
                    bot.wrt(text)
                case "sleep":
                    if len(args) == 0:
                        bot.sleep()
                    elif len(args) == 1:
                        secs = args[0]
                        bot.sleep(secs=secs)
                case "shoot":
                    if len(args) == 0:
                        bot.take_shot()
                    elif len(args) == 1:
                        d = float(args[0])
                        bot.take_shot(delay=d)
                case "play":
                    if args[0] == "mouse":
                        bot.play_mouse()
                    elif args[0] == "kb":
                        bot.play_kb()
                case "repeat":
                    if len(args) > 0:
                        reps = int(args[0])
                        bot.repeat_man(command=cmds[2:], reps=reps)
                    else:
                        print("Invalid number of args.")
                case _:
                    print(f"Invalid command/syntax: {func}")
        except Exception as e:
            print(e)
            
    # Create and start a new thread for executing commands
    execution_thread = threading.Thread(target=execute_commands)
    execution_thread.start()

def replay_mouse(reps = 1):
    for i in range(reps):
        bot.play_mouse()

def replay_kb(reps = 1):
    for i in range(reps):
        bot.play_kb()