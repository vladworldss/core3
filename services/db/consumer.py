# coding: utf-8
# flake8: noqa
from __future__ import absolute_import

from ..transport.consumer import BlockConsumer
from . import worker_store


class DbConsumer(BlockConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_store(self):
        return worker_store

    class Msg(BlockConsumer.Msg):
        """
        Класс сообщений db-консьюмера
        """
        __service_fields = ['db_type', 'session_data', 'dlraw_data', 'parse_data', 'load_data']

        service_name = 'DB'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @property
        def service_fields(self):
            return self.__service_fields


"""
{
    # S E S S I O N
    {'session_data': dict.fromkeys(
        ['vendor', 'technology', 'vendtech', 'id_vendtech', 'id_parser', 'id_session'], '')
    },

    # D L R A W
    {'dlraw_data': {
        'conf': dict.fromkeys(
            [
            'id_conf', 'id_omc', 'id_server', 'dir_from', 'folder_to', 'dir_to', 
            'mask_remote', 'mask_archive', 'mask_files', 'min_files', 'max_files', 
            'id_vendtech', 'id_mr', 
            'raw_files': dict.fromkeys(['id_file', 'name', 'status'], '')
            ], ''),

        'server': dict.fromkeys(
            ['id_server', 'server_name', 'login', 'password', 'type'], '')
    }
},

    # P A R S E
    {
        'parse_data': dict.fromkeys(['bit_parameter_data', 'mo_type_data', 'parameter_type_data'], '')
    },

    # L O A D
    {'load_data': dict.fromkeys(
        ['datfile_dir', 'datfile_format', 'datfile_live_dates_count', 'ctl_file_content', 'ctl_dir'], '')
    }
}
"""

