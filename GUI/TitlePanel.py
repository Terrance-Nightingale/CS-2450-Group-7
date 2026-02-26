import tkinter as tk
from tkinter import scrolledtext


class TitlePanel:

    def __init__(self, master):
        self.master = master
        self.panel = tk.Frame(
            master,
            borderwidth=2,
            relief="solid",
            bg="black",
            height=80
        )
        self.panel.pack(fill="x", padx=10, pady=10)
        self.panel.pack_propagate(False)

        tk.Label(
            self.panel,
            text="UVSimulator",
            font=("Arial", 16),
            bg="black",
            fg="white"
        ).pack(side="left", padx=10, pady=10)
