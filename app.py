import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import botcontroller as bc  # Imports the core engine logic
from terminal import LogTerminal  # Imports our logging terminal widget

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

        # Layout Setup
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.setContentsMargins(20, 20, 20, 20)
        self.setLayout(grid)

        # 1. Main Header Label
        bot_label = QLabel("BOTCOMPOSE", self)
        bot_label.setFont(QFont("Helvetica", 20))
        bot_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(bot_label, 0, 0, 1, 3)

        # 2. Screen Resolution Label
        screen_res_label = QLabel(f"Screen Resolution: {bc.get_screen_resolution()}", self)
        screen_res_label.setFont(QFont("Helvetica", 12))
        screen_res_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(screen_res_label, 1, 0, 1, 3)

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


def run():
    app = QApplication(sys.argv)
    ui = AppUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()