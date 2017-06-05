from __future__ import absolute_import
import abc

from core3.services.templates.decorators import has_methods


@has_methods('credentials')
class DbConf(metaclass=abc.ABCMeta): pass


@has_methods('close', 'cursor')
class DbConnection(metaclass=abc.ABCMeta): pass


@has_methods('close')
class DbCursor(metaclass=abc.ABCMeta): pass


class _DbExecutor(metaclass=abc.ABCMeta):
    """
    Абстрактный класс, определяющий логику выполнения SQL-скриптов и получения результатов.
    Реализован в качестве контекстного менеджера (with...)
    """

    def __init__(self, conf):
        self.__db_conf = None
        self.__connection = None
        self.__cursor = None

        self.db_conf = conf

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.__connection = self.__cursor = None

    @property
    def db_conf(self):
        return self.__db_conf

    @db_conf.setter
    def db_conf(self, conf):
        if not issubclass(conf, DbConf):
            raise TypeError('Settings does not have required attrs')
        self.__db_conf = conf

    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, conn):
        if self.__connection:
            raise AttributeError('Connection is already created!')
        elif not isinstance(conn, DbConnection):
            raise AttributeError('Connection does not have required attrs!')
        self.__connection = conn

    @property
    def cursor(self):
        return self.__cursor

    @cursor.setter
    def cursor(self, curs):
        if not isinstance(curs, DbCursor):
            raise AttributeError('Cursor does not have required attrs!')
        self.__cursor = curs

    @abc.abstractmethod
    def close(self):
        pass
