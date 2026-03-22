import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import os
import json

'''
A Menu Bar object to assist the user with saving, file uploads and a help page. I replaced the large button with the help guide
because this looks a lot better. It has some color changing functionality too.
'''

CONFIG_FILE = "config.json"

class MenuBar:
    def __init__(self, master, app_ui):
        self.menu_bar = tk.Menu(master, bg = "#0A3E0B", fg = "white") #I found out that this might actually be visible in Linux...
        self.master = master
        self.app_ui = app_ui
        self.master.config(menu = self.menu_bar)
        saved_theme = self.load_config()
        self.theme_commands(saved_theme)
        

    def create_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff = 0)
        file_menu.add_command(label = "Save CPU state to text file", command = self.app_ui.controller.save_program)
        file_menu.add_command(label = "Exit", command = self.app_ui.exit_prompt)

        self.menu_bar.add_cascade(label = "File", menu = file_menu)

    '''
    Creates a theme menu that the user can use to swap out different color themes

    TODO I need to make this a menu that saves the choice to a config file that gets loaded to the program upon start.
    '''
    def create_theme_menu(self):
        theme_menu = tk.Menu(self.menu_bar, tearoff = 0)
        theme_menu.add_command(label = "DarkAzure", command = lambda: self.theme_commands(0))
        theme_menu.add_command(label = "DarkCrimson", command = lambda: self.theme_commands(1))
        theme_menu.add_command(label = "DarkGreen", command = lambda: self.theme_commands(2))

        self.menu_bar.add_cascade(label = "Theme", menu = theme_menu)

    '''
    Creates a help menu drop down for the tk menu.
    '''
    def create_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff = 0)
        help_menu.add_command(label = "User Help Guide", command = self.show_guide)
        help_menu.add_command(label = "Version", command = self.version_info)

        self.menu_bar.add_cascade(label = "Help", menu = help_menu)

    '''
    Just a silly thing for fun. I made it 0.4 since we will be on the 4th milestone.
    '''
    def version_info(self):
        tk.messagebox.showinfo("Version info", "UVSim version 0.4")
    '''
    Copied this over from the TitleBarClass. A menu bar with dropdowns just made more sense.
    '''
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

        text.insert(tk.END, self.help_guide_content())
        text.config(state="disabled")

        guide_win.bind("<Escape>", lambda e: guide_win.destroy())
        guide_win.protocol("WM_DELETE_WINDOW", guide_win.destroy)

    '''
    Changes the background theme.
    '''
    def theme_commands(self, theme_id):
        match(theme_id):
            case 0:
                color1 = "#2F4880"
                color2 = "#203156"
                self.menu_bar.config(bg = color2, fg = "white")
                for panel in self.app_ui.panels.values():
                    panel.content_panel.config(bg = color1)
                    panel.sub_panel_title.config(bg = color2)
                    panel.title.config(bg = color2)

                self.app_ui.cup_state_panel.setColor(color1)
            case 1:
                color1 = "#591303"
                color2 = "#6E1804"
                self.menu_bar.config(bg = color2, fg = "white")
                for panel in self.app_ui.panels.values():
                    panel.content_panel.config(bg = color1)
                    panel.sub_panel_title.config(bg = color2)
                    panel.title.config(bg = color2)
                
                self.app_ui.cup_state_panel.setColor(color1)
            case 2:
                color1 = "#106511"
                color2 = "#0A3E0B"
                self.menu_bar.config(bg = color2, fg = "white")
                for panel in self.app_ui.panels.values():
                    panel.content_panel.config(bg = color1)
                    panel.sub_panel_title.config(bg = color2)
                    panel.title.config(bg = color2)
                
                self.app_ui.cup_state_panel.setColor(color1)

        self.save_config(theme_id)

    def save_config(self, theme_id):
        config = {"theme_id": theme_id}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    return config.get("theme_id", 0)
            except json.JSONDecodeError:
                return 0;

    '''
    This was moved over from the title panel class. I think having this in a menu bar looks cleaner.
    '''
    def help_guide_content(self):
        GUIDE_CONTENT = """\
UVSim Guide
───────────
Quick overview of what you see:
• Input / Console         → Where your program file is loaded or shown
• CPU State               → Displays Accumulator, Program Counter, Instruction Register
• Error Reports           → Shows any loading or runtime errors
• Memory                  → View of all 100 memory locations (program + data)
• Controls                → Buttons to RUN (execute fully), RESET (clear everything), SAVE (save memory to a text file)
            
How to use:
1. Load your BasicML program (via Input area if not already done)
2. Click RUN to execute until HALT or error
3. Use RESET to start over
4. Watch CPU State and Memory update as it runs
5. Type numbers in pop-ups when READ (10xx) is executed - pop-ups may not always appear on top
6. Type your own code in the Memory panel and press SAVE to save it to a .txt file
"""
        return GUIDE_CONTENT





