import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import Menu, messagebox


class MemoryPanel:
    def __init__(self, master, interface_with_backend):
        self.master = master
        self.input_to = interface_with_backend
        self.memory_ref = self.input_to.memory.main_memory()

        self.output_frame = tk.Frame(self.master)
        self.output_frame.pack(padx=6, pady=6, fill="both", expand=True)
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        self.memory_box = ScrolledText(
            self.output_frame,
            width=100,
            height=20,
            bg="dark grey",
            fg="white",
            font=("consolas", 10),
            wrap="none",
            insertbackground="white",
            selectbackground="#3399ff",
            selectforeground="white",
            undo=True,          # enable basic undo (Ctrl+Z)
            maxundo=-1          # unlimited undo
        )
        self.memory_box.grid(row=0, column=0, sticky="nsew")

        self.memory_box.config(state="normal")

        # Clipboard support
        self.memory_box.bind("<Control-c>", self.copy)
        self.memory_box.bind("<Control-x>", self.cut)
        self.memory_box.bind("<Control-v>", self.paste)
        self.memory_box.bind("<Control-z>", self.on_undo)  # optional: confirm undo

        # Right-click menu
        self.context_menu = Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy)
        self.context_menu.add_command(label="Cut", command=self.cut)
        self.context_menu.add_command(label="Paste", command=self.paste)
        self.memory_box.bind("<Button-3>", self.show_context_menu)

        # Load initial content once
        self.refresh_memory()

        # Auto-refresh only when not focused (prevents fighting edits)
        self.auto_refresh_id = None
        self.auto_refresh()

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy(self, event=None):
        try:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.memory_box.selection_get())
        except tk.TclError:
            pass
        return "break"

    def cut(self, event=None):
        self.copy()
        try:
            self.memory_box.delete("sel.first", "sel.last")
            self.schedule_sync()
        except tk.TclError:
            pass
        return "break"

    def paste(self, event=None):
        try:
            clipboard = self.master.clipboard_get()
            lines = [line.strip() for line in clipboard.splitlines() if line.strip()]

            if not lines:
                return "break"

            current_lines = self.memory_box.get("1.0", tk.END).strip().splitlines()
            current_count = len([l for l in current_lines if l.strip()])

            if current_count + len(lines) > 100:
                messagebox.showwarning("Memory Limit", "Cannot paste: would exceed 100 memory locations.")
                return "break"

            # Insert at cursor
            self.memory_box.insert(tk.INSERT, clipboard)
            self.schedule_sync()

        except tk.TclError:
            pass
        return "break"

    def schedule_sync(self):
        """Delay sync to backend so rapid edits don't lag."""
        if hasattr(self, 'sync_after_id'):
            self.master.after_cancel(self.sync_after_id)
        self.sync_after_id = self.master.after(300, self.update_memory_from_text)

    def update_memory_from_text(self):
        text = self.memory_box.get("1.0", tk.END).strip()
        lines = text.splitlines()

        # Clear backend
        for i in range(len(self.memory_ref)):
            self.memory_ref[i] = 0

        for i, line in enumerate(lines):
            if i >= 100:
                break
            line = line.strip()
            if not line:
                continue
            # Extract value after colon if present
            if ':' in line:
                try:
                    value_str = line.split(':', 1)[1].strip()
                    self.memory_ref[i] = int(value_str)
                except ValueError:
                    pass  # leave as 0
            else:
                try:
                    self.memory_ref[i] = int(line)
                except ValueError:
                    pass

    def refresh_memory(self):
        scroll_pos = self.memory_box.yview()

        # Skip refresh if user is typing/editing (has focus)
        if self.memory_box.focus_get() == self.memory_box:
            self.memory_box.yview_moveto(scroll_pos[0])
            return

        memory_text = '\n'.join(f'{i}: {x}' for i, x in enumerate(self.memory_ref))

        current = self.memory_box.get("1.0", tk.END).rstrip('\n')
        if current != memory_text:
            pos = self.memory_box.index(tk.INSERT)
            self.memory_box.delete("1.0", tk.END)
            self.memory_box.insert("1.0", memory_text)
            try:
                self.memory_box.mark_set(tk.INSERT, pos)
            except:
                pass

        self.memory_box.yview_moveto(scroll_pos[0])

    def auto_refresh(self):
        self.refresh_memory()
        self.auto_refresh_id = self.master.after(800, self.auto_refresh)  # slower = less intrusive

    def on_undo(self, event=None):
        # Optional: could add confirmation if desired
        return None  # let default undo happen
