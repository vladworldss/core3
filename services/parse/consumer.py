# coding: utf-8
from __future__ import absolute_import

from ..transport.consumer import BlockConsumer
from . import worker_store


class ParseConsumer(BlockConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_store(self):
        return worker_store

    class Msg(BlockConsumer.Msg):
        """
        Класс сообщений parse-консьюмера
        """
        __service_fields = ['vendtech', 'id_omc', 'id_mr', 'id_vendtech', 'raw_file', 'flush_dir']
        service_name = 'Parse'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @property
        def service_fields(self):
            return self.__service_fields
