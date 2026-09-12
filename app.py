import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import botcontroller as bc  
from terminal import LogTerminal  

try:
    from pynput import keyboard as pynput_kb
except Exception:
    pynput_kb = None

try:
    import keyboard as keyboard_pkg
except Exception:
    keyboard_pkg = None

class AppUI(QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        self.worker = None

    def initUI(self) -> None:
        self.setWindowTitle("Bot Controller Action Log")
        
        if bc.width == 1366 and bc.height == 768:
            self.setFixedSize(650, 520)
        elif bc.width == 1920 and bc.height == 1080:
            self.setFixedSize(850, 620)
        else:
            self.setFixedSize(750, 560)

        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setContentsMargins(20, 20, 20, 20)
        self.setLayout(grid)

        bot_label = QLabel("BOTCOMPOSE", self)
        bot_label.setFont(QFont("Helvetica", 20))
        bot_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(bot_label, 0, 0, 1, 3) 

        screen_res_label = QLabel(f"Screen Resolution: {bc.get_screen_resolution()}", self)
        screen_res_label.setFont(QFont("Helvetica", 12))
        screen_res_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(screen_res_label, 1, 0, 1, 3) 

        self.set_stop_btn = QPushButton(f"Stop Key: {bc.stop_key.upper()}", self)
        self.set_stop_btn.clicked.connect(self.change_stop_key)
        grid.addWidget(self.set_stop_btn, 1, 2)

        file_read_label = QLabel("Read from file ->", self)
        self.file_input_field = QLineEdit(self)
        self.file_input_field.setPlaceholderText("Enter file path...")
        
        file_read_btn = QPushButton("Run", self)
        file_read_btn.clicked.connect(self.start_file_stream)
        
        grid.addWidget(file_read_label, 2, 0)
        grid.addWidget(self.file_input_field, 2, 1)
        grid.addWidget(file_read_btn, 2, 2)

        manual_label = QLabel("Run commands manually ->", self)
        self.man_input_field = QLineEdit(self)
        self.man_input_field.setPlaceholderText("e.g., mv 500 500")
        
        man_run_btn = QPushButton("Run", self)
        man_run_btn.clicked.connect(self.execute_manual_direct)
        
        grid.addWidget(manual_label, 3, 0)
        grid.addWidget(self.man_input_field, 3, 1)
        grid.addWidget(man_run_btn, 3, 2)

        self.terminal_widget = LogTerminal(self)
        grid.addWidget(self.terminal_widget, 4, 0, 1, 3)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(4, 5)

    def start_file_stream(self):
        """Spawns the safe background thread worker and registers connection slots."""
        bc.is_running = True
        bc.bot.kb.start_interruption_monitor(bc.stop_key)

        self.worker = bc.ScriptWorker(self.file_input_field.text())
        # Connect signals thread-safely straight to Main Thread processors
        self.worker.command_signal.connect(self.process_hardware_action)
        self.worker.status_signal.connect(self.handle_system_status)
        self.worker.start()

    def execute_manual_direct(self):
        """Executes manual actions immediately on the main thread context.

        Manual UI execution should expose the same stop-key monitor as the
        file worker so repeat loops in the manual command path can observe the
        stop flag and exit cleanly instead of needing repeated key presses.
        """
        clean_cmd = self.man_input_field.text().strip()
        if not clean_cmd or clean_cmd.startswith("#"):
            return

        bc.bot.kb.start_interruption_monitor(bc.stop_key)
        try:
            cmds = clean_cmd.split(" ")
            self.process_hardware_action(cmds[0], cmds[1:])
        finally:
            bc.bot.kb.stop_interruption_monitor()

    def handle_system_status(self, status: str):
        if status == "EOF" or "stopped" in status:
            print(f"[SYSTEM] Clean thread breakdown: {status}")
            bc.bot.kb.stop_interruption_monitor()
            bc.is_running = False
            if self.worker:
                self.worker.quit()
        else:
            print(status)

    def process_hardware_action(self, func: str, args: list):
        """CRITICAL: Every input action is processed exclusively on the application Main Thread."""
        try:
            match func:
                case "mv":
                    bc.bot.m.mv(int(float(args[0])), int(float(args[1])))
                case "clck":
                    bc.bot.m.clck(args[0])
                case "mvclck":
                    bc.bot.m.mvclck(int(float(args[0])), int(float(args[1])), args[2])
                case "scroll":
                    bc.bot.m.scroll(int(args[0]))
                case "press":
                    bc.bot.kb.press(args[0])
                case "hld":
                    if args[0] == 'mouse': bc.bot.m.hld(args[1])
                    elif args[0] == 'kb': bc.bot.kb.hld(args[1])
                case "rel":
                    if args[0] == 'mouse': bc.bot.m.rel(args[1])
                    elif args[0] == 'kb': bc.bot.kb.rel(args[1])
                case "wrt":
                    bc.bot.kb.wrt(" ".join(args))
                case "shoot":
                    if len(args) == 0: bc.bot.take_shot()
                    elif len(args) == 1: bc.bot.take_shot(delay=float(args[0]))
                case "drag":
                    # Execute hardware drag directly on the Mouse controller
                    bc.bot.m.drag(int(args[0]), int(args[1]), int(args[2]), int(args[3]))
                case "clckimg":
                    # Support: clckimg <img> [btn] [conf]
                    if len(args) == 0:
                        print("[RUNTIME ERROR] clckimg requires at least an image path")
                    elif len(args) == 1:
                        bc.bot.m.clck_img(args[0])
                    elif len(args) == 2:
                        bc.bot.m.clck_img(args[0], btn=args[1])
                    else:
                        try:
                            conf = float(args[2])
                        except Exception:
                            conf = 0.6
                        bc.bot.m.clck_img(args[0], btn=args[1], conf=conf)
                case "repeat":
                    # Manual UI syntax: repeat <reps> <func> <args...>
                    if len(args) < 2:
                        print("[RUNTIME ERROR] repeat requires a count followed by a command token stream")
                    else:
                        try:
                            reps = int(args[0])
                            command = args[1:]
                            bc.bot.repeat_man(command, reps=reps)
                        except Exception as exc:
                            print(f"[RUNTIME ERROR] Failed repeating manual instruction: {exc}")
                case _:
                    pass
        except Exception as e:
            print(f"[RUNTIME ERROR] Failed executing hardware instruction '{func}': {e}")

    def change_stop_key(self) -> None:
        self.set_stop_btn.setText("Press any key...")
        self.set_stop_btn.setEnabled(False)
        listener = None

        def on_press(key):
            nonlocal listener
            try:
                key_name = getattr(key, "char", None)
                if key_name is None:
                    key_name = key.name
            except AttributeError:
                key_name = getattr(key, "name", str(key))

            bc.stop_key = key_name
            self.set_stop_btn.setText(f"Stop Key: {key_name.upper()}")
            self.set_stop_btn.setEnabled(True)

            # Stop the active listener from the appropriate backend.
            if pynput_kb is not None and listener is not None:
                listener.stop()
            elif keyboard_pkg is not None:
                keyboard_pkg.unhook_all()

        if pynput_kb is not None:
            listener = pynput_kb.Listener(on_press=on_press)
            listener.start()
        elif keyboard_pkg is not None:
            # Fallback backend from the existing requirements file.
            keyboard_pkg.hook(on_press=on_press)
        else:
            self.set_stop_btn.setText("Stop Key: ESC")
            self.set_stop_btn.setEnabled(True)
            print("[WARN] No keyboard listener backend installed; using ESC as default stop key.")


def run():
    app = QApplication(sys.argv)
    ui = AppUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()