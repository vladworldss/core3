# coding: utf-8
# flake8: noqa
"""
Модуль для конфигов сервиса Db.
"""
from collections import namedtuple, OrderedDict


def create_conf(service_name, **kwargs):
    """
    Метод создания объекта настроек микросервиса.

    :param service_name: имя микросервиса.
    :param kwargs: именованные аргументы, по которым осуществляется доступ к настройкам.
    :return:  namedtuple.
    """
    name = str(service_name).capitalize()
    keys = []
    kw = OrderedDict()
    if kwargs:
        kw.update(kwargs)
        keys = kw.keys()
    CongCls = namedtuple(f'{name}Conf', ['service_name', *keys])
    return CongCls(service_name, *kw.values())

