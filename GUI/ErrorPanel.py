import tkinter as tk
'''
The color of this window is dictated by the subpanel class.
'''
class ErrorPanel:
    def __init__(self, master, cpu):
        self.cpu = cpu
        self.master = master
        
        self.mainLabel = tk.Label(master, text = "", bg = "darkgrey", fg = "black", font = ("Arial", 14))
        self.mainLabel.pack(expand = False, fill = "both")
        self.update()

    def update(self):
        if hasattr(self.cpu, "errorMessage") and self.cpu.errorMessage:
            self.mainLabel.config(text = self.cpu.errorMessage)
        else:
            self.mainLabel.config(text = "No errors")
        self.master.after(100, self.update)