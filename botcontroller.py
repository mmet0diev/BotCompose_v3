import os
import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from screeninfo import get_monitors
from Models.Bot import Bot

try:
    monitor = get_monitors()[0]
    width = monitor.width
    height = monitor.height
except Exception:
    width, height = 1920, 1080

def get_screen_resolution():
    return f"x={width} y={height}"

# Initialize the core bot engine object instance
bot = Bot()
stop_key = "esc" 
is_running = False

class ScriptWorker(QThread):
    """Safe Qt-native background worker that reads files without touching the hardware layer."""
    command_signal = pyqtSignal(str, list) # Emits (function_name, arguments_list)
    status_signal = pyqtSignal(str)        # Emits system status updates

    def __init__(self, src_path):
        super().__init__()
        self.src_path = src_path

    def run(self):
        self.status_signal.emit(f"Reading and executing commands from {self.src_path}\n")
        try:
            with open(self.src_path, "r") as f:
                for line in f:
                    clean_line = line.strip()
                    if not clean_line or clean_line.startswith("#"):
                        continue

                    # Check for stop trigger state from the bot model tracking layer
                    if bot.kb.check_key_pressed(stop_key):
                        self.status_signal.emit("Execution stopped by user.")
                        break
                    
                    if clean_line.startswith("repeat"):
                        cmds = clean_line.split(" ")
                        reps = int(cmds[1])
                        next_lines = int(cmds[2])
                        bot.repeat_lines(f=f, reps=reps, n_lines=next_lines, stop_trigger=stop_key)
                        continue

                    command = clean_line.split(" ")
                    func = command[0]
                    args = command[1:]

                    # Emit the task safely to the Main UI Thread for hardware processing
                    self.command_signal.emit(func, args)

                    if func == "sleep":
                        seconds = float(args[0]) if args else 1.0
                        time.sleep(seconds)
                    else:
                        time.sleep(0.02) # Yield execution gap
                        
        except FileNotFoundError:
            self.status_signal.emit(f"File not found: {self.src_path}")
        except Exception as e:
            self.status_signal.emit(f"Invalid command syntax error: {e}")
        finally:
            self.status_signal.emit("EOF")