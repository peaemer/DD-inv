import math
import os.path
from math import trunc
from typing import TextIO, Tuple, Final

from includes.util.Logging import Logger

logger: Logger = Logger('ConfigManager')
CONFIGURATION_HEADER_LENGTH: Final[int] = 60


class Configuration:
    """
        :var ConfigManager manager:
    """

    def read_parameter(self, parameter_name: str, generate_if_missing:bool = False, gen_initial_value:str = 'null') -> str:
        """
            :param str parameter_name: the name of the property
            :param bool generate_if_missing: whether to generate the new parameter inside
                the configuration file, if it is not present
        """
        lines: list[str] = self.manager.get_lines()
        i: int = self.offset + 2
        while i < len(lines):
            if lines[i].startswith('##'):
                break
            if lines[i].startswith(parameter_name):
                return lines[i].split(':')[1].strip().strip('\n')
            i += 1
        if generate_if_missing:

            self.write_parameter(parameter_name, gen_initial_value)
        return gen_initial_value

    def write_parameter(self, parameter_name: str, value: object, append_if_missing: bool = True) -> None:
        """
            converts an object to a string and replaces the former value of the property inside the config
            file with the new value.

            :param str parameter_name:the name of the property.
            :param object value:the value of the property.
            :param bool append_if_missing:whether to create a new property for the configuration in case the property doesn't exist already.
        """
        lines: list[str] = self.manager.get_lines()
        i: int = self.offset + 1
        if i == len(lines):
            lines.append(f'\n#description\n{parameter_name}:{str(value)}\n')
        else:
            i += 1
            while i <= len(lines):
                if parameter_name in lines[i]:
                    lines[i] = f'{parameter_name}:{str(value)}\n'
                    break
                if lines[i].startswith('##') or i == len(lines) - 1:
                    if append_if_missing:
                        lines.insert(i - 1, f'#description\n{parameter_name}:{str(value)}\n\n')
                        break
                    else:
                        return
                i += 1
        text: str = ''
        for line in lines:
            text += line
        self.manager.overwrite_config_file(text)

    def __init__(self, manager_: 'ConfigManager', name_: str, offset_: int):
        """
            :param ConfigManager manager_: the manager for the file where the configuration is stored
            :param str name_: the name of the configuration file
            :param str offset_: the line count of the line with this configuration's name inside th config file
        """
        self.manager = manager_
        self.name: str = name_
        self.offset: int = offset_


class ConfigManager:
    """
        :var str file_path:
    """

    def __open(self, readonly: bool = True) -> TextIO:
        """
            opens a TextIO stream to the config file at the file path of this ConfigManager

            :param bool readonly: if true, create a new empty config file, in case there is none.
        """
        if not os.path.isfile(self.file_path):
            open(self.file_path, 'w').close()
        return open(self.file_path, 'r') if readonly else open(self.file_path, 'w')

    @staticmethod
    def __is_decorator_line(line: str) -> bool:
        """
            checks that every character in the string is '#' or newline

            :param str line: the string to check
        """
        return all(char == '#' or char == '\n' for char in line)

    def get_lines(self) -> list[str]:
        """
            reads the contents of the file at the file path of this ConfigManager
            returns the data as a list of strings, where each string is a line of the file.

            :return: a list of strings, containing the config file's text
        """
        lines: list[str]
        with self.__open() as file_handle:
            lines = file_handle.readlines()
        return lines

    def __resize_Configurations(self):
        """

        """
        lines: list[str] = self.get_lines()
        for line in lines:
            if line.startswith('##') and not False:
                pass

    def overwrite_config_file(self, text: str) -> None:
        """
            writes the text to the file at the file path of this ConfigManager
        """
        with self.__open(readonly=False) as file_handle:
            file_handle.write(text)

    def get_configuration_by_name(self, configuration_name: str) -> Configuration | None:
        """
            searches the configuration file after a line where the configuration name is surrounded by '#'.

            :param str configuration_name: the title of the configuration

            :return: a configuration if a Configuration with that name exists, None otherwise
        """
        for line in self.get_lines():
            i: int = 0
            if f'# {configuration_name} #' in line:
                return Configuration(self, configuration_name, self.get_lines().index(line) + 1)
        return None

    def generate_configuration(self, configuration_name: str, always_append: bool = False) -> Configuration:
        """
            Creates a configuration header which is made of the given name and enough '#' at both sides,
            so that the lines is 60 chars long all together.
            Additionally, the line above and beneath are filled 60 '#' each.
            The properties of the new configuration are listed under the header.
            If overwrite is enabled, the config file is first searched for an already existing configuration by that name.
            In that case the already existing configuration's properties may be overwritten with the given data.

            :param str configuration_name:
            :param bool always_append:

            :return: a configuration with the given name
        """
        #serach for the configuration as it may exist already
        if not always_append and self.get_configuration_by_name(configuration_name):
            return self.get_configuration_by_name(configuration_name)
        #buffer the whole text of the config into a string
        buffer: str = ''
        for line in self.get_lines():
            buffer += line
        #if the buffer isn't empty and doesn't have a newline at its end, add a newline
        if not buffer.endswith('\n') and not buffer == '':
            buffer += '\n'
        #if the buffer isn't still empty, add two additional newlines
        if not buffer == '':
            buffer += '\n\n'
        #add a row of '#'
        for i in range(CONFIGURATION_HEADER_LENGTH):
            buffer += '#'
        buffer += '\n'
        # calculate the amount of '#' that must be added to the configuration's name to make it 60 characters long
        # add half the '#' and a space to the left of the configuration's name
        for i in range(math.floor((CONFIGURATION_HEADER_LENGTH - 2 - len(configuration_name)) / 2)):
            buffer += '#'
        buffer += ' '
        buffer += configuration_name
        buffer += ' '
        #add a space and the rest of the '#' to the right of the configuration's name
        for i in range(math.ceil((CONFIGURATION_HEADER_LENGTH - 2  - len(configuration_name)) / 2)):
            buffer += '#'
        buffer += '\n'
        #add a row of '#'
        for i in range(CONFIGURATION_HEADER_LENGTH):
            buffer += '#'
        buffer += '\n'
        #write the buffer to the config file
        self.overwrite_config_file(buffer)
        return self.get_configuration_by_name(configuration_name)

    def __init__(self, file_path_: str = os.path.dirname(__file__) + '/main.config', initial_fields:list[str] = None):

        """

            :param list[str] initial_fields:
        """
        self.file_path: str = file_path_
        if initial_fields and len(initial_fields) > 0:
            for field in initial_fields:
                self.generate_configuration(field)
