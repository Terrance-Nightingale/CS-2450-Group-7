import tkinter as tk
from GUI.TitlePanel import TitlePanel
from GUI.ContentPanel import ContentPanel
from GUI.CPUStatePanel import CPUStatePanel
from GUI.InputPanel import InputPanel
from GUI.InputInfoPanel import InputInfoPanel
from GUI.Memorypanel import MemoryPanel
from GUI.ErrorPanel import ErrorPanel
from GUI.MenuBar import MenuBar

class AppUI:
    def __init__(self, window, controller, uvsim):
        self.uvsim = uvsim
        self.window = window
        self.window.title("UVSim")
        self.window.configure(bg = "darkgrey")
        self.panels = {}

        self.controller = controller

        self.subPanelNames = ["Input", "CPU State", "Error Reports", "Input Info", "Memory", "Controls"]

        #self.titlePanel = TitlePanel(window)

        self.container = tk.Frame(window)
        self.container.pack(expand = True, fill = "both")

        for i in range(2):
            self.container.rowconfigure(i, weight = 1)

        for i in range(3):
            self.container.columnconfigure(i, weight = 1)

        self.createGridPanels()

        menu = MenuBar(self.window, self)
        menu.createFileMenu()
        menu.createThemeMenu()
        menu.createHelpMenu()

    def createGridPanels(self):
        for index, name in enumerate(self.subPanelNames):
            row = index // 3
            col = index % 3
            buttons = None

            if name == "Controls":
                buttons = [
                    {
                        'name': 'RUN',
                        'command': self.controller.runProgram
                    },

                    {
                        'name': 'RESET',
                        'command': self.controller.resetProgram
                    }
                ]

            panel = ContentPanel(self.container, name, buttons)
            panel.grid(row, col)

            self.panels[name] = panel.subPanel
            
            if name == "CPU State":
                panel.subPanel.statusLabel.destroy()
                self.cpuStatePanel = CPUStatePanel(panel.subPanel.contentPanel, self.uvsim.cpu)
        
            if name == "Controls":
                panel.subPanel.statusLabel.destroy()

            if name == "Input":
                panel.subPanel.statusLabel.destroy()
                InputPanel(panel.subPanel.contentPanel, self.uvsim)

            if name == "Input Info":
                panel.subPanel.statusLabel.destroy()
                InputInfoPanel(panel.subPanel.contentPanel, self.uvsim)

            if name == "Memory":
                panel.subPanel.statusLabel.destroy()
                MemoryPanel(panel.subPanel.contentPanel, self.uvsim.cpu)

            if name == "Error Reports":
                panel.subPanel.statusLabel.destroy()
                

    '''
    This will create an exit prompt upon clicking the "Exit" option in the File menu selection
    '''
    def exitPrompt(self):
        areYouSure = tk.messagebox.askyesno("Exiting UVSim", "Are you sure you want to exit?")
        
        if areYouSure:
            self.window.destroy()
        else:
            pass

            
