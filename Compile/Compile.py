import PyInstaller.__main__

PyInstaller.__main__.run([
    "--noconfirm",
    "--onefile",
    "--console",
    "--icon", r"C:\Users\alex\PycharmProjects\DD-inv\includes\assets\srhIcon.ico",
    "--add-data", r"C:\Users\alex\PycharmProjects\DD-inv\includes;includes/",
    "--add-data", r"C:\Users\alex\PycharmProjects\DD-inv\cache.py;.",
    "--hidden-import", "sqlite3",
    "--hidden-import", "tkinter",
    "--hidden-import", "customtkinter",
    "--hidden-import", "pillow",
    "--hidden-import", "CTkListbox",
    r"C:\Users\alex\PycharmProjects\DD-inv\main.py"
])
