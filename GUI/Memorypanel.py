import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import Menu, messagebox
from tkinter.constants import RIGHT


class MemoryPanel:
    """
    Displays and allows editing of the simulator's 100 memory locations.

    Shows memory contents in a scrollable, editable text area (address: value format).
    Supports cut/copy/paste via keyboard shortcuts and right-click menu.
    Automatically refreshes display from backend memory (when not being edited).
    Changes made in the editor are synced back to the backend memory array.
    Enforces 100-location limit during paste operations.
    """

    def __init__(self, master, interface_with_backend):
        """
        Initialize the memory panel UI and set up editing/clipboard features.

        Args:
            master: Parent Tkinter widget/container
            interface_with_backend: UVSim/CPU instance providing access to memory
        """
        self.master = master
        self.input_to = interface_with_backend
        self.memory_ref = self.input_to.memory.main_memory()


        self.program_canvas = tk.Canvas(self.master)
        self.scrollbar = ttk.Scrollbar(self.master, command=self.program_canvas.yview)
        self.program_frame = ttk.Frame(self.program_canvas)

        #Make sure the program_frame still scrolls when program_canvas resizes:
        self.program_frame.bind("<Configure>", 
                                lambda _: self.program_canvas.configure(
                                    scrollregion=self.program_canvas.bbox("all")))
        self.program_canvas.create_window((0, 0), window=self.program_frame, anchor = "nw")
        self.program_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.program_canvas.pack(fill="both", expand=True)

        self.program_canvas.bind_all("<MouseWheel>", 
                                        lambda e: self.program_canvas.yview_scroll(
                                            int(-1*(e.delta/120)), "units"))



        tk.Label( #Address Label
            self.program_frame,
            height=1,
            width=7,
            text="Address"
        ).grid(row=0, column=0, sticky="nsew")
        tk.Label( #Program Label
            self.program_frame,
            height=1,
            text="      Program",
        ).grid(row=0, column=1, sticky="nsew")

        self.address_box = tk.Label( #renamed from "indexes_box"
            self.program_frame,
            width=7,
            background="light grey",
            fg="black",
            font=("consolas", 10),
            justify="center",
            text='\n'.join([str(n) for n in range(100)])
        )
                
        #self.address_box.config(state=tk.DISABLED)
        self.address_box.grid(row=1, column=0, sticky="nsew")


        #TODO: program_box needn't be scrollable anymore on its own.
        self.program_box = ScrolledText( #renamed from "memory_box"
            self.program_frame,
            width=100,
            #height=20,
            bg="dark grey",
            fg="white",
            font=("consolas", 10),
            wrap="none",
            insertbackground="white",
            selectbackground="#3399ff",
            selectforeground="white",
            undo=True,
            maxundo=-1
        )
        self.program_box.grid(row=1, column=1, sticky="nsew")


        self.program_box.config(state="normal")

        self.program_box.bind("<Control-c>", self.copy)
        self.program_box.bind("<Control-x>", self.cut)
        self.program_box.bind("<Control-v>", self.paste)

        self.context_menu = Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy)
        self.context_menu.add_command(label="Cut", command=self.cut)
        self.context_menu.add_command(label="Paste", command=self.paste)
        self.program_box.bind("<Button-3>", self.show_context_menu)

        self.refresh_memory()
        self.auto_refresh_id = None
        self.auto_refresh()

    def show_context_menu(self, event):
        """Display the right-click context menu at the mouse position."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy(self, event=None):
        """Copy currently selected text to the system clipboard."""
        try:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.program_box.selection_get())
        except tk.TclError:
            pass
        return "break"

    def cut(self, event=None):
        """Cut selected text (copy to clipboard + delete from editor)."""
        self.copy()
        try:
            self.program_box.delete("sel.first", "sel.last")
            self.schedule_sync()
        except tk.TclError:
            pass
        return "break"

    def paste(self, event=None):
        """
        Paste clipboard content at cursor position.
        Checks that total lines won't exceed 100.
        """
        try:
            clipboard = self.master.clipboard_get()
            lines = [line.strip() for line in clipboard.splitlines() if line.strip()]

            if not lines:
                return "break"

            current_lines = self.program_box.get("1.0", tk.END).strip().splitlines()
            current_count = len([l for l in current_lines if l.strip()])

            if current_count + len(lines) > 100:
                messagebox.showwarning("Memory Limit", "Cannot paste: would exceed 100 memory locations.")
                return "break"

            self.program_box.insert(tk.INSERT, clipboard)
            self.schedule_sync()

        except tk.TclError:
            pass
        return "break"

    def schedule_sync(self):
        """Delay backend memory sync by 300ms to batch rapid edits and reduce lag."""
        if hasattr(self, 'sync_after_id'):
            self.master.after_cancel(self.sync_after_id)
        self.sync_after_id = self.master.after(300, self.update_memory_from_text)

    def update_memory_from_text(self):
        """
        Parse current text content of the editor and update backend memory array.
        Clears memory first, then sets values from each line (after colon if present).
        Invalid lines are ignored (left as 0).
        """
        text = self.program_box.get("1.0", tk.END).strip()
        lines = text.splitlines()

        for i in range(len(self.memory_ref)):
            self.memory_ref[i] = 0

        for i, line in enumerate(lines):
            if i >= 100:
                break
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                try:
                    value_str = line.split(':', 1)[1].strip() #TODO: get rid of the extra code for dealing with the indexes and colons
                    self.memory_ref[i] = int(value_str)
                except ValueError:
                    pass
            else:
                try:
                    self.memory_ref[i] = int(line)
                except ValueError:
                    pass

    def refresh_memory(self):
        """
        Update editor content from backend memory if not currently focused.
        Preserves scroll position and cursor location when possible.
        """
        scroll_pos = self.program_box.yview()

        if self.program_box.focus_get() == self.program_box:
            self.program_box.yview_moveto(scroll_pos[0])
            return

        memory_text = '\n'.join(str(data) for data in self.memory_ref)

        current = self.program_box.get("1.0", tk.END).rstrip('\n')
        if current != memory_text:
            pos = self.program_box.index(tk.INSERT)
            self.program_box.delete("1.0", tk.END)
            self.program_box.insert("1.0", memory_text)
            try:
                self.program_box.mark_set(tk.INSERT, pos)
            except:
                pass

        self.program_box.yview_moveto(scroll_pos[0])

    def auto_refresh(self):
        """Periodically refresh display from backend memory (every 800ms)."""
        self.refresh_memory()
        self.auto_refresh_id = self.master.after(800, self.auto_refresh)
