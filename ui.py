import tkinter as tk
import threading
import botcontroller as bc  # Imports the core engine logic

class AppUI():
    
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Bot Controller")
        
        # Adaptive UI sizing based on engine width/height
        if bc.width == 1366 and bc.height == 768:
            self.root.geometry("600x400")
        elif bc.width == 1920 and bc.height == 1080:
            self.root.geometry("900x550")
            
        self.root.resizable(False, False)
        self.root.columnconfigure([0, 1, 2, 3], pad=20)
        self.root.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], pad=20)

        # Define widgets
        bot_label = tk.Label(self.root, text="BOTCOMPOSE", font=("Helvetica", 20), pady=5)
        screen_res_label = tk.Label(self.root, text=f"Screen Resolution: {bc.get_screen_resolution()}", font=("Helvetica", 12))

        mouse_filepath_entry = tk.Entry(self.root)
        kb_filepath_entry = tk.Entry(self.root)
        mouse_rec_btn = tk.Button(self.root, text="rec mouse", pady=5, command=lambda: self.callMouseRec(mouse_filepath_entry.get()))
        kb_rec_btn = tk.Button(self.root, text="rec kb", pady=5, command=lambda: self.callKbRec(kb_filepath_entry.get()))

        mouse_label1 = tk.Label(self.root, text="Enter output file path. -->")
        mouse_label2 = tk.Label(self.root, text="Enter number of re-plays -->")
        kb_label1 = tk.Label(self.root, text="Enter output file path. -->")
        kb_label2 = tk.Label(self.root, text="Enter number of re-plays -->")

        mouse_play_entry = tk.Entry(self.root, name="1")
        mouse_play_btn = tk.Button(self.root, text="play mouse", pady=5, command=lambda: self.replay_mouse_btn_clicked(mouse_play_entry))
        kb_play_entry = tk.Entry(self.root)
        kb_play_btn = tk.Button(self.root, text="play kb", pady=5, command=lambda: self.replay_kb_btn_clicked(kb_play_entry))

        file_read_label = tk.Label(self.root, text="Read from file ->")
        file_input_field = tk.Entry(self.root)
        file_read_btn = tk.Button(self.root, text="Run", pady=5)
        file_read_btn.configure(command=lambda: bc.read_from_file(file_input_field.get()))

        manual_label = tk.Label(self.root, text="Run commands manually ->")
        man_input_field = tk.Entry(self.root)
        man_run_btn = tk.Button(self.root, text="Run", command=lambda: bc.manual_input(man_input_field.get()))

        # Grid-mapping configurations
        bot_label.grid(row=0, column=0, columnspan=4)
        screen_res_label.grid(row=1, column=0, columnspan=4)

        mouse_label1.grid(row=2, column=0)
        mouse_filepath_entry.grid(row=2, column=1)
        mouse_rec_btn.grid(row=2, column=2)
        mouse_label2.grid(row=4, column=0)
        mouse_play_entry.grid(row=4, column=1)
        mouse_play_btn.grid(row=4, column=2)

        kb_label1.grid(row=3, column=0)
        kb_filepath_entry.grid(row=3, column=1)
        kb_rec_btn.grid(row=3, column=2)
        kb_label2.grid(row=5, column=0)
        kb_play_entry.grid(row=5, column=1)
        kb_play_btn.grid(row=5, column=2)

        file_read_label.grid(row=6, column=0)
        file_input_field.grid(row=6, column=1)
        file_read_btn.grid(row=6, column=2)
        manual_label.grid(row=7, column=0)
        man_input_field.grid(row=7, column=1)
        man_run_btn.grid(row=7, column=2)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(4, weight=1)
        bot_label.grid_configure(sticky="nsew")

        self.root.mainloop()

    def replay_mouse_btn_clicked(self, entry):
        value = entry.get()
        if value:
            try:
                reps = int(value)
                execution_thread = threading.Thread(target=lambda: bc.replay_mouse(reps))
                execution_thread.start()
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        else:
            execution_thread = threading.Thread(target=bc.bc.bot.play_mouse)
            execution_thread.start()

    def replay_kb_btn_clicked(self, entry):
        value = entry.get()
        if value:
            try:
                reps = int(value)
                execution_thread = threading.Thread(target=lambda: bc.replay_kb(reps))
                execution_thread.start()
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        else:
            execution_thread = threading.Thread(target=bc.bot.play_kb)
            execution_thread.start()

    def callMouseRec(self, entry):
        def execute_commands():
            if entry == "":
                bc.bot.rec_mouse()
            else:
                bc.bot.rec_mouse(entry)

        execution_thread = threading.Thread(target=execute_commands)
        execution_thread.start()

    def callKbRec(self, entry):
        def execute_commands():
            if entry == "":
                bc.bot.rec_kb()
            else:
                bc.bot.rec_kb(entry)

        execution_thread = threading.Thread(target=execute_commands)
        execution_thread.start()

def run():
    app = AppUI()

if __name__ == "__main__":
    run()