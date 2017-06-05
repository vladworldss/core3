# coding: utf-8
# flake8: noqa
"""
Модуль API взаимодействия с БД Oracle.
"""

import os
from collections import OrderedDict, ChainMap, defaultdict

from core3.services.templates.layer import DbLayer
from .model import *

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright 2017, Gerasimenko V.A."
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class _DbLayer(DbLayer):
    """
    Базовый класс 
    """

    @property
    def func_store(self):
        store = {
            'id_vendtech': 'DS8_API.GET_VENDTECH_ID',
            'id_parser': 'DS8_API.GET_PARSER_ID',
            'id_session': 'DS8_API.GET_SESSION_ID',
            'tmo_data': 'DS8_API.GET_MO_TYPE_DATA',
            'tprm_data': 'DS8_API.GET_PARAMETER_TYPE_DATA',
            'update_bad_omc': 'DS8_API.UPDATE_BAD_OMC_SET_1',
            'loaded_data': 'DS8_PROCESS_LOADED_DATA',
            'table_columns': 'DS8_API.GET_TABLE_COLUMNS',
            'pckg_errors': 'DS8_API.GET_INTERFACE_PACKAGE_ERRORS',
            'config': 'DS8_API.GET_CONFIG',
            'server_data': 'DS8_API.GET_SERVER_DATA',
            'parsing_files': 'DS8_API.GET_PARSING_FILES',
            'bit_prm_data': 'DS8_API.GET_BIT_PARAMETERS_DATA'

        }
        return store

    def call_func(self, func_name, params, *args, **kw):
        try:
            func = self.func_store[func_name]
        except KeyError:
            raise NameError('Bad name of db_function!')

        return self.db_executor.call_func(func, params, *args, **kw)

    def get_id(self, id_type, vendtech):
        """
        Получить идентификатор с БД.

        :param id_type: имя функции в БД. 
        :return: dict
        """

        params = (vendtech,)
        id = ''
        try:
            id = int(self.call_func(id_type, params, 'NUMBER'))
        except Exception:
            pass
        return id


class Session(_DbLayer):

    def get_data(self, vendtech, **kw):
        """
        Получение технической информации для инициализации сессии парсера.
        
        :param vendtech: 
        :return: 
        """
        func_names = ('id_vendtech', 'id_parser', 'id_session')
        ids = map(lambda func_name: self.get_id(func_name, vendtech), func_names)
        return dict(zip(func_names, ids))


class DlRaw(_DbLayer):

    def get_data(self, **kw):
        """
        Получение информации, необходимой для сервиса DlRaw.
        
        :param vendtech: 
        :return: 
        """

        conf = self.get_confs(**kw)
        return conf

    def get_confs(self, id_vendtech, **kw):
        """
        Получение конфигураций для выгрузки RAW файлов.

        :param id_vendtech: идентификатор вендор/технология
        :type id_vendtech: int
        :return: список кортежей (конфигурация, сервер)
        :rtype: list
        """
        parameters = (id_vendtech,)

        dlraw_confs = self.call_func('config', parameters)

        server_confs = self.get_server_confs()
        server_hash_confs = dict(map(lambda x: (x['id_server'], x), server_confs))

        chain = map(
            lambda conf: dict(ChainMap(conf, server_hash_confs[conf['id_server']])),
            dlraw_confs
        )

        confs = defaultdict(list)
        list(map(lambda x: confs[x['id_server']].append(x), chain))
        return confs

    def get_server_confs(self):
        """
        Получение всей таблицы серверов.

        :return: список объектов DlrawServer
        :rtype: list
        """
        parameters = ()
        data = self.call_func('server_data', parameters)
        return data

    def get_parsing_files_from_rawdir(self, vendor, technology, raw_dirpath):
        """
        Получение списка RAW файлов для парсинга

        :param vendor: название вендора
        :type vendor: str
        :param technology: название технологии
        :type technology: str
        :param raw_dirpath: полный путь к директории с RAW файлами
        :type raw_dirpath: str

        :return: список файлов
        :rtype: list
        """
        db_raw_files = self.get_parsing_files_from_db(vendor, technology)
        result = []

        # TODO: переписать рекурсивно
        dir_name_list = os.listdir(raw_dirpath)
        raw_file_records = []
        for dir_name in dir_name_list:
            if not os.path.isdir(os.path.join(raw_dirpath, dir_name)):
                continue
            raw_file_names = os.listdir(os.path.join(raw_dirpath, dir_name))
            for raw_filename in raw_file_names:
                if os.path.isdir(os.path.join(
                        raw_dirpath, dir_name, raw_filename)):
                    continue
                raw_file_records.append((dir_name, raw_filename))

        for raw_file_record in raw_file_records:
            for db_raw_file in db_raw_files:
                if (os.path.basename(db_raw_file.dirname) ==
                        raw_file_record[0] and
                        db_raw_file.filename == raw_file_record[1]):
                    result.append(db_raw_file)
                    break
        return result

    def get_parsing_files_from_db(self, vendor, technology, **kw):
        """
        Получение списка RAW файлов для парсинга

        :param vendor: название вендора
        :type vendor: str
        :param technology: название технологии
        :type technology: str

        :return: список файлов
        :rtype: list
        """
        parameters = (vendor, technology)
        raw_files = self.call_func('parsing_files', parameters)
        if not raw_files:
            raise Exception(f'RAW files for {vendor}{technology} are not found. '
                            f'Check OMC/DLRAW table.'
                            )

        result = [RawFile(**raw_file) for raw_file in raw_files]
        return result

    def dlraw_add_file(self, id_conf, name, path, dlraw_date,
                       modification_date, id_vendtech, id_omc, id_mr, size,
                       comment, backup_path, bad=0):
        """
        Добавление информации о RAW файле в базу.

        :param id_conf: идентификатор конфигурации
        :type id_conf: int
        :param name: имя
        :type name: str
        :param path: путь
        :type path: str
        :param dlraw_date: дата загрузки
        :type dlraw_date: datetime.datetime
        :param modification_date: дата модификации файла на сервере
        :type modification_date: datetime.datetime
        :param id_vendtech: идентификатор вендра/технологии
        :type id_vendtech: int
        :param id_omc: идентификатор OMC
        :type id_omc: int
        :param mr: макрорегион
        :type mr: str
        :param size: размер файла
        :type size: int
        :param comment: комментарий
        :type comment: str
        :param backup_path: полный путь к бэкап-директории
        :type backup_path: str
        :param bad: признак успешного парсинга файла
        :type bad: int
        """
        # id_mr = self.update_mr(mr) - ЭТОГО УЖЕ НЕТ
        try:
            modification_date_str = modification_date.strftime(
                '%d-%m-%Y %H:%M:%S')

        except BaseException:
            modification_date_str = '01-01-2013 00:00:00'

        parameters = (id_conf, name, path,
                      dlraw_date.strftime('%d-%m-%Y %H:%M:%S'),
                      modification_date_str, id_vendtech, id_omc, id_mr,
                      size, comment, backup_path, bad)

        result = self.call_func(
            'DS8_API.DLRAW_ADD_FILE', parameters, 'STRING')

        if str(result) != '0':
            self.logger.info(
                'File {}\{} added into DB with result: {}'.format(
                    path, name, result))
        return result


class Parse(_DbLayer):

    def get_data(self, **kw):
        """
        Получение информации, необходимой для сервиса Parse.
        
        :param vendtech: 
        :return: 
        """

    # TODO: Рудимент - в нескольких парсерах test OK
    def get_bit_parameter_data(self, vendor, technology, **kw):
        """
        Получение записей таблицы типов MO

        :param vendor: название вендора
        :type vendor: str
        :param technology: название технологии
        :type technology: str

        :return: список записей таблицы типов MO в виде объектов MOType
        :rtype: list
        """
        parameters = ('{}{}'.format(vendor, technology), )
        bit_parameter_data = self.call_func('bit_prm_data', parameters)
        result = [BitParameter(**bit_param) for bit_param in bit_parameter_data]
        return result

    def get_mo_type_data(self, vendtech, id_vendtech=None, **kw):
        """
        Получение записей таблицы типов MO

        :param vendor: название вендора
        :type vendor: str
        :param technology: название технологии
        :type technology: str

        :return: список записей таблицы типов MO в виде объектов MOType
        :rtype: list
        """
        if not id_vendtech:
            id_vendtech = self.get_id('id_vendtech', vendtech)
        parameters = (vendtech, )

        mo_type_data = self.call_func('tmo_data', parameters)
        result = [MOType(id_vendtech=id_vendtech, **mo_type) for mo_type in mo_type_data]
        return result

    def get_parameter_type_data(self, vendtech, id_vendtech, **kw):
        """
        Получение записей таблицы типов параметров

        :param vendor: название вендора
        :type vendor: str
        :param technology: название технологии
        :type technology: str

        :return: список записей таблицы типов параметров
        в виде объектов ParameterType
        :rtype: list
        """
        parameters = (vendtech,)
        prm_type_data = self.call_func('tprm_data', parameters)
        result = [ParameterType(id_vendtech=id_vendtech, **prm_type) for prm_type in prm_type_data]
        return result

    def mark_unparsed_omcs_by_vendtech(self, id_vendtech, omc_list, **kw):
        """
        Пометить omc в таблице rfile bad=1, которые распарсилились с ошибками

        :param id_vendtech: идентификатор вендора
        :type id_vendtech: int
        :param omc_list: множество omc
        :type omc_list: set of omc
        """
        parameters = (id_vendtech, ','.join(omc_list))
        try:
            result = self.call_proc('update_bad_omc', parameters, 'NUMBER')
        except Exception as e:
            print(e)
            result = -1
        return result


class Load(_DbLayer):

    def get_load_data(self, **kw):
        """
        Получение информации, необходимой для сервиса Load.
        
        :param vendtech: 
        :return: 
        """

    def process_loaded_data(self, vendtech, id_vendtech):
        parameters = (vendtech, id_vendtech)
        result = self.db_executor.call_proc('loaded_data', parameters, 'NUMBER')
        return result

    def get_table_columns(self, tablename, **kw):
        """
        Получение спецификации колонок в таблице

        :param tablename: наименование таблицы
        :type tablename: str

        """
        data_cursor = self.call_func('table_columns', (tablename, ))
        result = OrderedDict()
        for data in data_cursor:
            column_name = data['COLUMN_NAME']
            column_type = ''
            if data['DATA_TYPE'] == 'VARCHAR2':
                column_type = 'CHAR({})'.format(data['DATA_LENGTH'])
            result[column_name] = column_type
        return result

    def get_interface_package_errors(self, id_vendtech, **kw):
        parameters = (id_vendtech, None)
        data_cursor = self.call_func('pckg_errors', parameters)
        result = []
        for d in data_cursor:
            r = (str(d['LOG_DATE']), d['PROC_NAME'],
                 str(d['LOG_MSG'], errors='replace').encode('ascii', 'replace')
                 )
            result.append(r)
        return result
