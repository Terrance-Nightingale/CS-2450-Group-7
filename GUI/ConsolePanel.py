import tkinter as tk

class ConsolePanel:
    def __init__(self, container, uvsim):
        self.container = container

        self.label = tk.Label(
            self.container,
            text="Program Outputs:",
            font=("Segoe UI", 11, "bold"), 
            width=30,
            anchor="w", 
            justify="left",
            padx=8,
            pady=6
        )
        self.label.grid(row=0, column=0, columnspan=2, sticky="w")

        self.prev_inputs_label = tk.Label(
            self.container,
            text="Program Outputs will appear here..."
        )
        self.prev_inputs_label.grid(row=1, column=0, columnspan=2)

        self.inputs_history = []

    def update_prev_outputs(self, new_input):
        self.inputs_history.append(new_input)
        self.prev_inputs_label.config(text="\n".join(self.inputs_history))
    
    def reset_outputs(self):
        self.inputs_history = []
        self.prev_inputs_label.config(text="Program Outputs will appear here...")
