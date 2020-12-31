from src.resources.time_calculator import TimeCalculator
import tkinter as tk
from tkinter import *


class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = TimeCalculator(self)
        self.frame["bg"] = "#222"
        self.frame.pack(fill=BOTH, expand=1)
