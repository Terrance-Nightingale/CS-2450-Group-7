import tkinter as tk
from tkinter import filedialog

class InputPanel:
    def __init__(self, root, container, interface_with_backend):
        self.root = root
        self.input_to = interface_with_backend
        self.container = container
        
        self.file_entry_frame = tk.Frame(
            self.container)
        self.file_entry_frame.pack(padx=10, pady=6)

        tk.Label(
            self.file_entry_frame, 
            text="Enter your file path: ", 
            font="Arial, 11", 
            anchor="w", 
            justify="left"
            ).grid(row=0, column=0, columnspan=2, sticky="w")
        
        self.file_entry = tk.Entry(
            self.file_entry_frame, 
            bg="light gray",
            )
        self.file_entry.bind("<Return>", lambda event=None: self.file_entered())
        self.file_entry.grid(row=0, column=2)

        self.file_entry_button = tk.Button(
            self.file_entry_frame, 
            text=">", 
            command=self.file_entered,
            width=2, 
            height=1)
        self.file_entry_button.grid(padx=2, pady=2, row=0, column=3)
        
        self.load_button = tk.Button(
            self.file_entry_frame,
            text="Load",
            command=self.browse_file)
        
        self.load_button.grid(padx=2, pady=2, row=0, column=4)

        tk.Label(
            self.file_entry_frame, 
            text="Chosen file:",
            font="Arial, 11", 
            width=8,
            ).grid(row=1, column=0)

        self.file_choice_label = tk.Label(
            self.file_entry_frame, 
            text="--No file Chosen--", 
            anchor="w", 
            justify="left", 
            width=30)
        self.file_choice_label.grid(row=1, column=1, columnspan=3, sticky="w")

    def file_entered(self):
        file_path = self.file_entry.get()
        self.file_choice_label.config(text=file_path)

        self.load_program_from_file(file_path)

        # Set currently selected tab's name to the loaded filename (i.e. "MyProgram.txt")
        current_tab = self.root.get_current_tab()
        self.root.set_tab_name(current_tab, file_path)


    def load_program_from_file(self, file_path):
        self.input_to.reset_program() # Reset CPU before loading new program. Added by: Josh 3/18/2026
        self.input_to.user_program.program = []
        self.input_to.user_program.inputProgram(file_path)
        self.input_to.load_program(self.input_to.user_program)
        

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Program File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)
        self.file_entered()
