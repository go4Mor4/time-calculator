# import packages
from re import split
from src.utility.environment import Environment
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from datetime import timedelta


class FrameFunctions(tk.Frame):
    def _screen_elements(self):
        self.time_entry_text = StringVar()
        self.time_entry = Entry(self, font=("Calibri", 30), border=0, bg="#eee", textvariable=self.time_entry_text)
        self.time_entry.config(state="readonly", justify="center")
        self.time_entry.place(x=10, y=10, height=60, width=270)
        self.time_entry_text.trace("w", lambda *args: self.__entry_validation(self.time_entry_text))

        self.__generate_buttons()

        self.text_box = Text(self, border=0, bg="#eee")
        self.text_box.config(state="disabled")
        self.text_box.place(width=150, height=275, x=290, y=10)

        self.clear_text_box_btn = Button(self, text="clear", fg="#222", highlightthickness=0, font=("Calibri", 10),
                                         border=0, width=21, bg="#54ff9f", activebackground="#28ae7b",
                                         command=self.__clear_text_box).place(x=290, y=292)
        self.get_result_btn = Button(self, text="=", fg="#222", highlightthickness=0, font=("Calibri", 20, "bold"),
                                     border=0, bg="#54ff9f", activebackground="#28ae7b",
                                     command=self.__get_result).place(width=60, height=112, x=220, y=200)
        self.clear_everything_btn = Button(self, text="Ce", fg="#222", highlightthickness=0, font=("Calibri", 20, "bold"),
                                       border=0, bg="#54ff9f", activebackground="#28ae7b",
                                       command=self.__clear_everything).place(width=60, height=52, x=150, y=260)

    def _apply_configurations(self):
        self.master.configure(bg=Environment.bg_color)
        self.master.resizable(False, False)
        self.master.iconbitmap(Environment.app_icon_path)
        self.master.title(Environment.app_title)
        self.master.bind("<Escape>", self.__clear_everything)
        self.master.bind("<Return>", self.__get_result)
        self.master.bind("+", lambda event, c="+": self.__use_operator(char=c))
        self.master.bind("-", lambda event, c="-": self.__use_operator(char=c))
        self.__center_window()

    def __generate_buttons(self):
        y, x = 80, 10
        for key in ("789+", "456-", "123", "C0"):
            for char in key:
                if char == "C":
                    Button(self, text=char, fg="#222", highlightthickness=0, font=("Calibri", 20, "bold"), border=0,
                           width=4, bg="#54ff9f", activebackground="#28ae7b",
                           command=self.__clear_time_entry).place(x=x, y=y)
                elif char in ["+", "-"]:
                    Button(self, text=char, fg="#222", highlightthickness=0, font=("Calibri", 20, "bold"), border=0,
                           width=4, bg="#54ff9f", activebackground="#28ae7b",
                           command=lambda c=str(char): self.__use_operator(c)).place(x=x, y=y)
                else:
                    Button(self, text=char, fg="#222", highlightthickness=0, font=("Calibri", 20, "bold"), border=0,
                           width=4, bg="#54ff9f", activebackground="#28ae7b",
                           command=lambda c=char: self.__put_value_in_entry(c)).place(x=x, y=y)
                x += 70
            x = 10
            y += 60

        for number in range(10):
            self.master.bind(str(number), lambda c=str(number): self.__put_value_in_entry(c.char))

    def __get_result(self, event=None):
        historic_text = self.text_box.get("1.0", END)
        time_entry_text = self.__autocomplete_entry(self.time_entry.get())

        self.text_box["state"] = "normal"
        self.text_box.insert(END, self.__autocomplete_entry(time_entry_text) + "\n")
        self.text_box["state"] = "disabled"

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

    def __entry_validation(self, entry_text: StringVar):
        text = entry_text.get()
        entry_text.set(text[:8])

        if len(text) == 2:
            self.time_entry.insert(3, ":")
        elif len(text) == 5:
            self.time_entry.insert(6, ":")

    def __center_window(self, w: int = 450, h: int = 330):
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y - 50))

    def __clear_everything(self, event=None):
        self.__clear_text_box()
        self.__clear_time_entry()

    def __clear_text_box(self):
        self.text_box["state"] = "normal"
        self.text_box.delete("1.0", END)
        self.text_box["state"] = "disabled"

    def __clear_time_entry(self, event=None):
        self.time_entry["state"] = "normal"
        self.time_entry.delete(0, "end")
        self.time_entry["state"] = "readonly"

    def __use_operator(self, char: str = "", event=None):
        time_entry_text = self.time_entry.get()
        self.text_box["state"] = "normal"
        self.text_box.insert(END, self.__autocomplete_entry(time_entry_text) + "\n")
        self.text_box.insert(END, char + "\n")
        self.text_box["state"] = "disabled"
        self.__clear_time_entry()

    def __put_value_in_entry(self, value: float):
        self.time_entry["state"] = "normal"
        self.time_entry.insert(tk.END, value)
        self.time_entry["state"] = "readonly"

    def __exit(self, event=None):
        are_you_sure = tk.messagebox.askquestion(Environment.exit_header, Environment.exit_message,
                                                 icon=Environment.exit_icon)
        if are_you_sure == "yes":
            self.master.destroy()

    @staticmethod
    def __adjust_time_value(time: str) -> str:
        if len(time) == 1:
            return f"0{time}"
        return time

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
