import sys
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QTextCursor
import platform
import os

class StreamSignals(QObject):
    """Signals to pass intercepted console text safely to the main GUI thread."""
    text_written = pyqtSignal(str)

class LogTerminal(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Style terminal UI (Dark Mode Logging Look)
        self.setFont(QFont("Courier New", 10))
        self.setStyleSheet("background-color: #121212; color: #33FF33;")
        self.setReadOnly(True)  # Blocks user input entirely since it's an output log
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        # Intercept system stdout/stderr streams
        self.signals = StreamSignals()
        self.signals.text_written.connect(self.append_log)
        
        sys.stdout = OutputRedirector(sys.stdout, self.signals)
        sys.stderr = OutputRedirector(sys.stderr, self.signals)
        
        print("[SYSTEM] Log Terminal Initialized. Monitoring Bot Actions...")
        self.print_platform_info()

    def append_log(self, text):
        """Appends incoming print statements and scrolls to the bottom."""
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(text)
        self.ensureCursorVisible()
    
    @staticmethod
    def print_platform_info():
        os_name = platform.system()

        print("=" * 50)
        print(f"Detected OS: {os_name}")

        if os_name == "Linux":
            session = os.environ.get("XDG_SESSION_TYPE", "unknown")

            if session.lower() == "x11":
                print("[INFO] Linux X11 session detected.")
                print("[INFO] Full mouse/keyboard automation should work normally.")

            elif session.lower() == "wayland":
                print("[WARNING] Linux Wayland session detected.")
                print("[WARNING] Mouse, keyboard hooks, screenshots, or image recognition may be restricted.")

            else:
                print(f"[INFO] Linux session type: {session}")

        elif os_name == "Windows":
            print("[INFO] Windows detected.")
            print("[INFO] Full mouse/keyboard automation should work normally.")

        else:
            print(f"[WARNING] Unrecognized OS: {os_name}")
            print("[WARNING] Automation compatibility is unknown.")

        print("=" * 50)

class OutputRedirector:
    """Helper wrapper to intercept write operations on sys.stdout/sys.stderr."""
    def __init__(self, original_stream, signals):
        self.original_stream = original_stream
        self.signals = signals

    def write(self, text):
        self.original_stream.write(text)  # Keeps printing to your IDE terminal
        self.signals.text_written.emit(text)  # Sends it straight to the PyQt GUI widget

    def flush(self):
        self.original_stream.flush()