import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import botcontroller as bc  # Imports the core engine logic
from terminal import LogTerminal  # Imports our logging terminal widget
import keyboard as kb  # Import the kernel-level listener module for binding

class AppUI(QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        
    def initUI(self) -> None:
        self.setWindowTitle("Bot Controller Action Log")
        
        # Window constraints matching your layout setup
        if bc.width == 1366 and bc.height == 768:
            self.setFixedSize(650, 520)
        elif bc.width == 1920 and bc.height == 1080:
            self.setFixedSize(850, 620)
        else:
            self.setFixedSize(750, 560)

        # Print Platform Info
        bc.print_platform_info()

        # Layout Setup
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setContentsMargins(20, 20, 20, 20)
        self.setLayout(grid)

        # 1. Main Header Label
        bot_label = QLabel("BOTCOMPOSE", self)
        bot_label.setFont(QFont("Helvetica", 20))
        bot_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(bot_label, 0, 0, 1, 3) # Spans completely from col 0 to col 2

        # 2. Screen Resolution Label
        screen_res_label = QLabel(f"Screen Resolution: {bc.get_screen_resolution()}", self)
        screen_res_label.setFont(QFont("Helvetica", 12))
        screen_res_label.setAlignment(Qt.AlignCenter)
        # FIX: We let the label span across ALL 3 columns just like the title, 
        # meaning its text alignment will perfectly mirror "BOTCOMPOSE".
        grid.addWidget(screen_res_label, 1, 0, 1, 3) 

        # Dynamic Stop Key Reassignment Button
        self.set_stop_btn = QPushButton(f"Stop Key: {bc.stop_key.upper()}", self)
        self.set_stop_btn.clicked.connect(self.change_stop_key)
        # FIX: We move the button down to row 1, column 2. 
        # Because the resolution label is transparently layered underneath it across the row, 
        # the button will sit neatly on the right side without squeezing the text over!
        grid.addWidget(self.set_stop_btn, 1, 2)

        # 3. File Read Row
        file_read_label = QLabel("Read from file ->", self)
        self.file_input_field = QLineEdit(self)
        self.file_input_field.setPlaceholderText("Enter file path...")
        
        file_read_btn = QPushButton("Run", self)
        file_read_btn.clicked.connect(lambda: bc.read_from_file(self.file_input_field.text()))
        
        grid.addWidget(file_read_label, 2, 0)
        grid.addWidget(self.file_input_field, 2, 1)
        grid.addWidget(file_read_btn, 2, 2)

        # 4. Manual Input Row
        manual_label = QLabel("Run commands manually ->", self)
        self.man_input_field = QLineEdit(self)
        self.man_input_field.setPlaceholderText("e.g., mv 500 500")
        
        man_run_btn = QPushButton("Run", self)
        man_run_btn.clicked.connect(lambda: bc.manual_input(self.man_input_field.text()))
        
        grid.addWidget(manual_label, 3, 0)
        grid.addWidget(self.man_input_field, 3, 1)
        grid.addWidget(man_run_btn, 3, 2)

        # 5. Integrated Action Log Viewer
        # Displays every single engine print() statement cleanly here
        self.terminal_widget = LogTerminal(self)
        grid.addWidget(self.terminal_widget, 4, 0, 1, 3)

        # Sizing stretches
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(4, 5)

    def change_stop_key(self) -> None:
        """Asynchronously waits for the next global keypress to change the termination hotkey."""
        self.set_stop_btn.setText("Press any key...")
        self.set_stop_btn.setEnabled(False)
        
        # We declare hook_ref as global or nonlocal so our inner function can see it
        hook_ref = None

        def capture_next_key(event):
            nonlocal hook_ref
            
            # 1. Update the stop key string directly inside the botcontroller module memory
            bc.stop_key = event.name
            
            # 2. Update the layout text to reflect the uppercase key token name
            self.set_stop_btn.setText(f"Stop Key: {event.name.upper()}")
            self.set_stop_btn.setEnabled(True)
            
            # 3. CRITICAL FIX: Cleanly unhook ONLY this specific listener
            if hook_ref is not None:
                kb.unhook(hook_ref)

        # kb.on_press returns a reference handle to this specific hook instance. 
        # We save it so we can safely remove it inside the callback itself!
        hook_ref = kb.on_press(capture_next_key)


def run():
    app = QApplication(sys.argv)
    ui = AppUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()