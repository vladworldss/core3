# coding: utf-8
# flake8: noqa
"""
Модуль определяющий логику выполнения SQL-скриптов и получения результатов. 
"""
from collections import OrderedDict
from decimal import Decimal
import cx_Oracle

from core3.services.templates.executor import _DbExecutor

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Gerasimenko V.A."
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class DbExecutor(_DbExecutor):
    """
    Класс транзакций с OracleDB.
    """

    __db_types = ('CURSOR', 'NUMBER', 'STRING')

    @classmethod
    def db_type(cls, _type):
        _type = _type.upper()
        if _type not in cls.__db_types:
            raise AttributeError(f'cx_Oracle does not support this type {_type}')
        return getattr(cx_Oracle, _type)

    def __init__(self, conf):
        super().__init__(conf)

        cred = self.db_conf.credentials()  # при дебаге - передавать tns сюда
        pool_size = self.db_conf.session_pool_size()

        self.__pool = cx_Oracle.SessionPool(
            user=cred.user, password=cred.password, dsn=cred.tnsname,
            min=pool_size.min, max=pool_size.max, increment=pool_size.increment
        )
        self.connection = self.__pool.acquire()
        self.cursor = self.connection.cursor()

    @property
    def pool(self):
        return self.__pool

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.pool.release(self.connection)

    @staticmethod
    def _fetch(cursor):
        """
        Преобразование результата выполнения запроса в словарь
        """
        def none_extraction(x):
            if x is None:
                x = ''
            elif isinstance(x, Decimal):
                x = float(x)
            return x

        desc = cursor.description

        res = []
        for row in cursor.fetchall():
            item = OrderedDict(
                zip([col[0].lower() for col in desc], map(none_extraction, row))
            )
            res.append(item)

        return res

    @staticmethod
    def get_sql_from_file(filepath):
        """
        acquire sql script from file
        """
        with open(filepath, 'r') as sql_file:
            return ''.join(sql_file)

    def run_query(self, sql):
        self.cursor.execute(sql)
        return self._fetch(self.cursor)

    def call_func(self, function_name, parameters, out_type='CURSOR'):
        """
        Вызов ORACLE функции

        :param function_name: имя функции
        :type function_name: string
        :param parameters: список параметров
        :type parameters: tuple
        :param out_type: тип возвращаемого значения
        :type out_type: _BASEVARTYPE
        :return: результат выполнения функции
        """
        out_type = self.db_type(out_type)
        res = self.cursor.callfunc(function_name, out_type, parameters)
        if out_type is cx_Oracle.CURSOR:
            res = self._fetch(res)
        return res

    def call_proc(self, procedure_name, parameters, out_type='CURSOR'):
        """
        Вызов ORACLE процедуры

        :param procedure_name: имя процедуры
        :type procedure_name: string
        :param parameters: список параметров
        :type parameters: tuple
        :param out_type: тип возвращаемого значения
        :type out_type: _BASEVARTYPE
        :return: результат выполнения процедуры
        """
        out_type = self.db_type(out_type)
        res = self.cursor.callproc(procedure_name, parameters)
        if out_type is cx_Oracle.CURSOR:
            res = self._fetch(res)
        return res
