import tkinter as tk


class InputPanel:
    def __init__(self, container, backend_controller):
        self.backend_controller = backend_controller
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

        tk.Label(
            self.file_entry_frame,
            text="If pop up doesn't appear during 'READ' command,\ncheck behind main window."
        ).grid(row=2, column=0, columnspan=4)

        """
        word_entry_frame = tk.Frame(
            self.container)
        word_entry_frame.pack(padx=10, pady=6)

        tk.Label(
            word_entry_frame,
            text="Upon 'READ' command, enter word here:", 
            font="Arial, 11"
        ).grid(row=0, column=0, columnspan=3)

        self.word_entry = tk.Entry(
            word_entry_frame,
            bg="light gray",
            font= "Arial, 20",
            width=15
        )
        self.word_entry.bind("<Return>", lambda event=None: self.word_entered())
        self.word_entry.grid(row=1, column=0, columnspan=2)

        word_entry_button = tk.Button(
            word_entry_frame, 
            text=">", 
            command=self.word_entered,
            width=2, 
            height=1)
        word_entry_button.grid(padx=2, pady=2, row=1, column=2)

        tk.Label(
            word_entry_frame,
            text="Note: word must be an integer between -/+9999",
            font= "Arial, 8"
        ).grid(row=2, column=0, columnspan=3)

        tk.Label(
            word_entry_frame,
            text="Last word submitted:"
        ).grid(row=3, column=0)

        self.word_choice_label = tk.Label(
            word_entry_frame,
            text="--No word submitted--"
        )
        self.word_choice_label.grid(row=3, column=1, columnspan=2)
        #"""


    def file_entered(self):
        file_path = self.file_entry.get()
        self.backend_controller.inputProgram(file_path)
        self.backend_controller.loadProgram()
        self.file_choice_label.config(text=file_path)

    """
    def word_entered(self):
        word = self.word_entry.get()
        self.backend_controller.read_word_from_gui(word)
        self.word_choice_label.config(text=word)
    #"""

