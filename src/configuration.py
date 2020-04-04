import fileinput
import os
import sys
from abc import abstractmethod, ABC
from enum import Enum


class File:
    def __init__(self, name=None):
        """
        Initializes all parent class variables that are going to be used
        later on.

        :param name: Name for the file.
        """
        if name is None:
            name = "bot_config"
        self.name = name if not name.endswith(".txt") else name.replace(".txt", "")
        self.path = os.path.join(os.getcwd(), "{0}.txt".format(self.name))
        self.prepare_file()

    def prepare_file(self):
        """
        Prepares the files.

        This depends on the :func:`~configuration.File.file_exists_method` and
        :func:`~configuration.File.file_not_exists_method` that are going to be
        implemented on extending classes.
        """
        if os.path.exists(self.path):
            self.file_exists_method()
        else:
            self.file_not_exists_method()

    @abstractmethod
    def file_exists_method(self):
        """
        This function should be implemented in the extending class since
        :func:`~configuration.File.prepare_files` will call this function
        when the file exists.
        """
        pass

    @abstractmethod
    def file_not_exists_method(self):
        """
        This function should be implemented in the extending class since
        :func:`~configuration.File.prepare_files` will call this function
        when the file does exists.
        """
        pass


class ConfigNode(Enum):
    TOKEN = ("bot_token", "replace this with your bot's token")
    PREFIX = ("command_prefix", "$")


class ConfigFile(File, ABC):
    def __init__(self, name=None):
        super().__init__(name)
        self.nodes = {}
        self.init_nodes()

    def init_nodes(self):
        f = open(self.path, 'r')
        for line in f:
            key = self.__get_key_from_line(line)
            if self.__key_in_nodes(key):
                self.nodes[key] = self.__get_val_from_line(line)
        f.close()

    def get_node(self, node):
        return self.nodes[node.value[0]]

    def set(self, node, value):
        for line in fileinput.input(self.path, inplace=True):
            key = self.__get_key_from_line(line)
            if key == node.value[0]:
                line = "{} = {}\n".format(key, value)
                self.nodes[key] = value
            sys.stdout.write(line)

    def file_exists_method(self):
        f = open(self.path, 'r+')
        for node in ConfigNode:
            if not self.__node_in_file(f, node):
                f.write("{} = {}\n".format(node.value[0], node.value[1]))
        f.close()

    def file_not_exists_method(self):
        f = open(self.path, 'w+')
        for node in ConfigNode:
            f.write("{} = {}\n".format(node.value[0], node.value[1]))
        f.close()

    @staticmethod
    def __get_key_from_line(line):
        return line.replace(" ", "")[0:line.index("=") - 1]

    @staticmethod
    def __get_val_from_line(line):
        return line[line.index("=") + 1:len(line) - 1].lstrip()

    @staticmethod
    def __node_in_file(f, node):
        for line in f:
            if line.startswith(node.value[0]):
                return True
        return False

    @staticmethod
    def __key_in_nodes(key):
        for node in ConfigNode:
            if key == node.value[0]:
                return True
        return False

