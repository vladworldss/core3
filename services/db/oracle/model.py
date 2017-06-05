# coding: utf-8
# TODO: ну, тут нужно будет все переписать
# http://ph.start-i.ru/w/parser/tables/
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import inspect


class BaseTable(object):
    """
    Базовый класс для моделей таблиц базы данных
    """

    # database table name
    db_table = None

    # похоже, это означает что таблицу нужно транкейтить перед заливкой
    truncatable = False

    # похоже, это означает таблицу в которую прогружаются .dat файлы
    is_dat = False

    # символ-разделитель колонок в DAT файле
    column_separator = '|'

    # __slots__ = ('db_table', 'truncatable', 'is_dat', 'column_separator')

    def __str__(self):
        """
        Строковое представление, использующееся для генерирования
        одной строки DAT файла
        """
        raise NotImplementedError('Subclasses should implement __str__!')

    @classmethod
    def columns(cls):
        """
        Список колонок таблицы, которые заполняются парсером

        :return: список колонок таблицы, заполняемые парсером
        :rtype: list
        """
        arg_spec = inspect.getargspec(cls.__init__)
        return map(lambda y: y.upper(),
                   filter(lambda x: x != 'self', arg_spec[0]))


class BitParameter(BaseTable):
    """
    Модель представляющая таблицу параметров
    """

    db_table = 'DS8_BIT_PARAMETER_MAP'

    __slots__ = ('short_alias', 'tprm_p_name', 'tmo_name', 'bit_number')

    def __init__(self, short_alias, tprm_p_name, tmo_name, bit_number, **kwargs):
        # алиас битового параметра, str
        self.short_alias = short_alias
        # наименование битового параметра, str
        self.tprm_p_name = tprm_p_name
        # наименование TMO, str
        self.tmo_name = tmo_name
        # номер бита, int
        self.bit_number = bit_number

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.short_alias, self.tprm_p_name,
            self.tmo_name, self.bit_number
        ]])


class MO(BaseTable):
    """
    Модель представляющая таблицу MO
    """

    db_table = 'MO'
    truncatable = True
    is_dat = True

    __slots__ = ('id_vendtech', 'id_mo', 'id_tmo', 'id_path', 'id_file',
                 'id_mo_cnm', 'id_mr', 'id_rg', 'id_raw', 'cname',
                 'mo_ref', 'id_omc')

    def __init__(self, id_vendtech, id_mo, id_tmo, id_path, id_file,
                 id_mo_cnm, id_mr, id_rg, id_raw='', cname='',
                 mo_ref='', id_omc='', **kwargs):

        # идентификатор вендора/технологии
        self.id_vendtech = id_vendtech
        # идентификатор MO
        self.id_mo = id_mo
        # идентифкатор TMO
        self.id_tmo = id_tmo
        # идентификатор RAW файла
        self.id_file = id_file
        # идентификатор PATH
        self.id_path = id_path
        # идентификатор контроллера
        self.id_mo_cnm = id_mo_cnm
        # идентификатор макрорегиона
        self.id_mr = id_mr
        # идентификатор региона
        self.id_rg = id_rg
        # идентификатор MO в пределах RAW файла
        self.id_raw = id_raw
        # название контроллера
        self.cname = cname  # str
        # строковая ссылка на MO в рамках иерархии
        self.mo_ref = mo_ref  # str
        # идентификатор OMC
        self.id_omc = id_omc

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vendtech, self.id_mo, self.id_tmo, self.id_path,
            self.id_file, self.id_mo_cnm, self.id_mr,
            self.id_rg, self.id_raw, self.cname, self.mo_ref, self.id_omc
        ]])


class MORelation(BaseTable):
    """
    Модель представляющая таблицу взаимосвязей MO
    """

    db_table = 'RLT'
    truncatable = True
    is_dat = True

    __slots__ = ('id_vendtech', 'id_trlt', 'id_mo_p', 'id_mo_c', 'data')

    def __init__(self, id_vendtech, id_trlt, id_mo_p, id_mo_c, data='', **kwargs):
        # идентификатор вендора/технологии
        self.id_vendtech = id_vendtech
        # идентификатор типа взаимосвязи
        self.id_trlt = id_trlt
        # идентифкатор родительского MO
        self.id_mo_p = id_mo_p
        # идентификатор дочернего MO
        self.id_mo_c = id_mo_c
        # дополнительная информация
        self.data = data

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vendtech, self.id_trlt, self.id_mo_p,
            self.id_mo_c, self.data
        ]])


class MORelationType(BaseTable):
    """
    Модель представляющая таблицу типов взаимосвязей MO
    """

    db_table = 'TRLT'
    truncatable = False
    is_dat = True

    __slots__ = ('id_trlt', 'name')

    def __init__(self, id_trlt, name, **kwargs):
        # идентифкатор типа взаимосвязи
        self.id_trlt = id_trlt
        # название взаимосвязи (HIERARCY, LINK)
        self.name = name

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_trlt, self.name
        ]])


class MOType(BaseTable):
    """
    Модель представляющая таблицу типов MO
    """

    db_table = 'TMO'
    truncatable = True
    is_dat = True

    __slots__ = ('id_vendtech', 'id_tmo', 'id_tmo_p', 'name', 'prefix',
                 'renamed', 'comp_parameter', 'rel_type')

    def __init__(self, id_vendtech, id_tmo, id_tmo_p, name, prefix='',
                 renamed='', comp_parameter=0, rel_type=0, **kwargs):
        self.id_vendtech = id_vendtech
        self.id_tmo = id_tmo
        self.id_tmo_p = id_tmo_p
        self.prefix = prefix
        self.name = name
        # переименованное название TMO
        self.renamed = renamed or ''
        # признак композитного TMO
        self.comp_parameter = comp_parameter
        self.rel_type = rel_type

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vendtech, self.id_tmo, self.id_tmo_p, self.name,
            self.prefix, self.renamed, self.comp_parameter, self.rel_type
        ]])


class MR(BaseTable):
    """
    Модель представляющая таблицу макрорегионов
    """

    db_table = 'MR'
    truncatable = False
    is_dat = False

    __slots__ = ('id_mr', 'name', 'ins_date', 'verified')

    def __init__(self, id_mr, name, ins_date, verified, **kwargs):
        self.id_mr = id_mr
        # название макрорегиона
        self.name = name
        # дата добавления
        self.ins_date = ins_date
        # признак верификации
        self.verified = verified

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_mr, self.name, self.ins_date, self.verified
        ]])


class Omc(BaseTable):
    """
    Модель представляющая таблицу OMC
    """

    db_table = 'OMC'
    truncatable = False
    is_dat = False

    __slots__ = ('id_omc', 'id_vendtech', 'omc_name')

    def __init__(self, id_omc, id_vendtech, omc_name, **kwargs):
        self.id_omc = id_omc
        self.id_vendtech = id_vendtech
        self.omc_name = omc_name

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_omc, self.id_vendtech, self.omc_name
        ]])


class Parameter(BaseTable):
    """
    Модель представляющая таблицу параметров
    """

    db_table = 'PRM'
    truncatable = True
    is_dat = True

    __slots__ = ('id_vendtech', 'id_prm', 'id_tprm', 'id_mo', 'value')

    def __init__(self, id_vendtech, id_prm, id_tprm, id_mo, value, **kwargs):
        self.id_vendtech = id_vendtech
        self.id_prm = id_prm
        self.id_tprm = id_tprm
        self.id_mo = id_mo
        self.value = value

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vendtech, self.id_prm, self.id_tprm,
            self.id_mo, self.value
        ]])


class ParameterType(BaseTable):
    """
    Модель представляющая таблицу типов параметров
    """

    db_table = 'TPRM'
    truncatable = True
    is_dat = True

    # __slots__ = ('id_vendtech', 'id_tprm', 'id_tmo', 'name', 'prefix',
    #              'source', 'renamed', 'val_type', 'multiple', 'bit')

    def __init__(self, id_vendtech, id_tprm, id_tmo, name,
                 prefix='', source=0, renamed='', val_type=1,
                 multiple=0, bit='', **kwargs):

        self.id_vendtech = id_vendtech
        self.id_tprm = id_tprm
        self.id_tmo = id_tmo

        if prefix == 'None':
            prefix = None
        self.prefix = prefix

        self.name = name
        self.renamed = renamed or ''

        # класс типа параметров (0,1,2)
        self.source = source

        # численный или строковый тип
        self.val_type = val_type

        # признак множественности типа
        self.multiple = multiple

        # bit: признак битового типа параметров
        self.bit = bit or ''

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vendtech, self.id_tprm, self.id_tmo,
            self.name, self.prefix, self.source, self.renamed,
            self.val_type, self.multiple, self.bit
        ]])


class ParserLog(BaseTable):
    """
    Модель представляющая таблицу журналирования
    """

    db_table = 'PARSER_LOG'
    truncatable = False
    is_dat = False

    __slots__ = ('created', 'process', 'thread', 'log_level', 'message',
                 'name', 'from_file', 'from_line', 'function_name')

    def __init__(self, created, process, thread, log_level, message,
                 name, from_file, from_line, function_name, **kwargs):
        # дата создания записи журнала
        self.created = created
        # название процесса
        self.process = process
        # название потока
        self.thread = thread
        # уровень записи
        self.log_level = log_level
        # сообщение
        self.message = message
        # название
        self.name = name
        # имя файла
        self.from_file = from_file
        # номер строки
        self.from_line = from_line
        # имя функции
        self.function_name = function_name

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.created, self.process,
            self.thread, self.log_level, self.message,
            self.name, self.from_file, self.from_line, self.function_name
        ]])


class Path(BaseTable):
    """
    Модель представляющая таблицу путей
    """

    db_table = 'PATH'
    truncatable = True
    is_dat = True

    __slots__ = ('id_vendtech', 'id_path', 'id_mo', 'id_raw', 'p_level')

    def __init__(self, id_vendtech, id_path, id_mo, id_raw, p_level, **kwargs):
        self.id_vendtech = id_vendtech
        self.id_path = id_path
        self.id_mo = id_mo
        # идентифкатор MO внутри RAW файла
        self.id_raw = id_raw
        # уровень вложенности в иерархии
        self.p_level = p_level

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vendtech, self.id_path, self.id_mo,
            self.id_raw, self.p_level
        ]])


class RawFile(BaseTable):
    """
    Модель представляющая таблицу RAW файлов
    """

    db_table = 'RFILE'
    truncatable = False
    is_dat = False

    __slots__ = ('id_file', 'id_mr', 'name', 'id_vendtech', 'fileinfo',
                 'path', 'id_omc', 'modification_date', 'bad')

    def __init__(self, id_file, id_mr, name, id_vendtech, fileinfo='',
                 id_omc=1, modification_date='', bad='', path='', **kwargs):
        # идентификатор RAW файла
        self.id_file = id_file
        # идентификатор макрорегиона
        self.id_mr = id_mr
        # название RAW файла
        self.filename = name
        self.fileinfo = fileinfo
        self.id_omc = id_omc
        self.dirname = path

        self.id_vendtech = id_vendtech
        # дата загрузки
        self.modification_date = modification_date
        # признак плохого(битого, некорректного, пустого) RAW-файла
        self.bad = bad

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_file, self.id_mr, self.filename, self.fileinfo,
            self.dirname, self.id_omc, self.id_vendtech,
            self.modification_date, self.bad
        ]])


class DeltaModel(BaseTable):
    """
    Модель представляющая таблицу REP DELTA
    """

    db_table = 'REP_DELTA'
    truncatable = False
    is_dat = False

    __slots__ = (
        'id_vendtech', 'dt_from', 'dt_to', 'mr', 'id_mr', 'rg', 'id_rg',
        'cname', 'id_mo_cnm', 'cell_name', 'cell_cgi', 'id_mo_cell',
        'id_mo_old', 'id_mo_new', 'id_raw', 'mo_ref', 'id_path', 'id_tmo',
        'id_tprm', 'old_value', 'new_value'
    )

    def __init__(self, id_vendtech, dt_from, dt_to, mr, id_mr, rg, id_rg,
                 cname, id_mo_cnm, cell_name, cell_cgi, id_mo_cell, id_mo_old,
                 id_mo_new, id_raw, mo_ref, id_path, id_tmo,
                 id_tprm, old_value, new_value, **kwargs):
        self.id_vendtech = id_vendtech
        # дата старого среза в формате числа: ГГГГММДД
        self.dt_from = dt_from
        # дата нового среза в формате числа: ГГГГММДД
        self.dt_to = dt_to
        self.mr = mr
        self.id_mr = id_mr
        self.rg = rg
        self.id_rg = id_rg
        # название контроллера
        self.cname = cname
        # идентификатор контроллера
        self.id_mo_cnm = id_mo_cnm
        # название соты
        self.cell_name = cell_name
        # CGI соты
        self.cell_cgi = cell_cgi
        # идентификатор соты
        self.id_mo_cell = id_mo_cell
        # идентификатор объекта в старом срезе
        self.id_mo_old = id_mo_old
        # идентификатор объекта в новом срезе
        self.id_mo_new = id_mo_new
        # идентификатор объекта в RAW файле
        self.id_raw = id_raw
        # MO-REF объекта в RAW файле
        self.mo_ref = mo_ref
        # идентификатор пути в иерархии из нового среза
        self.id_path = id_path
        self.id_tmo = id_tmo
        self.id_tprm = id_tprm
        # старое значение
        self.old_value = old_value
        # новое значение
        self.new_value = new_value

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vendtech, self.dt_from, self.dt_to, self.mr, self.id_mr,
            self.rg, self.id_rg, self.cname, self.id_mo_cnm, self.cell_name,
            self.cell_cgi, self.id_mo_cell, self.id_mo_old, self.id_mo_new,
            self.id_raw, self.mo_ref, self.id_path, self.id_tmo, self.id_tprm,
            self.old_value, self.new_value
        ]])


class RG(BaseTable):
    """
    Модель представляющая таблицу регионов
    """

    db_table = 'RG'
    truncatable = False
    is_dat = False

    __slots__ = ('id_rg', 'id_mr', 'name', 'ins_date', 'verified')

    def __init__(self, id_rg, id_mr, name, ins_date, verified, **kwargs):
        self.id_rg = id_rg
        self.id_mr = id_mr
        self.name = name
        # время добавления
        self.ins_date = ins_date
        # признак верификации
        self.verified = verified

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_rg, self.id_mr, self.name, self.ins_date, self.verified
        ]])


class RGMap(BaseTable):
    """
    Модель представляющая таблицу маппинга регионов и контроллеров
    """

    db_table = 'RG_MAP'
    truncatable = False
    is_dat = False

    __slots__ = ('id_vendtech', 'cname', 'id_rg',
                 'ins_date', 'verified', 'id_omc')

    def __init__(self, id_vendtech, cname, id_rg, ins_date, verified, id_omc, **kwargs):
        self.id_vendtech = id_vendtech
        # название контроллера
        self.cname = cname
        self.id_rg = id_rg
        # время добавления
        self.ins_date = ins_date
        # признак верификации
        self.verified = verified
        self.id_omc = id_omc

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vendtech, self.cname, self.id_rg, self.id_omc,
            self.ins_date, self.verified
        ]])


class Technology(BaseTable):
    """
    Модель представляющая таблицу технологий
    """

    db_table = 'TECHNOLOGY'
    truncatable = False
    is_dat = False

    __slots__ = ('id_tech', 'name_short', 'name_long')

    def __init__(self, id_tech, name_short, name_long, **kwargs):
        self.id_tech = id_tech
        # сокращенное наименование технологии
        self.name_short = name_short
        # наименование технологии
        self.name_long = name_long

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_tech, self.name_short, self.name_long
        ]])


class Vendor(BaseTable):
    """
    Модель представляющая таблицу вендора
    """

    db_table = 'VENDOR'
    truncatable = False
    is_dat = False

    __slots__ = ('id_vend', 'vendor_name', 'info')

    def __init__(self, id_vend, vendor_name, info, **kwargs):
        self.id_vend = id_vend
        # наименование вендора
        self.vendor_name = vendor_name
        # информация
        self.info = info

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vend, self.vendor_name, self.info
        ]])


class VendTech(BaseTable):
    """
    Модель представляющая таблицу вендора/технологии
    """

    db_table = 'VENDTECH'
    truncatable = False
    is_dat = False

    __slots__ = ('id_vendtech', 'vendtech_code', 'id_vend', 'id_tech')

    def __init__(self, id_vendtech, vendtech_code, id_vend, id_tech, **kwargs):
        # идентификатор вендора/технологии
        self.id_vendtech = id_vendtech
        # ключевое название
        self.vendtech_code = vendtech_code
        # идентификатор вендора
        self.id_vend = id_vend
        # идентификатор технологии
        self.id_tech = id_tech

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_vendtech, self.vendtech_code, self.id_vend, self.id_tech
        ]])


class DlrawServer(BaseTable):
    """
    Класс, определяющий модель конфигураций серверов.
    """
    def __init__(self, id_server, server_name, login, password, type, **kwargs):
        # идентификатор сервера
        self.id_server = id_server
        # наименование сервера
        self.server_name = server_name
        self.login = login
        self.password = password
        self.type = type

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_server, self.server_name, self.login,
            self.password, self.type
        ]])


class DlrawConfig(BaseTable):
    """
    Класс, определяющий модель конфигураций выгрузок
    """
    def __init__(self, id_conf, id_omc, id_server, dir_from, folder_to,
                 dir_to, mask_remote, mask_archive, mask_files, min_files,
                 max_files, id_vendtech, id_mr, **kwargs):
        self.id_conf = id_conf
        self.id_omc = id_omc
        self.id_server = id_server
        self.dir_from = dir_from
        self.folder_to = folder_to
        self.dir_to = dir_to
        self.mask_remote = mask_remote
        self.mask_archive = mask_archive
        self.mask_files = mask_files
        self.min_files = min_files
        self.max_files = max_files
        self.id_vendtech = id_vendtech
        self.id_mr = id_mr

    def __str__(self):
        return self.column_separator.join([str(item) for item in [
            self.id_conf, self.id_omc, self.id_server,
            self.dir_from, self.folder_to, self.dir_to, self.mask_remote,
            self.mask_archive, self.mask_files, self.min_files,
            self.max_files, self.id_vendtech, self.id_mr
        ]])


MODELS = (
    # read
    BitParameter,  # одна для всех вендоров - список битовых параметров
    MORelationType,  # везде 1

    # write
    MO, MORelation, Parameter, Path,  # DS8_{}_L

    # append
    DeltaModel,

    # merge
    MOType, ParameterType,

    # not used in parser
    # manual
    MR, RG,
    Omc, Technology, Vendor, VendTech, RGMap,

    ParserLog,  # туда все пишется но оч много пишется, не исп

    # проверить
    RawFile,
)
