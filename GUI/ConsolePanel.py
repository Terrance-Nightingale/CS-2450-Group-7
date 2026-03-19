import tkinter as tk

class ConsolePanel:
    def __init__(self, container, interface_with_backend):
        self.input_to = interface_with_backend
        self.container = container

        tk.Label(
            self.container,
            text="Previous inputs:"
            ).grid(row=0, column=0)

        self.prev_inputs_label = tk.Label(
            self.container,
            text="Previous inputs will appear here..."
        )
        self.prev_inputs_label.grid(row=1, column=0, columnspan=2)

        self.inputs_history = []

    def update_prev_inputs(self, new_input):
        self.inputs_history.append(new_input)
        self.prev_inputs_label.config(text="\n".join(self.inputs_history))
    
    def reset_inputs(self):
        self.inputs_history = []
        self.prev_inputs_label.config(text="Previous inputs will appear here...")
