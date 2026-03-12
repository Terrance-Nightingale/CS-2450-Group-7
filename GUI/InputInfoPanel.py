import tkinter as tk

class InputInfoPanel:
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

    def update_prev_inputs(self, recent_input):
        self.inputs_history.append(recent_input)
        self.prev_inputs_label.config(text="\n".join(self.inputs_history))

