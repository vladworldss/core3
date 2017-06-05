# coding: utf-8
# flake8: noqa
"""
Модуль для конфигов сервиса DlRaw.
"""
from __future__ import absolute_import
import os

from core3.settings import BASE_PARSER_DIR
from ..templates.config import create_conf


# Параметр для определения "свежести" файлов
DLRAW_OFFSET = 1

# Полный путь к директории, куда будут загружены RAW файлы
RAW_FILE_BASEDIR = os.path.join(BASE_PARSER_DIR, 'raw')

# Полный путь к директории, содержащей бэкап-копии RAW файлов
BACKUP_BASEDIR = os.path.join(BASE_PARSER_DIR, 'backup')


def get_conf():
    """
    Фабричный метод для микросервиса DlRaw.
    :return:
    """
    # TODO: не нравиццца!
    return create_conf(service_name='dlraw', type='thread', count=20,
                       download_dir=RAW_FILE_BASEDIR
                       )
