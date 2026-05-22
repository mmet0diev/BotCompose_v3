import sys
import os
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QFont, QTextCursor

class EmbeddedTerminal(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Style terminal UI (Dark Mode)
        self.setFont(QFont("Courier New", 10))
        self.setStyleSheet("background-color: #121212; color: #00FF00;")
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        # Core Shell Process Integration
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        
        # Determine appropriate OS System Shell Execution Target
        if sys.platform.startswith("win"):
            # Use PowerShell if available, fallback to cmd
            self.shell_cmd = "powershell.exe" if os.path.exists("C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe") else "cmd.exe"
        else:
            self.shell_cmd = "/bin/bash"
            
        # Start the background session terminal container
        self.process.start(self.shell_cmd)
        
        # Track input line boundary indexing properties
        self.command_buffer = ""
        
    def handle_stdout(self):
        """Reads normal output bytes from the process stream."""
        data = self.process.readAllStandardOutput().data()
        try:
            text = data.decode(sys.getdefaultencoding(), errors='replace')
        except Exception:
            text = data.decode('utf-8', errors='replace')
        self.append_text_at_end(text)

    def handle_stderr(self):
        """Reads warning and error byte signals from process stream."""
        data = self.process.readAllStandardError().data()
        try:
            text = data.decode(sys.getdefaultencoding(), errors='replace')
        except Exception:
            text = data.decode('utf-8', errors='replace')
        self.append_text_at_end(text)

    def append_text_at_end(self, text):
        """Inserts incoming shell streaming data safely into the viewport end."""
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(text)
        self.ensureCursorVisible()

    def keyPressEvent(self, event):
        """Captures real-time keyboard events to write directly to shell STDIN."""
        key = event.key()
        text = event.text()

        if key == Qt.Key_Return or key == Qt.Key_Enter:
            # Send current command string sequence down pipe path
            self.append_text_at_end("\n")
            self.process.write((self.command_buffer + "\n").encode())
            self.command_buffer = ""
        elif key == Qt.Key_Backspace:
            if len(self.command_buffer) > 0:
                self.command_buffer = self.command_buffer[:-1]
                # Mimic local character extraction deleting standard visual representation 
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.End)
                cursor.deletePreviousChar()
        elif text and text.isprintable():
            self.command_buffer += text
            self.append_text_at_end(text)
        else:
            # Allow fallback processing mechanics for scrolling or selection keys
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """Clean terminate child session references when killing main execution wrapper."""
        self.process.terminate()
        self.process.waitForFinished(1000)
        super().closeEvent(event)