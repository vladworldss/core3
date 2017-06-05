# coding: utf-8
# flake8: noqa
"""
Interface for API Database.
"""

import abc

from .executor import _DbExecutor

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Gerasimenko V.A."
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class DbLayer(metaclass=abc.ABCMeta):
    """
    API для работы с БД.
    """

    def __init__(self, executor):
        self.__db_executor = None
        self.db_executor = executor

    @property
    def db_executor(self):
        return self.__db_executor

    @db_executor.setter
    def db_executor(self, ex):
        if not isinstance(ex, _DbExecutor):
            raise TypeError("")
        elif self.__db_executor:
            self.__db_executor.close()
        self.__db_executor = ex

    @abc.abstractmethod
    def get_data(self, *args, **kw):
        """Получение данных из БД для сервиса"""
        pass
