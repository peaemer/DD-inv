from io import FileIO
from os.path import isfile
from typing import List, TypeVar, Generic

T = TypeVar("T")

class Configuration(Generic[T]):
    """
        a helper class to read and write configuration data from a text file easier.

        :var str file_path: the path to the configuration file.
    """

    def open(self) -> FileIO:
        return open(self.file_path)

    def read_configuration(self) -> T:
        """
            :return:
        """
        print(self.file_path)
        return T(None)


    def write_configuration(self, value: T) -> None:
        pass


    def __init__(self, file_path_: str):
        if not isfile(file_path_):
            raise Exception('asdfasd')
        self.file_path: str = file_path_


class ConfigurationManager:
    def __init__(self, file_path_: str):
        self.file_name = file_path_

    def get_file_name(self) -> str:
        return self.file_name

    def generate_configuration(self) -> Configuration:
        return Configuration(self.file_name)

    def open(self) -> FileIO:
        return open(self.file_path)



ConfigurationManager('').generate_configuration()
