import tkinter as tk

# Creates panels in the content panels. One should hold a title and the other should be holding the contents of the UV sim with the corresponding title.
# The panel that holds the information should be changed depending on what the subPanelTitle is.
class Subpanel:
    def __init__(self, container, title, buttons = None):
        self.sub_panel_title = tk.Frame(container, borderwidth = 1, bg = "#0A3E0B", height = 30)
        self.sub_panel_title.grid(row = 0, column = 0, sticky = "nsew")
        self.sub_panel_title.pack_propagate(False)

        self.title = tk.Label(self.sub_panel_title, text = title, bg = "#0A3E0B", fg = "white", font = ("Arial", 16))
        self.title.pack(expand = False, fill = "both")

        self.content_panel = tk.Frame(container, borderwidth = 2, bg = "#106511")
        self.content_panel.grid(row = 1, column = 0, sticky = "nsew")

        self.status_label = tk.Label(self.content_panel, text = title, bg = "#106511", font = ("Arial", 16))
        self.status_label.pack(expand = False)
