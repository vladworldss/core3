# coding: utf-8
from __future__ import absolute_import

import pprint
import json
from collections import OrderedDict

from ..templates.consumer import Consumer
from ..templates.amqp import Queue
from ..exception.errors import *


__all__ = ['BlockConsumer']


class BlockConsumer(Consumer):
    """
    Консьюмер работает в синхронном режиме (1 сообщение - 1 воркер).
    """
    __slots__ = ('__pid', '__consumer_tag',
                 '__queue', '__exchange', '__log', '__store'
                 )

    def __init__(self, queue, log='', exchange=''):
        """

        :param queue: экземпляр очереди сообщений.
        :param exchange: обменник aka router
        """
        # пока работаем без exchange
        self.__exchange = exchange
        self.__queue = self._isinstance(queue, Queue)
        self.__log = log

        self.__pid = ''
        self.__consumer_tag = ''
        self.__store = self.get_store()

    @property
    def exchange(self):
        return self.__exchange

    @property
    def queue(self):
        return self.__queue.name

    @property
    def pid(self):
        return self.__pid

    @pid.setter
    def pid(self, id):
        if not self.__pid:
            self.__pid = id

    @property
    def consumer_tag(self):
        return self.__consumer_tag

    @consumer_tag.setter
    def consumer_tag(self, tag):
        if not self.__consumer_tag:
            self.__consumer_tag = tag
        else:
            print(ConsumerError('Консьюмеру уже назначен тэг!'))

    # _________Main_consuming_method

    def callback(self, channel, method, properties, body):
        """

        :param channel:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        try:
            msg = self.Msg(**json.loads(body))
            action = msg.action.capitalize()
            Worker = getattr(self.__store, action)
            res = Worker(msg).run()
            msg.set_result(status='Ok', info=res)

        except (MsgError, json.decoder.JSONDecodeError) as e:
            msg = self.Msg()
            txt = f"Сообщение <{body}> имеет неверный формат. Info: {e}"
            msg.set_result(status='Error', info=txt)

        except ImportWorkerError as e:
            txt = f"Ошибка при импорте worker. Info: <{e}>"
            msg.set_result(status='Error', info=txt)

        except RunWorkerError as e:
            txt = f"Worker завершился с ошибкой. Info: <{e}>."
            msg.set_result(status='Error', info=txt)

        finally:
            print('# '*30)
            pp = pprint.pformat(msg.__repr__(), indent=1, width=80, depth=None)
            print(pp)
            if self.__log:
                self.publish(self.__log, msg.__repr__())
            channel.basic_ack(delivery_tag=method.delivery_tag)

    # _________

    def publish(self, queue_name, msg, exchange=''):
        self.__queue.publish(queue_name, msg, exchange)

    class Msg(Consumer.Msg):
        """
        В атрибуте класса __required_fields находятся обязательные поля таски.
        """

        __required_fields = ['source', 'destination', 'action', 'body', 'status', 'info']

        def __init__(self, *args, **kwargs):
            self.__fields = set()
            required_fields = OrderedDict.fromkeys(self.__required_fields, '')
            self.set_fields(**required_fields)

            if kwargs:
                self.issubset(required_set=self.required_fields, **kwargs)
                self.issubset(required_set=self.service_fields, **kwargs['body'])
                self.set_fields(**kwargs)

        @property
        def required_fields(self):
            return self.__required_fields

        @staticmethod
        def issubset(required_set, **custom_set):
            """

            :param required_set:
            :param custom_set:
            :return:
            """
            if not set(custom_set).issubset(set(required_set)):
                raise MsgError('Сообщение имеет неверный формат: '
                               'отсутствуют обязательные аргументы!')

        def set_fields(self, **kwargs):
            try:
                for attr in kwargs:
                    setattr(self, attr, kwargs[attr])
                    self.__fields.add(attr)
            except Exception as e:
                raise MsgError(e)

        def set_result(self, status, info=''):
            self.status = status
            self.info = info

        def __repr__(self):
            msg = OrderedDict()
            for key in self.__fields:
                value = getattr(self, key)
                msg.update({key: value})
            return json.dumps(msg, ensure_ascii=False)
