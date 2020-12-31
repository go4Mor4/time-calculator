# import packages
import tkinter as tk


class FrameFunctions(tk.Frame):
    def __init__(self, **kwargs):
        tk.Frame.__init__(self)

    def _center_window(self, w=300, h=200):
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y - 50))
