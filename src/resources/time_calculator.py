# import packages
from src.resources.frame_functions import FrameFunctions
from tkinter import messagebox
from src.utility.environment import Environment
import tkinter as tk
from re import split
from tkinter import *
from datetime import timedelta


class TimeCalculator(FrameFunctions):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.master = master
        FrameFunctions._center_window(self, 450, 330)
        self.master.resizable(False, False)
        self.__screen_elements()
        self.master.iconbitmap(Environment.app_icon_path)
        self.master.title(Environment.app_title)
        self.master.bind("<Escape>", self.__exit)

    def __exit(self, event=None):
        are_you_sure = tk.messagebox.askquestion(Environment.exit_header, Environment.exit_message,
                                                 icon=Environment.exit_icon)
        if are_you_sure == "yes":
            self.master.destroy()

    def __screen_elements(self):
        self.time_entry_text = StringVar()
        self.time_entry = Entry(self, font=("Calibri", 30), border=0, bg="#eee", textvariable=self.time_entry_text)
        self.time_entry.config(state="readonly", justify="center")
        self.time_entry.place(x=10, y=10, height=60, width=270)
        self.time_entry_text.trace("w", lambda *args: self.__entry_validation(self.time_entry_text))

        self.__generate_buttons(self.time_entry_text)

        self.text_box = Text(self, border=0, bg="#eee")
        self.text_box.config(state="disabled")
        self.text_box.place(width=150, height=275, x=290, y=10)

        self.clear_text_box_btn = Button(self, text="clear", fg="#222", highlightthickness=0, font=("Calibri", 10),
                                         border=0, width=21, bg="#54ff9f", activebackground="#28ae7b",
                                         command=self.__clear_text_box).place(x=290, y=292)
        self.get_result_btn = Button(self, text="=", fg="#222", highlightthickness=0, font=("Calibri", 20, "bold"),
                                     border=0, bg="#54ff9f", activebackground="#28ae7b",
                                     command=self.__get_result).place(width=60, height=112, x=220, y=200)
        self.clear_everything = Button(self, text="Ce", fg="#222", highlightthickness=0, font=("Calibri", 20, "bold"),
                                       border=0, bg="#54ff9f", activebackground="#28ae7b",
                                       command=self.__clear_everything).place(width=60, height=52, x=150, y=260)

    def __clear_everything(self):
        self.__clear_text_box()
        self.__clear_time_entry()

    def __clear_text_box(self):
        self.text_box["state"] = "normal"
        self.text_box.delete("1.0", END)
        self.text_box["state"] = "disabled"

    def __generate_buttons(self, event=None):
        y, x = 80, 10
        for key in ("789+", "456-", "123", "C0"):
            for char in key:
                if char == "C":
                    self.__button(char, x, y, self.__clear_time_entry)
                elif char in ["+", "-"]:
                    self.__button(char, x, y, lambda c=str(char): self.__use_operator(self.time_entry.get(), c))
                else:
                    self.__button(char, x, y, lambda c=char: self.__put_value_in_entry(c))
                x += 70
            x = 10
            y += 60

        for number in range(10):
            self.master.bind(str(number), lambda c=str(number): self.__put_value_in_entry(c.char))

    def __get_result(self):
        historic_text = self.text_box.get("1.0", END)
        time_entry_text = self.__autocomplete_entry(self.time_entry.get())
        self.__use_operator(time_entry_text)
        list_calculus = split("([+-])", (historic_text + time_entry_text).replace("\n", ""))
        refactored_calculus = []
        for element in list_calculus:
            if element not in ["+", "-"]:
                time = element.split(":")
                time = [t[1] if t[0] == "0" else t for t in time]
                refactored_calculus.append(f"timedelta(hours={time[0]}, minutes={time[1]}, seconds={time[2]})")
            else:
                refactored_calculus.append(element)
        total_seconds = eval("".join(refactored_calculus)).total_seconds()
        h = str(int(total_seconds // 3600))
        m = str(int((total_seconds % 3600) // 60))
        s = str(int(((total_seconds % 3600) % 60)))
        result = f"{self.__adjust_time_value(h)}:{self.__adjust_time_value(m)}:{self.__adjust_time_value(s)}"
        self.time_entry_text.set(result)

    @staticmethod
    def __adjust_time_value(time: str) -> str:
        if len(time) == 1:
            return f"0{time}"
        return time

    def __use_operator(self, time_entry_text, char=""):
        self.text_box["state"] = "normal"
        self.text_box.insert(END, self.__autocomplete_entry(time_entry_text) + "\n")
        self.text_box.insert(END, char + "\n")
        self.text_box["state"] = "disabled"
        self.__clear_time_entry()

    def __clear_time_entry(self):
        self.time_entry["state"] = "normal"
        self.time_entry.delete(0, "end")
        self.time_entry["state"] = "readonly"

    @staticmethod
    def __autocomplete_entry(text_entry: str) -> str:
        if len(text_entry) != 8:
            if len(text_entry) == 1:
                temp = list(text_entry)
                temp.append(temp[0])
                temp[0] = "0"
                text_entry = "".join(temp)
            completed_text_entry = text_entry.ljust(8, "0")
            temp = list(completed_text_entry)
            temp[2], temp[5] = ":", ":"
            completed_text_entry = "".join(temp)
            return completed_text_entry
        else:
            return text_entry

    def __button(self, text, x, y, command=None):
        w = Button(self, text=text, fg="#222", highlightthickness=0, font=("Calibri", 20, "bold"), border=0, width=4,
                   bg="#54ff9f", activebackground="#28ae7b", command=command)
        w.place(x=x, y=y)

        return w

    def __put_value_in_entry(self, value):
        self.time_entry["state"] = "normal"
        self.time_entry.insert(tk.END, value)
        self.time_entry["state"] = "readonly"

    def __entry_validation(self, entry_text):
        text = entry_text.get()
        entry_text.set(text[:8])

        if len(text) == 2:
            self.time_entry.insert(3, ":")
        elif len(text) == 5:
            self.time_entry.insert(6, ":")
