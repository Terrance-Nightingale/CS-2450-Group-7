import tkinter as tk
'''
The color of this window is dictated by the subpanel class.
'''
class ErrorPanel:
    def __init__(self, master, cpu):
        self.cpu = cpu
        self.master = master
        
        self.main_label = tk.Label(master, text = "", bg = "darkgrey", fg = "black", font = ("Arial", 14))
        self.main_label.pack(expand = False, fill = "both")
        self.update()

    def update(self):
        if hasattr(self.cpu, "errorMessage") and self.cpu.errorMessage:
            self.main_label.config(text = self.cpu.errorMessage)
        else:
            self.main_label.config(text = "No errors")
        self.master.after(100, self.update)
        