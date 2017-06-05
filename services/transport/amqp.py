# coding: utf-8
from __future__ import absolute_import

import os
import sys
from multiprocessing import synchronize, sharedctypes
import pika

from ..templates.amqp import Queue
from ..templates.consumer import Consumer
from ..exception.errors import *
from ..exception.verify import isInstance


class BlockQueue(Queue):
    """

    """
    __slots__ = ('__name', '__host', '__exchange', '__prefetch_count',
                 '__prefetch_size', '__durable', '__connection', '__channel',
                 '__consumer', '__lock', '__created')

    def __init__(self, name, host='localhost', exchange='',
                 prefetch_count=1, prefetch_size=0, durable=True, auto_delete=True):
        """
            self.prefetch_count - не отдавать подписчику единовременно более одного сообщения
        (подписчик не получит новое сообщение, до тех пор пока не обработает и не подтвердит предыдущее.
        RabbitMQ передаст сообщение первому освободившемуся подписчику).
            self.durable - устойчивая очередь (если consumer не подтверждает обработку сообщения, оно не удаляется)

        """
        # Queue settings
        self.__name = str(name)
        self.__host = host
        self.__exchange = exchange
        self.__prefetch_count = prefetch_count
        self.__prefetch_size = prefetch_size
        self.__durable = bool(durable)
        self.__auto_delete = bool(auto_delete)

        self.__connection = None
        self.__channel = None
        self.__consumer = None

        # Мульпроцессный lock
        self.__lock = None
        # Мультипроцессный семафор состояния очереди
        self.__created = False

    # Property's - - - - - - - - -

    @property
    def name(self): return self.__name

    @property
    def host(self): return self.__host

    @property
    def exchange(self): return self.__exchange

    @property
    def prefetch_count(self): return self.__prefetch_count

    @property
    def prefetch_size(self): return self.__prefetch_size

    @property
    def durable(self): return self.__durable

    @property
    def auto_delete(self): return self.__auto_delete

    @property
    def connection(self): return self.__connection

    @connection.setter
    def connection(self, value):
        if not self.__connection: self.__connection = value

    @property
    def channel(self): return self.__channel

    @channel.setter
    def channel(self, value):
        if not self.__channel: self.__channel = value

    @property
    def consumer(self): return self.__consumer

    @consumer.setter
    def consumer(self, value):
        if not self.__consumer: self.__consumer = value

    @property
    def lock(self): return self.__lock

    @lock.setter
    def lock(self, value):
        if not self.__lock: self.__lock = value

    # - - - - - - - - -

    @staticmethod
    def _isinstance(instance, Class): return isInstance(instance, Class)

    # - - - - - - - - -

    def print(self, *args, **kwargs):
        """
        Метод берет lock и делает принт, чтобы исключить смешивание output в одном stdout.
        :param args:
        :param kwargs:
        :return:
        """
        if self.lock:
            with self.lock:
                print(*args, **kwargs)
        else:
            print(*args, **kwargs)

    # Class-methods - - - - - - - - -

    @classmethod
    def get_publish_properties(cls, delivery_mode=2):
        """
        Устанавливает тип публикуемых сообщений как "устойчивые".
        Возвращает объект свойства публикуемых сообщений.

        :param delivery_mode: устанавливает сообщение как устойчивое
        :type delivery_mode: int
        :return: pika.BasicProperties
        """
        return pika.BasicProperties(delivery_mode=delivery_mode, )

    @classmethod
    def get_new_connection(cls, host='localhost'):
        """
        Возвращает объект блокируемого соединения.

        :param host: адрес хоста, на котором запущен брокер сообщений.
        :type host: str
        :return: pika.BlockingConnection
        """
        return pika.BlockingConnection(pika.ConnectionParameters(host))

    @classmethod
    def publish(cls, queue_name, msg, exchange=''):
        """
        По-дефолту публикация устойчивых сообщений (ожидают подтверждения со стороны консьюмера).

        :param queue_name: имя очереди, куда будет отправлено сообщение
        :type queue_name: str
        :param msg: тело сообщения
        :type msg: json.dumps() aka str
        :param exchange: обменник (по-умолчанию отсутствует)
        :type exchange: str
        :return:
        """
        prop = cls.get_publish_properties()
        with cls.get_new_connection() as conn:
            channel = conn.channel()
            channel.basic_publish(exchange=exchange, routing_key=queue_name,
                                  body=msg, properties=prop)

    # Service methods - - - - - - - - -

    def start_consuming(self):
        """
        Запуск процесса прослушивания очереди. На момент запуска
        консьюмер должен быть связан с очередью.

        :return:
        """
        self.print(f'Запускаем очередь={self.name}...')
        if not self.consumer:
            raise BindConsumerError('Консьюмер не найден!')
        self.print(f'Очередь={self.name} успешно запущена. '
                   f'Ожидание входящих сообщений. '
                   f'Для выхода нажмите Ctr+C')
        self.channel.start_consuming()

    def stop_consuming(self):
        """
        Отвязка консьюмера от очереди.
        Остановка процесса прослушивания очереди.
        :return:
        """
        # блокирующий режим
        self.print(f'Начало остава очереди={self.name}...')
        self.unbind()
        self.print('Все консьюмеры были отвязаны.')
        self.channel.stop_consuming()
        self.print(f'Очередь={self.name} успешно остановлена.')

    def restart_consuming(self, *args, **kwargs):
        pass

    # Creating methods - - - - - - - - -

    def make_queue(self):
        self.print(f'Создаем очередь={self.name}...')
        self.connection = self.get_new_connection(host=self.host)
        self.channel = self.connection.channel()
        with self.lock:
            if not self.created.value:
                # TODO: есть autodelete
                self.channel.queue_declare(self.name, durable=self.durable, auto_delete=self.auto_delete)
                self.channel.basic_qos(prefetch_size=self.prefetch_size,
                                         prefetch_count=self.prefetch_count
                                         )
                self.created.value = True
        self.print(f'Очередь={self.name} успешно создана.')

    def queue_delete(self):
        self.print(f'Удаляем очередь={self.name}...')
        with self.lock:
            if not self.created.value:
                self.print(MsgQueueError(
                    f'DeleteWarning: очередь={self.name} уже удалена!'))
            else:
                self.channel.queue_delete(queue=self.name)
                self.created.value = False
                self.print(f'Очередь={self.name} успешно удалена')
        self.connection.close()

    # Binding methods - - - - - - - -

    def bind(self, consumer):
        self.print(f'Связываем очередь={self.name} с консьюмером.')
        self._isinstance(consumer, Consumer)
        consumer.pid = os.getpid()
        consumer.consumer_tag = self.channel.basic_consume(
            consumer_callback=consumer.callback, queue=self.name
        )
        self.consumer = consumer
        self.print(f'Консьюмер={consumer.consumer_tag} успешно '
                   f'привязан к очереди={self.name}')

    def unbind(self):
        self.print(f'Начинаем отвязывать консьюмер='
                   f'{self.consumer.consumer_tag} от очереди={self.name}')
        if not self.consumer:
            self.print(BindConsumerError(
                f'Консьюмер={self.consumer.consumer_tag} не найден'))
        else:
            self.channel.basic_cancel(consumer_tag=self.consumer.consumer_tag)
            self.print(f'Консьюмер={self.consumer.consumer_tag} '
                       f'успешно отвязан от очереди={self.name}.')
            self.consumer = None

    # - - - - - - - - -

    def __call__(self, consumer, lock, created):
        """
        Метод будет вызываться при запуске отдельного процесса.
        lock+created нужны для исключения повторного удаления очереди из другого процесса.

        :param consumer: экземпляр слушателя очереди
        :param lock: межпроцессный лок.
        :param created: межпроцессный флаг состояния rabbit-очереди
                        (False-очередь не запущена; True - очередь ожидает подключения).

        :return:
        """
        self.print(f'Adress queue: {self}')
        try:
            self.lock = self._isinstance(lock, synchronize.Lock)
            self.created = self._isinstance(created, sharedctypes.Synchronized)
            self.make_queue()
            self.bind(consumer)
            self.start_consuming()
        except KeyboardInterrupt:
            pass
        except SystemExit:
            print('!!!!'*10, 'Sysexit')
        finally:
            self.print('\nПолучено прерывание. Начинаем останов сервиса...')
            if not self.auto_delete:
                self.stop_consuming()
                self.queue_delete()
            self.print('Сервис остановлен.')
