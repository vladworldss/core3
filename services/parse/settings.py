# coding: utf-8
# flake8: noqa
"""
Модуль для конфигов сервиса Parse.
"""
from __future__ import absolute_import

from ..templates.config import create_conf

#
PARSER_DIR = ''

# DC, MPConv
SORT_CMD = 'sort -S 1024M'

# утилита распаковки архивов
ARCHIVE_UTIL_CMD = '7z'

# регулярное вырпжение, описывающее поддерживаемые архивы для распаковки
SUPPORTED_ARCHIVES = '.*\.(rar|tar\.gz|tar\.Z|tar|tgz|zip|gz)'

# Команда для запаковки архива
PACK_CMD = '7z a {folder}.7z ./{folder}/*'

# Команда для распаковки архива
UNPACK_CMD = '7z x -aoa {folder}.7z -o{folder}'

RAW_FILE = '/Users/vladworld/Documents/IOSS/develop/files/raw/HUA_HR/Sharing_eNodeB_para.csv'

FLUSH_DIR = '/Users/vladworld/Documents/IOSS/develop/files/dat/HUA_HR'


def get_conf():
    """
    Фабричный метод для микросервиса Parse.
    :return:
    """
    return create_conf(service_name='parse', type='process', count=20)

