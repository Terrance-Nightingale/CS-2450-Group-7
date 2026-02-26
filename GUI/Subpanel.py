import tkinter as tk

# Creates panels in the content panels. One should hold a title and the other should be holding the contents of the UV sim with the corresponding title.
# The panel that holds the information should be changed depending on what the subPanelTitle is.
class Subpanel:
    def __init__(self, container, title, buttons = None):
        self.subPanelTitle = tk.Frame(container, borderwidth = 1, bg = "#0A3E0B", height = 80)
        self.subPanelTitle.grid(row = 0, column = 0, sticky = "nsew")
        self.subPanelTitle.pack_propagate(False)

        self.title = tk.Label(self.subPanelTitle, text = title, bg = "#0A3E0B", fg = "white", font = ("Arial", 16))
        self.title.pack(expand = False, fill = "both")

        self.contentPanel = tk.Frame(container, borderwidth = 2, bg = "#106511")
        self.contentPanel.grid(row = 1, column = 0, sticky = "nsew")

        self.statusLabel = tk.Label(self.contentPanel, text = title, bg = "#106511", font = ("Arial", 16))
        self.statusLabel.pack(expand = False)

        if buttons:
            for button in buttons:
                tk.Button(self.contentPanel, command = button['command'], text = button['name'] , font = ("Arial", 16)).pack(fill="x", padx = 5, pady = 5)