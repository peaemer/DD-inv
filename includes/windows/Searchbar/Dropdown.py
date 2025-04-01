"""
    .
"""
import tkinter
import customtkinter

'''
Advanced Scrollable Dropdown Frame class for customtkinter widgets
Author: Akash Bora
'''

import customtkinter
import sys
import difflib

from customtkinter import CTkComboBox


class CTkScrollableDropdownFrame(customtkinter.CTkFrame):

    def __init__(self, attach, x=None, y=None, button_color=None, height: int = 200, width: int = None,
                 fg_color=None, button_height: int = 20, justify="center", scrollbar_button_color=None,
                 scrollbar=True, scrollbar_button_hover_color=None, frame_border_width=2, values=None,
                 command=None, image_values=None, double_click=False, frame_corner_radius=True, resize=True,
                 frame_border_color=None,
                 text_color=None, autocomplete=False, **button_kwargs):

        super().__init__(master=attach.winfo_toplevel(), bg_color=attach.cget("bg_color"))

        if values is None:
            values = []
        if image_values is None:
            image_values = []
        self.attach = attach
        self.corner = 11 if frame_corner_radius else 0
        self.padding = 0
        self.disable = True

        self.hide = True
        self.attach.bind('<Configure>', lambda e: self._withdraw() if not self.disable else None, add="+")
        self.attach.winfo_toplevel().bind("<ButtonPress>", lambda e: self._withdraw() if not self.disable else None,add="+")
        self.bind("<Escape>", lambda e: self._withdraw() if not self.disable else None, add="+")

        self.disable = False
        self.fg_color = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"] if fg_color is None else fg_color
        self.frame_border_color = customtkinter.ThemeManager.theme["CTkFrame"][
            "border_color"] if frame_border_color is None else frame_border_color

        self.frame = customtkinter.CTkScrollableFrame(self, fg_color=self.fg_color, bg_color=attach.cget("bg_color"),
                                                      corner_radius=self.corner, border_width=frame_border_width,
                                                      border_color=self.frame_border_color)
        self.frame.pack(expand=True, fill="both")

        if self.corner == 0:
            self.corner = 21

        self.height = height
        self.height_new = height
        self.width = width
        self.fade = False
        self.resize = resize
        self.appear = False

        if justify.lower() == "left":
            self.justify = "w"
        elif justify.lower() == "right":
            self.justify = "e"
        else:
            self.justify = "c"

        self.x = x
        self.y = y

        self.attach.bind("<Destroy>", lambda _: self._destroy(), add="+")



    def _destroy(self):
        self.after(500, self.destroy_popup)

    def _withdraw(self):
        if self.winfo_viewable() and self.hide:
            self.place_forget()

        self.event_generate("<<Closed>>")
        self.hide = True

    def _update(self, a, b, c):
        self.live_update(self.attach._entry.get())

    def destroy_popup(self):
        self.destroy()
        self.disable = True

    # wip

    def place_dropdown(self):
        self.x_pos = self.attach.winfo_x() if self.x is None else self.x + self.attach.winfo_rootx()
        self.y_pos = self.attach.winfo_y() + self.attach.winfo_reqheight() + 5 if self.y is None else self.y + self.attach.winfo_rooty()
        self.width_new = self.attach.winfo_width() - 45 + self.corner if self.width is None else self.width

        # Determine the parent widget of self.attach
        parent_name = self.attach.winfo_parent()
        parent_widget = self.nametowidget(parent_name)

        # Check if the parent widget is a frame
        import tkinter as tk
        if isinstance(parent_widget, tk.Frame):
            self.x_pos = parent_widget.winfo_x() + self.attach.winfo_x()
            self.y_pos = parent_widget.winfo_y() + self.attach.winfo_y() + self.attach.winfo_reqheight() + 5  # Box höhe

        if self.resize:
            if self.button_num <= 5:
                self.height_new = self.button_height * self.button_num + 55
            else:
                self.height_new = self.button_height * self.button_num + 35
            if self.height_new > self.height:
                self.height_new = self.height

        self.frame.configure(width=self.width_new, height=self.height_new)
        self.frame._scrollbar.configure(height=self.height_new)
        self.place(x=self.x_pos, y=self.y_pos)

        if sys.platform.startswith("darwin"):
            self.dummy_entry.pack()
            self.after(100, self.dummy_entry.pack_forget())

        self.lift()
        self.attach.focus()



class Dropdown(tkinter.Toplevel):
    """
        .
    """
    def __init__(self, attach:tkinter.Misc):
        super().__init__(self)
        self.configure(width=100, height=100, background='blue')
        self.geometry('100x100')
