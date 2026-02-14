import tkinter as tk

# Creates panels in the content panels. One should hold a title and the other should be holding the contents of the UV sim with the corresponding title.
# The panel that holds the information should be changed depending on what the subPanelTitle is.
class Subpanel:
    def __init__(self, container, title, buttons = None):
        self.subPanelTitle = tk.Frame(container, borderwidth = 1, relief = "solid", bg = "white", height = 80)
        self.subPanelTitle.grid(row = 0, column = 0, sticky = "nsew")
        self.subPanelTitle.pack_propagate(False)
        tk.Label(self.subPanelTitle, text = title, bg = "darkgrey", font = ("Arial", 16)).pack(expand = True, fill = "both")

        self.contentPanel = tk.Frame(container, borderwidth = 2, relief = "solid", bg = "white")
        self.contentPanel.grid(row = 1, column = 0, sticky = "nsew")

        self.statusLabel = tk.Label(self.contentPanel, text = title, bg = "darkgrey", font = ("Arial", 16))
        self.statusLabel.pack(expand = True, fill = "both")

        if buttons:
            for text in buttons:
                #change the lambda: None to the actual button function
                tk.Button(self.contentPanel, command = lambda: None, text = text , font = ("Arial", 16)).pack(fill="x", padx = 5, pady = 5)