# coding: utf-8
from __future__ import absolute_import

from ..transport.consumer import BlockConsumer
from . import worker_store


class DlRawConsumer(BlockConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_store(self):
        return worker_store

    class Msg(BlockConsumer.Msg):
        """
        Класс сообщений dlraw-консьюмера
        """
        __service_fields = ['vendtech', 'id_vendtech', 'id_session',
                            'id_omc', 'id_mr', 'db_credentials', 'download_dir', 'configs']
        service_name = 'DlRaw'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @property
        def service_fields(self):
            return self.__service_fields
