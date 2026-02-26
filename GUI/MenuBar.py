import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

'''
A Menu Bar object to assist the user with saving, file uploads and a help page. I replaced the large button with the help guide
because this looks a lot better. It has some color changing functionality too.
'''
class MenuBar:
    def __init__(self, master, appUi):
        self.menuBar = tk.Menu(master, bg = "#0A3E0B", fg = "white") #I found out that this might actually be visible in Linux...
        self.master = master
        self.appUi = appUi
        self.master.config(menu = self.menuBar)
        

    def createFileMenu(self):
        fileMenu = tk.Menu(self.menuBar, tearoff = 0)
        fileMenu.add_command(label = "Save CPU state to text file")
        fileMenu.add_command(label = "Exit", command = self.appUi.exitPrompt)

        self.menuBar.add_cascade(label = "File", menu = fileMenu)

    '''
    Creates a theme menu that the user can use to swap out different color themes

    TODO I need to make this a menu that saves the choice to a config file that gets loaded to the program upon start.
    '''
    def createThemeMenu(self):
        themeMenu = tk.Menu(self.menuBar, tearoff = 0)
        themeMenu.add_command(label = "DarkAzure", command = lambda: self.themeCommands(0))
        themeMenu.add_command(label = "DarkCrimson", command = lambda: self.themeCommands(1))
        themeMenu.add_command(label = "DarkGreen", command = lambda: self.themeCommands(2))

        self.menuBar.add_cascade(label = "Theme", menu = themeMenu)

    '''
    Creates a help menu drop down for the tk menu.
    '''
    def createHelpMenu(self):
        helpMenu = tk.Menu(self.menuBar, tearoff = 0)
        helpMenu.add_command(label = "User Help Guide", command = self.show_guide)
        helpMenu.add_command(label = "Version", command = self.versionInfo)

        self.menuBar.add_cascade(label = "Help", menu = helpMenu)

    '''
    Just a silly thing for fun. I made it 0.4 since we will be on the 4th milestone.
    '''
    def versionInfo(self):
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

        text.insert(tk.END, self.helpGuideContent())
        text.config(state="disabled")

        guide_win.bind("<Escape>", lambda e: guide_win.destroy())
        guide_win.protocol("WM_DELETE_WINDOW", guide_win.destroy)

    '''
    Changes the background theme.
    '''
    def themeCommands(self, theme_id):
        match(theme_id):
            case 0:
                color1 = "#2F4880"
                color2 = "#203156"
                self.menuBar.config(bg = color2, fg = "white")
                for panel in self.appUi.panels.values():
                    panel.contentPanel.config(bg = color1)
                    panel.subPanelTitle.config(bg = color2)
                    panel.title.config(bg = color2)

                self.appUi.cpuStatePanel.setColor(color1)
            case 1:
                color1 = "#A13830"
                color2 = "#752823"
                self.menuBar.config(bg = color2, fg = "white")
                for panel in self.appUi.panels.values():
                    panel.contentPanel.config(bg = color1)
                    panel.subPanelTitle.config(bg = color2)
                    panel.title.config(bg = color2)
                
                self.appUi.cpuStatePanel.setColor(color1)
            case 2:
                color1 = "#106511"
                color2 = "#0A3E0B"
                self.menuBar.config(bg = color2, fg = "white")
                for panel in self.appUi.panels.values():
                    panel.contentPanel.config(bg = color1)
                    panel.subPanelTitle.config(bg = color2)
                    panel.title.config(bg = color2)
                
                self.appUi.cpuStatePanel.setColor(color1)

    '''
    This was moved over from the title panel class. I think having this in a menu bar looks cleaner.
    '''
    def helpGuideContent(self):
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
5. Type numbers in pop-ups when READ (10xx) is executed - pop-ups may not always appear on top
"""
        return GUIDE_CONTENT





