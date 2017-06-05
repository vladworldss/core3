# coding: utf-8
from __future__ import absolute_import

import os
import time
import subprocess as sp
from collections import namedtuple

from core3.services.exception.errors import RabbitError
from .settings import get_conf


class Rabbit(object):
    """
    Класс API для взаимодействия с процессом брокера сообщений rabbitmq.
    """
    __slots__ = ('__config', '__rabbitmqctl', '__rabbitmq_server')

    def __init__(self):
        self.__config = get_conf()
        self.__rabbitmqctl = self.abs_rabbit_path(self.__config.RABBITMQCTL)
        self.__rabbitmq_server = self.abs_rabbit_path(self.__config.RABBITMQ_SERVER)

    @property
    def rabbitmqctl(self):
        return self.__rabbitmqctl

    @property
    def rabbitmq_server(self):
        return self.__rabbitmq_server

    def abs_rabbit_path(self, name):
        if not isinstance(name, str):
            raise TypeError('Name must be str-type.')
        return os.path.join(self.__config.RABBITMQ_PATH, name)

    @property
    def server_is_running(self):
        """
        Возвращает статус состояния rabbitmq-server. True - работает, False - остановлен.

        :return: bool
        """
        is_running = False
        cmd = f'{self.rabbitmqctl} status'
        res = self.call(cmd)
        if not res.err:
            is_running = True
        return is_running

    def start(self):
        if not self.server_is_running:
            print(f"Сервер не запущен. Начало запуска {self.rabbitmq_server} ...")
            cmd = f"sudo {self.rabbitmq_server} -detached"
            res = self.call(cmd)
            print(f"{self.rabbitmq_server} успешно запущен. Info: out:{res.out}, err:{res.err}")

            print(f"Запуск ноды...")
            cmd = f"{self.rabbitmqctl} start_app"
            res = self.call(cmd)

            # Delay на запуск брокера
            time.sleep(5)
            print(f'Нода запущена. Info: out:{res.out}, err:{res.err}')
            print('Просьба перезапустить приложение.')
            if not self.server_is_running:
                raise RabbitError("Нода не была запущена. Проверьте настройки.")
            return False
        else:
            print(f"Сервер {self.rabbitmq_server} уже запущен")
            return True

    def stop(self):
        f"""
        Метод останова rabbit-node.

        :return:
        """
        cmd = f"{self.rabbitmqctl} stop"
        res = self.call(cmd)
        return res

    def restart(self):
        f"""
        Метод перезапуска {self.rabbitmq_server}.
        :return:
        """
        pass

    @property
    def list_queues(self):
        """
        Возвращает список прослушиваемых очередей.

        :return:
        """
        cmd = f'{self.rabbitmqctl} list_queues'
        res = self.call(cmd)
        return res

    @property
    def list_connections(self):
        """
        Возвращает список активных соединений. По дефолту, в rabbit установлен таймаут,
        в течении которого, если консьюмер не откликается, его исключают.

        :return:
        """
        cmd = f'{self.rabbitmqctl} list_connections'
        res = self.call(cmd)
        return res

    def call(self, cmd):
        """
        Запускает переданную комманду в терминале, предварительно получив stdout, stderr.

        :param cmd:
        :return:
        """
        result = namedtuple('result', ['err', 'out'])
        with sp.Popen(cmd, shell=True, executable='/bin/bash', stdout=sp.PIPE, stderr=sp.PIPE) as pipe:
            err = pipe.stderr.readlines()
            out = pipe.stdout.readlines()
        result.err, result.out = err, out
        return result
