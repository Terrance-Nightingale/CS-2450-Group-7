import tkinter as tk


class InputInfoPanel:
    def __init__(self, container, interface_with_backend):
        self.input_to = interface_with_backend
        self.container = container
        self.prev_inputs = ["These", "Are", "some", "inputs", "oh", "Three", "More"]

        tk.Label(
            self.container,
            text="Previous user inputs:"
            ).pack(padx=5, pady=5)

        self.prev_inputs_label = tk.Label(
            self.container,
            text=""
        )
        self.prev_inputs_label.pack(padx=5, pady=5)
        self.update_prev_inputs_disp()

    def update_prev_inputs_disp(self):
        output = ""
        for line in self.prev_inputs:
            output = output + line + "\n"
        self.prev_inputs_label.config(text=output)

    def add_prev_inputs(self, recent_input):
        self.prev_inputs.insert(0, recent_input)
        self.update_prev_inputs_disp()

