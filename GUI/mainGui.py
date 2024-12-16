import tkinter as tk
import threading
from pages import logInWindow, mainPage, userDetailsWindow, detailsWindow, roomDetailsWindow, adminRoomWindow, \
    adminUserWindow, adminRoleWindow


class ddINV(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Inventartool")
        self.configure(background="white")
        self.state("zoomed")

        # Set window dimensions and icon
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0')
        self.minsize(1280, 720)
        self.maxsize(1920, 1080)
        self.iconbitmap("assets/srhIcon.ico")

        # Create a container for frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Load the login window first
        self.show_frame(logInWindow)


    def show_frame(self, cont):
        if cont not in self.frames:
            frame = cont(self.container, self)
            self.frames[cont] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        else:
            frame = self.frames[cont]

        if isinstance(frame, tk.Frame):
            frame.tkraise()

            if hasattr(frame, 'on_load') and callable(frame.on_load):
                print(f"on_load wird für {cont.__name__} aufgerufen")  # Debug
                frame.on_load()


if __name__ == "__main__":
    app = ddINV()
    app.mainloop()
