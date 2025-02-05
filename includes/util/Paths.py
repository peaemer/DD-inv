import os, sys
import pathlib
from shutil import copyfile

real_path:str = ''
root_path:str = ''
bundled_app_files_path = ''
app_files_path:str = ''
assets_path:str = ''

def gen_paths():
    """

    """
    global app_files_path, bundled_app_files_path, real_path, root_path, assets_path
    real_path = os.path.dirname(os.path.realpath(__file__))
    root_path = str(pathlib.Path.cwd())+'\\'
    bundled_app_files_path = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))[:-4])
    if not bundled_app_files_path.endswith('\\includes\\'):
        bundled_app_files_path += '\\includes\\'
    app_files_path = root_path + 'DD-Inv-Files\\'
    assets_path = bundled_app_files_path + 'assets\\'
    if not pathlib.Path(app_files_path).exists():
        os.mkdir(app_files_path)
    print('root path:'+root_path)
    print('bundled app files path:' + bundled_app_files_path)
    print('app files path:' + app_files_path)
    print('assets path:' + assets_path)

def gen_app_files():
    """
        creates a directory and initializes a fallback database as well as the local config file
    """
    global root_path, bundled_app_files_path, app_files_path
    if not pathlib.Path(app_files_path + r'DD-invBeispielDatenbank.sqlite3').is_file():
        copyfile(
            bundled_app_files_path + r'sec_data_info\DD-invBeispielDatenbank.sqlite3',
            app_files_path + r'DD-invBeispielDatenbank.sqlite3')

def asset_path(relative_asset_path:str) -> str:
    global assets_path
    return os.path.join(assets_path, relative_asset_path)