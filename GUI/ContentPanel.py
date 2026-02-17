import tkinter as tk
from GUI.Subpanel import Subpanel

# Holds the subpanel content.

class ContentPanel:
    def __init__(self, container, title, buttons = None):
        self.container = tk.Frame(container, borderwidth = 1, relief = "solid", bg = "black")
        self.container.rowconfigure(0, weight = 0, minsize = 80)
        self.container.rowconfigure(1, weight = 1)
        self.container.columnconfigure(0, weight = 1)
        self.subPanel = Subpanel(self.container, title, buttons)

    def grid(self, row, col):
        self.container.grid(row = row, column = col, sticky = "nsew", padx = 5, pady = 5)