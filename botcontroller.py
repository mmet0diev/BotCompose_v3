import os
import sys
import threading
import time
from screeninfo import get_monitors
from Models.Bot import Bot
import pyautogui as pag

monitor = get_monitors()[0]
width = monitor.width
height = monitor.height

def get_screen_resolution():
    return f"x={width} y={height}"

bot = Bot()

# This variable can now be reassigned dynamically by your UI button!
stop_key = "esc" 

is_running = False

def read_from_file(src_path: str):
    global is_running
    is_running = True

    def check_interrupt():
        """Helper to quickly check keypress status using dynamic variable."""
        global is_running, stop_key
        if not is_running or bot.kb.check_key_pressed(stop_key):
            is_running = False
            return True
        return False

    def execute_commands():
        global is_running
        print(f"Reading and executing commands from {src_path}\n")

        try:
            with open(src_path, "r") as f:
                for line in f:
                    clean_line = line.strip()
                    
                    # Skip completely empty lines or script comments
                    if not clean_line or clean_line.startswith("#"):
                        continue

                    # Intercept loop steps cleanly before executing line
                    if check_interrupt():
                        print("Execution stopped by user.")
                        break
                        
                    command = clean_line.split(" ")
                    func = command[0]
                    args = command[1:]
                    
                    try:
                        match func:
                            case "mv":
                                x, y = map(float, args)
                                print(f"mouse moved: {x},{y}")
                                bot.mv(x, y)
                            case "clck":
                                btn = args[0]
                                print(f"mouse btn clicked: {btn}")
                                bot.clck(btn)
                            case "mvclck":
                                x, y = map(float, args[:2])
                                btn = args[2]
                                print(f"mouse moved {x},{y} and btn clicked: {btn}")
                                bot.mvclck(x, y, btn)
                            case "scroll":
                                n = int(args[0])
                                print(f"scrolling: {n} units")
                                bot.scroll(n)
                            case "press":
                                key = args[0]
                                print(f"key pressed: {key}")
                                bot.press(key)
                            case "hld":
                                comp, btn = args[0], args[1]
                                print(f"holding down {comp} button/key: {btn}")
                                if comp == 'mouse':
                                    bot.mouse_hld(btn=btn)
                                elif comp == 'kb':
                                    bot.kb_hld(btn=btn)
                            case "rel":
                                comp, btn = args[0], args[1]
                                print(f"releasing {comp} button/key: {btn}")
                                if comp == 'mouse':
                                    bot.mouse_rel(btn=btn)
                                elif comp == 'kb':
                                    bot.kb_rel(btn=btn)
                            case "clckimg":
                                if len(args) == 1:
                                    print(f"searching image on screen: {args[0]}")
                                    bot.clckimg(args[0])
                                elif len(args) == 2:
                                    print(f"searching and clicking image on screen: {args[0]} with button {args[1]}")
                                    bot.clckimg(args[0], btn=args[1])
                                elif len(args) == 3:
                                    print(f"searching image on screen: {args[0]} with confidence {args[2]}")
                                    bot.clckimg(args[0], btn=args[1], conf=float(args[2]))
                            case "drag":
                                if len(args) == 4:
                                    x1, y1, x2, y2 = map(int, args)
                                    print(f"dragging from {x1},{y1} to {x2},{y2}")
                                    bot.drag(x1, y1, x2, y2)
                                elif len(args) == 5:
                                    x1, y1, x2, y2 = map(int, args[:4])
                                    dur = int(args[4])
                                    print(f"dragging from {x1},{y1} to {x2},{y2} over {dur}s")
                                    bot.drag(x1, y1, x2, y2, dur)
                            case "wrt":
                                text = " ".join(args)
                                print(f"writing text input: '{text}'")
                                bot.wrt(text)
                            case "sleep":
                                seconds = float(args[0])
                                print(f"sleeping for {seconds} seconds...", flush=True)
                                
                                # Dynamic Micro-Step Pause: Allows manual/file tasks to catch stop keys mid-sleep!
                                steps = int(seconds / 0.1)
                                for _ in range(steps):
                                    if check_interrupt():
                                        break
                                    time.sleep(0.1)
                            case "shoot":
                                print("screen shot")
                                if len(args) == 0:
                                    bot.take_shot()
                                elif len(args) == 1:
                                    bot.take_shot(delay=float(args[0]))
                            case "repeat":
                                reps = int(args[0])
                                next_lines = int(args[1])
                                print(f"repeating next {next_lines} lines for {reps} cycles")
                                # Forward the dynamic string variable
                                bot.repeat_lines(f=f, reps=reps, n_lines=next_lines, stop_trigger=stop_key)
                            case _:
                                continue
                                
                        # Secondary inline safety check immediately following action steps
                        if check_interrupt():
                            print("Execution stopped.")
                            break

                    except pag.FailSafeException:
                        raise pag.FailSafeException
                    except Exception as e:
                        print(f"[ERROR] Line skipped in '{func}': {e}")
                        continue
                        
        except pag.FailSafeException:
            print("[PANIC] Fail-Safe triggered! Terminating script execution immediately.")
        except FileNotFoundError:
            print(f"File not found: {src_path}")
        except Exception as e:
            print(f"Invalid command or syntax error:\n{e}")
        finally:
            is_running = False

    execution_thread = threading.Thread(target=execute_commands, daemon=True)
    execution_thread.start()


def manual_input(cmd: str):
    global is_running
    is_running = True
    print("Executing manual commands:")

    def check_interrupt():
        global is_running, stop_key
        if not is_running or bot.kb.check_key_pressed(stop_key):
            is_running = False
            return True
        return False

    def execute_commands():
        global is_running, stop_key
        clean_cmd = cmd.strip()
        
        if not clean_cmd or clean_cmd.startswith("#"):
            is_running = False
            return
            
        cmds = clean_cmd.split(" ")
        func = cmds[0]
        args = cmds[1:]
        
        try:
            if check_interrupt():
                print("Manual execution stopped by user.")
                is_running = False
                return

            try:
                match func:
                    case "mv":
                        x, y = map(int, args)
                        print(f"mouse moved: {x},{y}")
                        bot.mv(x, y)
                    case "clck":
                        print(f'mouse btn clicked: {args[0]}')
                        bot.clck(args[0])
                    case "mvclck":
                        x, y = map(int, args[:2])
                        print(f'mouse moved {x},{y} and btn clicked: {args[2]}')
                        bot.mvclck(x, y, args[2])
                    case "scroll":
                        n = int(args[0])
                        print(f"scrolling: {n} units")
                        bot.scroll(n)
                    case "press":
                        print(f"key pressed: {args[0]}")
                        bot.press(btn=args[0])
                    case "hld":
                        comp, btn = args[0], args[1]
                        print(f"holding down {comp} button/key: {btn}")
                        if comp == 'mouse': bot.mouse_hld(btn=btn)
                        elif comp == 'kb': bot.kb_hld(btn=btn)
                    case "rel":
                        comp, btn = args[0], args[1]
                        print(f"releasing {comp} button/key: {btn}")
                        if comp == 'mouse': bot.mouse_rel(btn=btn)
                        elif comp == 'kb': bot.kb_rel(btn=btn)
                    case "clckimg":
                        if len(args) == 1: 
                            print(f"searching image on screen: {args[0]}")
                            bot.clckimg(args[0])
                        elif len(args) == 2: 
                            print(f"searching and clicking image on screen: {args[0]} with button {args[1]}")
                            bot.clckimg(args[0], btn=args[1])
                        elif len(args) == 3: 
                            print(f"searching image on screen: {args[0]} with confidence {args[2]}")
                            bot.clckimg(args[0], btn=args[1], conf=float(args[2]))
                    case "drag":
                        if len(args) == 4:
                            x1, y1, x2, y2 = map(int, args)
                            print(f"dragging from {x1},{y1} to {x2},{y2}")
                            bot.drag(*map(int, args))
                        elif len(args) == 5:
                            x1, y1, x2, y2 = map(int, args[:4])
                            dur = int(args[4])
                            print(f"dragging from {x1},{y1} to {x2},{y2} over {dur}s")
                            bot.drag(*map(int, args[:4]), dur)
                    case "wrt":
                        text = " ".join(args)
                        print(f"writing text input: '{text}'")
                        bot.wrt(text)
                    case "sleep":
                        seconds = float(args[0]) if len(args) > 0 else 1.0
                        print(f"sleeping for {seconds} seconds...", flush=True)
                        
                        # Dynamic Micro-Step Pause for manual input mode
                        steps = int(seconds / 0.1)
                        for _ in range(steps):
                            if check_interrupt():
                                print("Manual sleep sequence stopped by user.")
                                break
                            time.sleep(0.1)
                    case "shoot":
                        print("screen shot")
                        if len(args) == 0: bot.take_shot()
                        elif len(args) == 1: bot.take_shot(delay=float(args[0]))
                    case "repeat":
                        if len(args) > 0:
                            reps = int(args[0])
                            print(f"repeating sequence command manual entry {reps} times")
                            # Forward the dynamic string variable
                            bot.repeat_man(command=cmds[2:], reps=reps, stop_trigger=stop_key)
                    case _:
                        pass
                        
                # Check right after single-shot manual actions finish running
                if check_interrupt():
                    print("Manual execution dropped.")

            except pag.FailSafeException:
                raise pag.FailSafeException
            except Exception as e:
                print(f"[ERROR] Manual input failed execution step '{func}': {e}")

        except pag.FailSafeException:
            print("[PANIC] Fail-Safe triggered via Manual input field! Stopping immediately.")
        finally:
            is_running = False
            
    execution_thread = threading.Thread(target=execute_commands, daemon=True)
    execution_thread.start()