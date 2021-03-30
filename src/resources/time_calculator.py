# import packages
from src.resources.frame_functions import FrameFunctions
import tkinter as tk


class TimeCalculator(FrameFunctions):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        FrameFunctions._screen_elements(self)
        FrameFunctions._apply_configurations(self)
