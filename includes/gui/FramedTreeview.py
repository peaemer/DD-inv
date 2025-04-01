"""
    .
"""
import tkinter
from tkinter import ttk
import customtkinter

from includes.gui._styles import scroll_corner, srh_grey
from includes.windows import sort_column


class FramedTreeview(tkinter.Frame):
    """
        .
    """
    def __init__(self, parent, columns:list[tuple[str,str, int]]):
        super().__init__(self, parent)

        self.treeview = ttk.Treeview(
            self,
            columns=("c1", "c2", "c3", "c4", "c5"),
            show="headings",
            cursor="hand2"
        )
        self.scrollbar = customtkinter.CTkScrollbar(
            self,
            orientation="vertical",
            command=self.treeview.yview,
            fg_color="white",
            width=20,
            corner_radius=scroll_corner,
            button_color = srh_grey,
            button_hover_color="#2980b9"
        )

        self.treeview.grid(row=1, column=0, sticky='NS')  # Scrollbar genau neben der Tabelle
        self.scrollbar.grid(row=1, column=1, sticky='NS')

        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=0)


        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.treeview.tag_configure("oddrow", background="#f7f7f7")
        self.treeview.tag_configure("evenrow", background="white")

        for col_id, col_name, col_width in columns:
            self.treeview.column(col_id, anchor=tkinter.CENTER, width=col_width)
            self.treeview.heading(col_id, text=col_name, command=lambda c=col_id:sort_column(self.treeview, c, False))