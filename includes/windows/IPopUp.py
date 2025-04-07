import math
import tkinter
import tkinter as tk
from abc import ABC, abstractmethod
from typing import Tuple, Callable, Any

from includes.gui.styles import srh_orange, srh_blue
from includes.util import Paths
from includes.util.Logging import Logger

logger: Logger = Logger('IPopUp')


class IPopUp(tk.Toplevel, ABC):
    """
        an abstract base class for the Popups

        :ivar header_frame:
        :ivar content_frame: a frame that each subclass can freely adjust and ad widgets to
        :ivar buttons_frame:

        :ivar header_button:
        :ivar header_label:
        :ivar buttons: a row of buttons at the bottom of the popup
        :ivar button_images: a list of PhotoImages where each photo is associated with one of the bottom buttons
    """

    def __set_size(self, parent: tkinter.Toplevel, size: tuple[int, int] = None):
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        center_x = int(screen_width / 2)
        center_y = int(screen_height / 2)

        if size is not None:
            center_x -= int(math.floor(size[0] / 2))
            center_y -= int(math.floor(size[1] / 2))
            self.geometry(f"{size[0]}x{size[1]}+{center_x}+{center_y}")
        else:
            center_x -= int(math.floor(screen_width / 2))
            center_y -= int(math.floor(screen_height / 2))
            self.geometry(f"{screen_width}x{screen_height}+{center_x}+{center_y}")
        self.resizable(False, False)

    def __set_bottom_buttons(self, buttons_: list[tuple[str | tkinter.PhotoImage, Callable | None]] = None):
        """
            Creates a frame with a row of buttons at the bottom of the popup.
            Each button is stored inside the buttons_list, and its picture os text is stored inside the button_images list

            :param list[tuple[str | tkinter.PhotoImage, Callable | None]] buttons_:
        """
        self.buttons: list[tkinter.Button] = []
        self.button_images: list[tkinter.PhotoImage | str] = []
        self.buttons_frame: tk.Frame = tk.Frame(
            self,
            height=10,
            background='white'
        )

        self.buttons_frame.grid(row=2, column=0, columnspan=3, pady=20, sticky="SWE")
        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=2)

        for i in range(0, len(buttons_)):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
            self.button_images.append(buttons_[i][0] if isinstance(buttons_[i][0], tkinter.PhotoImage) else None)
            self.buttons.append(
                tk.Button(
                    self.buttons_frame,
                    image=self.button_images[i],
                    bd=0,
                    relief=tk.FLAT,
                    bg="white",
                    cursor="hand2",
                    activebackground="white",
                    command=buttons_[i][1]
                )
            )
            self.buttons[i].grid(row=0, column=i)

    def __set_header(self, header_text='', header_button:tuple[str|tkinter.PhotoImage, Callable]= ('',None)):
        """
            Creates a frame with the strip at the top of the popup with a set text and
            an optional button at the left of the text.

            :param str header_text:
            :param tuple[str | tkinter.PhotoImage, Callable | None] header_button:
        """
        self.header_label = tk.Label(
            self.header_frame,
            background=srh_blue if self.admin_mode == True else srh_orange,
            text=header_text,
            foreground='white',
            font=("Arial", 40)
        )

        if header_button is not None:
            self.header_button_image: tkinter.PhotoImage = header_button[0] if isinstance(header_button[0], tkinter.PhotoImage) else None
            self.header_button = tkinter.Button(
                self.header_frame,
                image=self.header_button_image,
                text=header_button[0] if isinstance(header_button[0], str) else None,
                background = srh_blue if self.admin_mode else srh_orange,
                activebackground = srh_blue if self.admin_mode == True else srh_orange,
                bd=0,
                relief=tk.FLAT,
                command=header_button[1]
            )

            self.header_button.grid(row=0, column=0, sticky="NSWE")
            self.header_label.grid(row=0, column=2, sticky="NS")

            self.header_frame.grid_columnconfigure(0, weight=1)
            self.header_frame.grid_columnconfigure(1, weight=0)
            self.header_frame.grid_columnconfigure(2, weight=1)
            self.header_frame.grid_columnconfigure(3, weight=1)
        else:
            self.header_frame.grid_columnconfigure(0, weight=1)
            self.header_frame.grid_columnconfigure(1, weight=0)
            self.header_frame.grid_columnconfigure(2, weight=1)
            self.header_label.grid(row=0, column=1, sticky="NS")

    @abstractmethod
    def add_content(self, content_frame: tk.Frame) -> None:
        """
            Subclasses must implement this method, to add the actual content to the content_frame of the popup.
        """

    def __init__(
            self,
            parent: tkinter.Toplevel,
            title: str = 'IPopUp',
            header_text: str = 'IPopUp',
            background:str = 'white',
            size:tuple[int, int] = None,
            admin_mode:bool = False,
            header_button:tuple[str|tkinter.PhotoImage, Callable|None] = None,
            buttons:list[tuple[str|tkinter.PhotoImage, Callable|None]] = None,
    ):
        """
            :param TopLevel parent:
            :param str header_text:
            :param str title:
            :arg str background:
            :param bool admin_mode:
            :param list[tuple[str | tkinter.PhotoImage, Callable | None]] buttons:
            :param tuple[str | tkinter.PhotoImage, Callable | None] header_button:
            :param tuple[int,int] size:

        """
        super().__init__(parent, background=background)

        self.admin_mode = admin_mode

        self.transient(parent)
        self.title(title)
        self.grab_set()
        self.attributes('-topmost', 0)
        self.__set_size(parent, size)

        self.iconbitmap(Paths.assets_path("srhIcon.ico"))

        self.content_frame: tk.Frame = tk.Frame(
            self,
            height=10,
            background=background
        )
        self.header_frame = tk.Frame(
            self,
            height=10,
            background=srh_blue if admin_mode == True else srh_orange
        )

        self.__set_header(header_text, header_button)

        self.__set_bottom_buttons(buttons)

        self.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.header_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="NWE")
        self.content_frame.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="NSWE" if hasattr(self, 'buttons_frame') else "SWE"
        )

        non_blocking_add_content_command:Callable = self.add_content

        def block_add_content():
            """
                does nothing but raising an error.
            """
            raise RuntimeError("add_content should not be called outside of IPopup")


        self.add_content = block_add_content
        self.after(0, non_blocking_add_content_command, self.content_frame)


class SimpleMessageBox(IPopUp):

    def add_content(self, content_frame: tk.Frame) -> None:
        pass

    def __init__(self, parent: tkinter.Toplevel, title: str = 'MessageBox', message:str='Info', admin_mode:bool = False):
        super().__init__(parent, title=title, admin_mode=admin_mode)