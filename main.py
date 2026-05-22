# import os
# import sys
# # Add the path of the Models directory to the system path
# dir_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(dir_path, "Models"))
# import threading
# from Models.Bot import Bot
# from screeninfo import get_monitors

# monitor = get_monitors()[0]  # Assuming the first monitor
# width = monitor.width
# height = monitor.height

# def get_screen_resolution():
#     return f"x={width} y={height}"

# bot = Bot()

# def read_from_file(src_path: str):
#     # "Press 'esc' to stop command(s) execution.
#     def execute_commands():
#         try:
#             with open(src_path, "r") as f:
#                 for line in f:
#                     if bot.kb.check_key_pressed("esc"):
#                         print("Execution stopped.")
#                         break
#                     if line != "":
#                         command = line.strip().split(" ")
#                         func = command[0]
#                         args = command[1:]
#                         match func:
#                             case "mv":
#                                 x, y = map(float, args)
#                                 bot.mv(x, y)
#                             case "clck":
#                                 btn = args[0]
#                                 bot.clck(btn)
#                             case "mvclck":
#                                 x, y = map(float, args[:2])
#                                 btn = args[2]
#                                 bot.mvclck(x, y, btn)
#                             case "scroll":
#                                 n = int(args[0])
#                                 bot.scroll(n)
#                             case "press":
#                                 key = args[0]
#                                 bot.press(key)
#                             case "hld":
#                                 comp = args[0]
#                                 btn = args[1]
#                                 if comp == 'mouse':
#                                     bot.mouse_hld(btn=btn)
#                                 elif comp == 'kb':
#                                     bot.kb_hld(btn=btn)
#                             case "rel":
#                                 comp = args[0]
#                                 btn = args[1]
#                                 if comp == 'mouse':
#                                     bot.mouse_rel(btn=btn)
#                                 elif comp == 'kb':
#                                     bot.kb_rel(btn=btn)
#                             case "clckimg":
#                                 if len(args) == 1:
#                                     img_path = args[0]
#                                     bot.clckimg(img_path)
#                                 elif len(args) == 2:
#                                     img_path = args[0]
#                                     btn = args[1]
#                                     bot.clckimg(img_path, btn=btn)
#                                 elif len(args) == 3:
#                                     img_path = args[0]
#                                     btn = args[1]
#                                     conf = float(args[2])
#                                     bot.clckimg(img_path, btn=btn, conf=conf)
#                             case "drag":
#                                 if (len(args) == 4):
#                                     x1 = int(args[0])
#                                     y1 = int(args[1])
#                                     x2 = int(args[2])
#                                     y2 = int(args[3])
#                                     bot.drag(x1, y1, x2, y2)
#                                 elif (len(args) == 5):
#                                     x1 = int(args[0])
#                                     y1 = int(args[1])
#                                     x2 = int(args[2])
#                                     y2 = int(args[3])
#                                     dur = int(args[4])
#                                     bot.drag(x1, y1, x2, y2, dur)
#                                 else:
#                                     print("Invalid arguments passed.")
#                             case "wrt":
#                                 text = " ".join(args)
#                                 bot.wrt(text)
#                             case "sleep":
#                                 secs = float(args[0])
#                                 bot.sleep(secs)
#                             case "shoot":
#                                 if len(args) == 0:
#                                     bot.take_shot()
#                                 elif len(args) == 1:
#                                     d = float(args[0])
#                                     bot.take_shot(delay=d)
#                             case "play":
#                                 if args[0] == "mouse":
#                                     bot.play_mouse()
#                                 elif args[0] == "kb":
#                                     bot.play_kb()
#                             case "repeat":
#                                 reps = int(args[0])
#                                 next_lines = int(args[1])
#                                 bot.repeat_lines(f=f, reps=reps, n_lines=next_lines)
#                             case _:
#                                 print(f"Invalid command(s)/syntax: {func}")
#                     else:
#                         print("Empty line")
#                 f.close()
#         except FileNotFoundError:
#             print(f"File not found: {src_path}")
#         except Exception as e:
#             print(f"Invalid command(s)/syntax or file:\n{e}")

#     # Create and start a new thread for executing commands
#     execution_thread = threading.Thread(target=execute_commands)
#     execution_thread.start()


# # Manually issue commands from the terminal(similar to REPL / interactive mode)
# def manual_input(cmd: str):
#     def execute_commands():
#         cmds = cmd.strip().split(" ")
#         func = cmds[0]
#         args = cmds[1:]
#         try:
#             match func:
#                 case "mv":
#                     x, y = map(float, args)
#                     bot.mv(x, y)
#                 case "clck":
#                     btn = args[0]
#                     bot.clck(btn)
#                 case "mvclck":
#                     x, y = map(float, args[:2])
#                     btn = args[2]
#                     bot.mvclck(x, y, btn)
#                 case "scroll":
#                     n = int(args[0])
#                     bot.scroll(n)
#                 case "press":
#                     btn = args[0]
#                     bot.press(btn=btn)
#                 case "hld":
#                     comp = args[0]
#                     btn = args[1]
#                     if comp == 'mouse':
#                         bot.mouse_hld(btn=btn)
#                     elif comp == 'kb':
#                         bot.kb_hld(btn=btn)
#                 case "rel":
#                     comp = args[0]
#                     btn = args[1]
#                     if comp == 'mouse':
#                         bot.mouse_rel(btn=btn)
#                     elif comp == 'kb':
#                         bot.kb_rel(btn=btn)
#                 case "clckimg":
#                     if len(args) == 1:
#                         img_path = args[0]
#                         bot.clckimg(img_path)
#                     elif len(args) == 2:
#                         img_path = args[0]
#                         btn = args[1]
#                         bot.clckimg(img_path, btn=btn)
#                     elif len(args) == 3:
#                         img_path = args[0]
#                         btn = args[1]
#                         conf = float(args[2])
#                         bot.clckimg(img_path, btn=btn, conf=conf)
#                 case "drag":
#                     if (len(args) == 4):
#                         x1 = int(args[0])
#                         y1 = int(args[1])
#                         x2 = int(args[2])
#                         y2 = int(args[3])
#                         bot.drag(x1, y1, x2, y2)
#                     elif (len(args) == 5):
#                         x1 = int(args[0])
#                         y1 = int(args[1])
#                         x2 = int(args[2])
#                         y2 = int(args[3])
#                         dur = int(args[4])
#                         bot.drag(x1, y1, x2, y2, dur)
#                     else:
#                         print("Invalid arguments passed.")
#                 case "wrt":
#                     text = " ".join(args)
#                     bot.wrt(text)
#                 case "sleep":
#                     if len(args) == 0:
#                         bot.sleep()
#                     elif len(args) == 1:
#                         secs = args[0]
#                         bot.sleep(secs=secs)
#                 case "shoot":
#                     if len(args) == 0:
#                         bot.take_shot()
#                     elif len(args) == 1:
#                         d = float(args[0])
#                         bot.take_shot(delay=d)
#                 case "play":
#                     if args[0] == "mouse":
#                         bot.play_mouse()
#                     elif args[0] == "kb":
#                         bot.play_kb()
#                 case "repeat":
#                     if len(args) > 0:
#                         reps = int(args[0])
#                         bot.repeat_man(command=cmds[2:], reps=reps)
#                     else:
#                         print("Invalid number of args.")
#                 case _:
#                     print(f"Invalid command/syntax: {func}")
#         except Exception as e:
#             print(e)
            
#     # Create and start a new thread for executing commands
#     execution_thread = threading.Thread(target=execute_commands)
#     execution_thread.start()

# def replay_mouse(reps = 1):
#     for i in range(reps):
#         bot.play_mouse()

# def replay_kb(reps = 1):
#     for i in range(reps):
#         bot.play_kb()

# import tkinter as tk

# class AppUI():
    
#     def __init__(self) -> None:
#         self.root = tk.Tk()
#         self.root.title("Bot Controller")
#         if width == 1366 and height == 768:
#             self.root.geometry("600x400")
#         elif width == 1920 and height == 1080:
#             self.root.geometry("900x550")
#         self.root.resizable(False, False)
#         self.root.columnconfigure([0, 1, 2, 3], pad=20)
#         self.root.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], pad=20)

#         # Define widgets
#         bot_label = tk.Label(self.root, text="BOTCOMPOSE", font=("Helvetica", 20), pady=5)
#         screen_res_label = tk.Label(self.root, text=f"Screen Resolution: {get_screen_resolution()}", font=("Helvetica", 12))

#         mouse_filepath_entry = tk.Entry(self.root)
#         kb_filepath_entry = tk.Entry(self.root)
#         mouse_rec_btn = tk.Button(self.root, text="rec mouse", pady=5, command=lambda: self.callMouseRec(mouse_filepath_entry.get()))
#         kb_rec_btn = tk.Button(self.root, text="rec kb", pady=5, command=lambda: self.callKbRec(kb_filepath_entry.get()))

#         mouse_label1 = tk.Label(self.root, text="Enter output file path. -->")
#         mouse_label2 = tk.Label(self.root, text="Enter number of re-plays -->")
#         kb_label1 = tk.Label(self.root, text="Enter output file path. -->")
#         kb_label2 = tk.Label(self.root, text="Enter number of re-plays -->")

#         mouse_play_entry = tk.Entry(self.root, name="1")
#         mouse_play_btn = tk.Button(self.root, text="play mouse", pady=5, command=lambda: self.replay_mouse_btn_clicked(mouse_play_entry))
#         kb_play_entry = tk.Entry(self.root)
#         kb_play_btn = tk.Button(self.root, text="play kb", pady=5, command=lambda: self.replay_kb_btn_clicked(kb_play_entry))


#         file_read_label = tk.Label(self.root, text="Read from file ->")
#         file_input_field = tk.Entry(self.root)
#         file_read_btn = tk.Button(self.root, text="Run", pady=5)
#         file_read_btn.configure(command=lambda: read_from_file(file_input_field.get()))

#         manual_label = tk.Label(self.root, text="Run commands manually ->")
#         man_input_field = tk.Entry(self.root)
#         man_run_btn = tk.Button(self.root, text="Run", command=lambda: manual_input(man_input_field.get()))

#         # Pack widgets
#         # span across all columns
#         bot_label.grid(row=0, column=0, columnspan=4)
#         screen_res_label.grid(row=1, column=0, columnspan=4)

#         mouse_label1.grid(row=2, column=0)
#         mouse_filepath_entry.grid(row=2, column=1)
#         mouse_rec_btn.grid(row=2, column=2)
#         mouse_label2.grid(row=4, column=0)
#         mouse_play_entry.grid(row=4, column=1)
#         mouse_play_btn.grid(row=4, column=2)

#         kb_label1.grid(row=3, column=0)
#         kb_filepath_entry.grid(row=3, column=1)
#         kb_rec_btn.grid(row=3, column=2)
#         kb_label2.grid(row=5, column=0)
#         kb_play_entry.grid(row=5, column=1)
#         kb_play_btn.grid(row=5, column=2)

#         file_read_label.grid(row=6, column=0)
#         file_input_field.grid(row=6, column=1)
#         file_read_btn.grid(row=6, column=2)
#         manual_label.grid(row=7, column=0)
#         man_input_field.grid(row=7, column=1)
#         man_run_btn.grid(row=7, column=2)

#         # Center the bot_label widget
#         self.root.grid_columnconfigure(0, weight=1)
#         self.root.grid_columnconfigure(4, weight=1)
#         bot_label.grid_configure(sticky="nsew")

#         self.root.mainloop()


#     def replay_mouse_btn_clicked(self, entry):
#         value = entry.get()
#         if value:
#             try:
#                 reps = int(value)
#                 def execute_commands():
#                     for _ in range(reps):
#                         bot.play_mouse()

#                 # Create and start a new thread for executing commands
#                 execution_thread = threading.Thread(target=execute_commands)
#                 execution_thread.start()
#             except ValueError:
#                 print("Invalid input. Please enter a valid integer.")
#         else:
#             def execute_commands():
#                 bot.play_mouse()

#             # Create and start a new thread for executing commands
#             execution_thread = threading.Thread(target=execute_commands)
#             execution_thread.start()

#     def replay_kb_btn_clicked(self, entry):
#         value = entry.get()
#         if value:
#             try:
#                 reps = int(value)
#                 def execute_commands():
#                     for _ in range(reps):
#                         bot.play_kb()

#                 # Create and start a new thread for executing commands
#                 execution_thread = threading.Thread(target=execute_commands)
#                 execution_thread.start()
#             except ValueError:
#                 print("Invalid input. Please enter a valid integer.")
#         else:
#             def execute_commands():
#                 bot.play_kb()

#             # Create and start a new thread for executing commands
#             execution_thread = threading.Thread(target=execute_commands)
#             execution_thread.start()

#     def callMouseRec(self, entry):
#         def execute_commands():
#             if(entry == ""):
#                 bot.rec_mouse()
#             else:
#                 bot.rec_mouse(entry)

#         # Create and start a new thread for executing commands
#         execution_thread = threading.Thread(target=execute_commands)
#         execution_thread.start()

#     def callKbRec(self, entry):
#         def execute_commands():
#             if(entry == ""):
#                 bot.rec_kb()
#             else:
#                 bot.rec_kb(entry)

#         execution_thread = threading.Thread(target=execute_commands)
#         execution_thread.start()

# def run():
#     app = AppUI()


# if __name__ == "__main__":
#     run()
