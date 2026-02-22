import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from Backend.Memory import Memory

class MemoryPanel:
    def __init__(self, master, interface_with_backend):
        self.master = master
        self.input_to = interface_with_backend
        memory = Memory()
        self.memory_ref = self.input_to.memory.mainmemory()
        self.memory = "\n".join(
            f'{i}: {x}'
            for i, x in enumerate(self.memory_ref, start=1)
            )
        self.output_frame = tk.Frame(
            self.master
        )
        self.output_frame.pack(padx=6, pady=6)

        self.memory_box = ScrolledText(
            self.output_frame,
            width=100,
            height=20,
            bg="dark grey",
            font=("consolas", 10),
            wrap="none"
        )
    
        self.memory_box.grid(row=0, column=0, sticky='nsew')
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.memory_box.insert("1.0", self.memory)
        self.memory_box.config(state="disabled")
        self.refresh_memory()
        self.auto_refresh()


    def refresh_memory(self):
        scroll_pos = self.memory_box.yview()
        memory_text = '\n'.join(
            f'{i}: {x}'
            for i, x in enumerate(self.memory_ref)#, start=1)
        )
        self.memory_box.config(state="normal")
        self.memory_box.delete("1.0", tk.END)
        self.memory_box.insert("1.0", memory_text)
        self.memory_box.config(state="disabled")
        self.memory_box.yview_moveto(scroll_pos[0])

    def auto_refresh(self):
        self.refresh_memory()
        self.master.after(500, self.auto_refresh)
