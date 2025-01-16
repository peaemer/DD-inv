from copy import copy
from typing import Final

message_type_style:Final[str] = '\033[1;32m'
class_style:Final[str] = '\033[1;34m'
error_style:Final[str] = '\033[1;31m'
reset_style:Final[str] = '\033[0;0m'

DEBUG_MODE_NORMAL:Final[bool] = True
DEBUG_MODE_ALL:Final[bool] = True
color_mode:bool = True


class Logger:

    levels:list[str]

    def __init__(self, level:str, levels:list[str]=None):
        self.levels:list[str] = []
        if levels:
            self.levels = copy(levels)
        self.levels.append(level)

    def __debug(self, message:str):
        levels: str = ''
        for level in self.levels:
            levels = levels + f'[{level}]'
        print(f'{message_type_style if color_mode == True else ''}[Debug]{class_style if color_mode == True else ''}{levels}:{reset_style if color_mode == True else ''}' + message)

    def debug(self, message:str):
        if DEBUG_MODE_NORMAL|DEBUG_MODE_ALL:
            self.__debug(message)

    def debug_e(self, message:str):
        if DEBUG_MODE_ALL:
            self.__debug(message)

    def error(self, message:str):
        levels: str = ''
        for level in self.levels:
            levels = levels + f'[{level}]'
        print(f'{error_style if color_mode == True else ''}[Error]{class_style if color_mode == True else ''}{levels}:{error_style if color_mode == True else ''}' + message)
