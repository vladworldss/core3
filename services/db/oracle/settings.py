# coding: utf-8
# flake8: noqa
"""
Модуль настроек для инициации сессий с БД Oracle.
"""
import os

from core3.settings import BASE_PARSER_DIR
from core3.services.templates.config import create_conf

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Gerasimenko V.A."
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class OracleDbConf:
    """
    Класс настроек для подключения, прогрузки данных в OracleDB.
    """
    __slots__ = ()

    __DB_TYPE = 'oracle'
    __BASE_PARSER_DIR = BASE_PARSER_DIR
    __REQUIRED_CRED = ('user', 'password', 'tnsname')

    @classmethod
    def credentials(cls, db_name='datasafe'):
        """ Метод класса, возвращающий credentials подключения к БД."""
        cred = {
            'local': create_conf(
                'credentials', **cls.create_cred('user', 'pwd', 'localhost:1521/xe')
            )
        }
        return cred[db_name]

    @classmethod
    def create_cred(cls, user, pwd, tnsname):
        if not all(isinstance(cred, str) for cred in (user, pwd, tnsname)):
            raise TypeError('Credentials must be a string!')
        return dict(zip(cls.__REQUIRED_CRED, (user, pwd, tnsname)))

    @classmethod
    def session_pool_size(cls):
        conf = {"min": 1, "max": 20, "increment": 1}
        return create_conf('session_pool_size', **conf)

    @classmethod
    def load_conf(cls):
        # Полный путь к директории, куда буду выгружены DAT файлы после работы парсера
        dat_file_basedir = os.path.join(BASE_PARSER_DIR, 'dat')

        # Формат временных DAT папок
        dat_date_format = '%d-%m-%y'

        # Количество DAT папок для хранения
        dat_live_dates_count = 2

        conf = dict(
            zip(
                ('dat_file_basedir', 'dat_date_format', 'dat_live_dates_count'),
                (dat_file_basedir, dat_date_format, dat_live_dates_count)
            )
        )
        return create_conf('load_conf', **conf)

    @classmethod
    def ctl_conf(cls):
        ctl_file_content = """OPTIONS (DIRECT=TRUE, MULTITHREADING=TRUE, READSIZE=400000, ERRORS=50000000) 
        LOAD DATA INFILE "{}" TRUNCATE INTO TABLE {} PARTITION ({}) FIELDS TERMINATED BY '|' 
        TRAILING NULLCOLS ({})
        """
        ctl_dir = os.path.join(cls.__BASE_PARSER_DIR, 'ctl')

        conf = dict(
            zip(
                ('ctl_file_content', 'ctl_dir'),
                (ctl_file_content, ctl_dir)
            )
        )
        return create_conf('ctl_conf', **conf)
