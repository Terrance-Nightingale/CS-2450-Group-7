import tkinter as tk
from tkinter import scrolledtext


class TitlePanel:
    GUIDE_CONTENT = """\
UVSim Guide
───────────
Quick overview of what you see:

• Input / Input Info      → Where your program file is loaded or shown
• CPU State               → Displays Accumulator, Program Counter, Instruction Register
• Error Reports           → Shows any loading or runtime errors
• Memory                  → View of all 100 memory locations (program + data)
• Controls                → Buttons to RUN (execute fully) or RESET (clear everything)

How to use:
1. Load your BasicML program (via Input area if not already done)
2. Click RUN to execute until HALT or error
3. Use RESET to start over
4. Watch CPU State and Memory update as it runs
5. Type numbers in console when READ (10xx) is executed
"""

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

        tk.Button(
            self.panel,
            text="UVSim Guide",
            font=("Arial", 16),
            command=self.show_guide
        ).pack(side="right", padx=10, pady=10)

    def show_guide(self):
        guide_win = tk.Toplevel(self.master)
        guide_win.title("UVSim Guide")
        guide_win.geometry("680x520")
        guide_win.minsize(580, 420)
        guide_win.configure(bg="#f8f8f8")
        guide_win.transient(self.master)

        text = scrolledtext.ScrolledText(
            guide_win,
            wrap=tk.WORD,
            font=("Consolas", 11),
            padx=14, pady=14,
            bg="white",
            fg="#111",
            spacing1=4,
            spacing2=2,
            spacing3=4
        )
        text.pack(fill="both", expand=True)

        text.insert(tk.END, self.GUIDE_CONTENT)
        text.config(state="disabled")

        guide_win.bind("<Escape>", lambda e: guide_win.destroy())
        guide_win.protocol("WM_DELETE_WINDOW", guide_win.destroy)
