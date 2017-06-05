# coding: utf-8
from __future__ import absolute_import

from importlib import import_module
from collections import defaultdict
import hashlib

from ..exception.errors import ImportWorkerError
from ..templates.worker import Worker
from ..exception.errors import RunWorkerError


class SharedTables(object):

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        pass

    def get_id_tmo(self, key):
        return '$$$TMO'

    def get_id_tprm(self, key):
        return '$$$TPRM'

    def get_id_trlt(self, ):
        return '$$$TRLT'


class Parse(Worker):
    """
    Воркер для запуска интерфейса парсера
    """

    def __init__(self, msg):
        """

        :param msg: экземпляр класса Consumer.Msg
        """
        super().__init__(msg)
        try:
            self.parse_module = self.get_parse_module()
            self.parser_handler = self.get_parse_handler()
        except Exception as e:
            raise ImportWorkerError(e)

    def get_parse_module(self):
        """
        Метод возвращает модуль, где содержится Handler парсера.
        :return:
        """
        iface = self.msg.body['iface']
        path = f'parsers.{iface}.source'
        return import_module(path)

    def get_parse_handler(self):
        # Handler для универсальности должен иметь одинаковое имя во всех парсерах.
        return self.parse_module.HUAHRParserHandler

    def run(self):
        try:
            NewHandler = type('new_handler', (self.WrappHandler, self.parser_handler),
                              dict(__init__=self.WrappHandler.__init__)
                              )
            new_handler = NewHandler(**self.msg.body)
            res = new_handler.parse()
            print('Воркер завершил работу. Статус {}'.format(res))
        except Exception as e:
            raise RunWorkerError(e)

    class WrappHandler(object):
        """
        Обертка над нашими парсерами
        """

        def __init__(self, *args, **kwargs):
            """
            Этот конструктор заменяет текущий HUAHRParserHandler.__init__.

            :param args:
            :param kwargs:
            """
            self.msg_fields = []
            self.init()
            if kwargs:
                for attr in kwargs:
                    setattr(self, attr, kwargs[attr])
                    self.msg_fields.append(attr)

        @staticmethod
        def get_table_names():
            from core.db.model import MODELS

            table_names = []
            for m in MODELS:
                if m.db_table and m.is_dat:
                    table_names.append(m.db_table)
            return table_names

        @staticmethod
        def get_id(name):
            """
            Метод, возвращающий хэш, который используется как id.

            :param name:
            :return:
            """
            hash = hashlib.md5(name.encode('utf-8'))
            # int_hash = int(hash.hexdigest(), 16)
            int_hash = int(float.fromhex(hash.hexdigest()))
            return int(int_hash)

        def init(self):
            """
            В этом методе переопределяется часть логики из первоначального HUAHRParserHandler.__init__.

            :return:
            """
            self.shared_tables = SharedTables()
            self.id_generator = defaultdict(int)  # выдавать хэш
            self.id_trlt = 'TRLT_ID'
            table_names = self.get_table_names()
            self.tables = {}
            self.tables.update(self.create_tables(table_names))

        def init_db(self, vendor, technology):
            """
            Метод для получения параметров из базы.

            :param VND_VENDOR:
            :param VND_TECHNOLOGY:
            :return:
            """
            import core.settings
            from core.db.layer import DbLayer
            from core.credentials import VndCredentials, OracleCredentials
            from core.logger.server import start_logging_server_db, stop_logging_server
            #

            db_credentials = OracleCredentials(core.settings.DB_USER,
                                               core.settings.DB_PASSWORD,
                                               core.settings.DB_TNSNAME)

            logger_server = start_logging_server_db(db_credentials)
            db_layer = DbLayer(logger_server.port, db_credentials)

            self.vnd_credentials = VndCredentials(vendor, technology)
            self.id_vendtech = db_layer.get_vendtech_id(
                self.vnd_credentials.vendor, self.vnd_credentials.technology
            )
