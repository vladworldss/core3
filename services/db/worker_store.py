# coding: utf-8
# flake8: noqa
from __future__ import absolute_import
from importlib import import_module

from ..templates.worker import Worker
from ..exception.errors import ImportWorkerError, WorkerError, MsgError


def get_db_classes(db_type):
    db_type = db_type.lower()

    try:
        settings = import_module(f'{db_type}.settings')
        executor = import_module(f'{db_type}.executor')
        layer = import_module(f'{db_type}.layer')

        return settings.DbConf, executor.DbExecutor, layer.DbLayer

    except ModuleNotFoundError:
        raise ImportWorkerError(f"{db_type}' does not support!")


class Common(Worker):
    """
    Воркер получения базовых конфигов.
    """

    def __init__(self, msg):
        super().__init__(msg)

    def run(self, *args, **kwargs):
        db_type = self.msg.body['db_type']
        DbConf, DbExecutor, DbLayer = get_db_classes(db_type)

        with DbExecutor(DbConf) as ex:
            layer = DbLayer(ex)
            layer.get_common_data(self.msg)


class DlRaw(Worker):
    """
    Воркер получения базовых конфигов.
    """

    def __init__(self, msg):
        super().__init__(msg)

    def run(self, *args, **kwargs):
        db_type = self.msg.body['db_type']
        DbConf, DbExecutor, DbLayer = get_db_classes(db_type)

        with DbExecutor(DbConf) as ex:
            layer = DbLayer(ex)
            layer.get_dlraw_data(self.msg)
