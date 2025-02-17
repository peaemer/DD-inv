import os, sys
import pathlib
from shutil import copyfile

real_path_string:str = ''
root_path_string:str = ''
bundled_app_files_path_string:str = ''
app_files_path_string:str = ''
assets_path_string:str = ''

def gen_paths():
    """
        .
    """
    global app_files_path_string, bundled_app_files_path_string, real_path_string, root_path_string, assets_path_string
    real_path_string = os.path.dirname(os.path.realpath(__file__))
    root_path_string = str(pathlib.Path.cwd()) + '\\'
    bundled_app_files_path_string = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))[:-4])
    if not bundled_app_files_path_string.endswith('\\includes\\'):
        bundled_app_files_path_string += '\\includes\\'
    app_files_path_string = root_path_string + 'DD-Inv-Files\\'
    assets_path_string = bundled_app_files_path_string + 'assets\\'
    if not pathlib.Path(app_files_path_string).exists():
        os.mkdir(app_files_path_string)
    print('root path:' + root_path_string)
    print('bundled app files path:' + bundled_app_files_path_string)
    print('app files path:' + app_files_path_string)
    print('assets path:' + assets_path_string)

def gen_app_files():
    """
        creates a directory for the app files and initializes a fallback database as well as the local config file
    """
    global root_path_string, bundled_app_files_path_string, app_files_path_string
    if not pathlib.Path(app_files_path_string + r'DD-invBeispielDatenbank.sqlite3').is_file():
        copyfile(
            bundled_app_files_path_string + r'sec_data_info\DD-invBeispielDatenbank.sqlite3',
            app_files_path_string + r'DD-invBeispielDatenbank.sqlite3'
        )

def assets_path(relative_asset_path:str) -> str:
    """
        generates a string with the path of the assets folder together with the relative path

        :param str relative_asset_path: the path relative to the assets folder

        :return: a string representing the path
    """
    global assets_path_string
    return os.path.join(assets_path_string, relative_asset_path)

gen_paths()
gen_app_files()