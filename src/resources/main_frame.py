from src.resources.time_calculator import TimeCalculator
from src.utility.environment import Environment
import tkinter as tk
from tkinter import *


class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = TimeCalculator(self)
        self.frame["bg"] = Environment.bg_color
        self.frame.pack(fill=BOTH, expand=1)
