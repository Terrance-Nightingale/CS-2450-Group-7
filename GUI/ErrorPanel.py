import tkinter as tk

class ErrorPanel:
    def __init__(self, master, cpu):
        self.cpu = cpu
        self.master = master
        self.errorLabel = tk.Label(master, text="", bg="darkgrey", fg="black", font=("Arial", 14))
        self.errorLabel.pack(expand=True, fill="both")
        self.update()

    def update(self):
        if hasattr(self.cpu, "errorMessage") and self.cpu.errorMessage:
            self.errorLabel.config(text=self.cpu.errorMessage)
        else:
            self.errorLabel.config(text="No errors")
        self.master.after(100, self.update)