import os
from abc import abstractmethod, ABC
from enum import Enum


class File:
    def __init__(self, name):
        """
        Initializes all parent class variables that are going to be used
        later on.

        :param name: Name for the file.
        """
        self.name = name
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
            print("file exists")
            self.file_exists_method()
        else:
            print("file does not exists")
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
    TOKEN = "bot_token"


class ConfigFile(File, ABC):
    def __init__(self, name):
        super().__init__(name)
        self.nodes = {}
        self.init_nodes()

    def init_nodes(self):
        f = open(self.path, 'r')
        for element in ConfigNode:
            for line in f:
                if line.startswith(element.value):
                    prefix = "{0}=".format(element.value)
                    value = line.replace(" ", "").replace(prefix, "")
                    self.nodes[element.value] = value
        f.close()

    def get_node(self, node):
        return self.nodes[node.value]

    def file_exists_method(self):
        f = open(self.path, 'r+')
        for node in ConfigNode:
            if not self.__node_in_file(f, node):
                f.write("{0} = \n".format(node.value))
        f.close()

    @staticmethod
    def __node_in_file(f, node):
        for line in f:
            if line.startswith(node.value):
                return True
        return False

    def file_not_exists_method(self):
        f = open(self.path, 'w+')
        for node in ConfigNode:
            f.write("{0} = \n".format(node.value))
        f.close()
