"""
    .
"""
import tkinter
from abc import ABC, abstractmethod

from includes.windows.styles import srh_orange, srh_blue

class IWindow(tkinter.Frame, ABC):
    """
        This is the base class for all window frames. It sets up the general arrangement of the frames of the Window.
        The frames are the header frame at the top of the window, the two sidebar frames and the main frame in the
        middle of the window. Classes that inherit from IWindow can access these frames only through the setup methods.
        The frames are created inside the constructor of IWindow.
    """

    @abstractmethod
    def setup_main_frame(self, frame:tkinter.Frame) -> None:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the main frame should be called in this method.
        """

    @abstractmethod
    def setup_header_bar(self, frame:tkinter.Frame) -> None:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the header frame should be called in this method.
        """

    @abstractmethod
    def setup_side_bar_left(self, frame:tkinter.Frame) -> bool:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the frame of the left sidebar should be called in this method.
            If the method returns True, the left sidebar will go from the bottom up to the top of the window, by
            narrowing the header frame.
            If the method returns False, the left sidebar will start from the bottom of the window and end at the bottom of the
            header frame. The header frame will extend to the left of the window.
        """

    @abstractmethod
    def setup_side_bar_right(self, frame:tkinter.Frame) -> bool:
        """
            All Subclasses o fIWindow must override this method.
            Code that adds content to the frame of the right sidebar should be called in this method.
            If the method returns True, the right sidebar will go from the bottom up to the top of the window, by
            narrowing the header frame.
            If the method returns False, the right sidebar will start from the bottom of the window and end at the bottom of the
            header frame. The header frame will extend to the right of the window.
        """

    @abstractmethod
    def on_load(self) -> None:
        """
            Subclasses must implement this method.
        """

    from main import DdInv
    def __init__(self, parent:tkinter.Widget, controller:DdInv, admin_mode:bool=False, ):
        """
            :param tkinter.Toplevel|tkinter.Frame parent:
            :param bool admin_mode:
            
        """
        super().__init__(parent, background='white')
        self.controller = controller
        self.parent = parent

        self.__header_frame:tkinter.Frame = tkinter.Frame(self, background=srh_orange if admin_mode else srh_blue)
        self.__header_buttons_frame_right:tkinter.Frame = tkinter.Frame(self.__header_frame, background=srh_orange if admin_mode else srh_blue)
        self.__header_buttons_frame_left:tkinter.Frame = tkinter.Frame(self.__header_frame, background=srh_orange if admin_mode else srh_blue)
        self.__center_frame:tkinter.Frame = tkinter.Frame(self, background='white')
        self.__left_bar_frame:tkinter.Frame = tkinter.Frame(self, background='white')
        self.__right_bar_frame:tkinter.Frame = tkinter.Frame(self, background='white')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)

        overlay_left:bool = self.setup_side_bar_left(self.__left_bar_frame)
        overlay_right:bool = self.setup_side_bar_right(self.__right_bar_frame)
        self.after(0, self.setup_header_bar, self.__header_frame)
        #self.setup_header_bar(self.__header_frame)

        self.__left_bar_frame.grid(row=0 if overlay_left else 1, column=0, rowspan=2 if overlay_left else 1, sticky='NSWE')
        self.__right_bar_frame.grid(row=0 if overlay_right else 1, column=2, rowspan=2 if overlay_right else 1, sticky='NSWE')
        self.__header_frame.grid(row=0, column=1 if overlay_left else 0, columnspan=3 - (1 if overlay_left else 0) - (1 if overlay_right else 0), sticky='NSWE')
        self.__center_frame.grid(row=1, column=1, sticky='NSWE')

        self.setup_main_frame(self.__center_frame)
