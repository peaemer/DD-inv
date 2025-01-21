from typing import TextIO
from os import path

""""
class Parameter(Generic[T]):
        :var int offset: the offset of the start of the parameter expression releative to the start of the file.


    def read(self) -> T:
        pass

    def write(self, value:T) -> None:
        pass

    def __init__(self):
        pass
"""

class Configuration:
    """
        :var ConfigManager manager:
    """

    def __load_configuration(self) -> None:
        pass

    def read_parameter(self, parameter_name:str)->str:
        pass

    def write_parameter(self, parameter_name:str, value:object) -> None:
        pass

    def __init__(self, manager_:'ConfigManager', name_:str, offset_:int):
        self.manager = manager_
        self.name:str = name_
        self.offset:int = offset_


class ConfigManager:

    def __open(self) -> TextIO:
        return open(self.file_path,'r')

    def __resize_Configurations(self):
        pass

    def __init__(self, file_path_:str):
        self.file_path:str = file_path_

    def generate_configuration(self):
        buffer:str = ''
        with self.__open() as file:
            lines:list[str] = file.readlines()
            length:int = len(lines)
            for i in range(length):
                buffer+=lines[i]
            buffer += '\n'


    def read_configuration(self, configuration_name:str)->Configuration:
        cfg:Configuration

        return cfg