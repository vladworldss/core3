# coding: utf-8
from __future__ import absolute_import

from ..templates.producer import Producer
from .amqp import BlockQueue as Queue


class BlockingProducer(Producer):
    """
    Класс для публикации сообщений в очередь.
    """
    def __init__(self, queue):
        self.queue = queue
        self.msg_type = {}

    def set_msg_type(self, msg_type):
        self.msg_type[msg_type.service_name] = msg_type

    def publish(self, queue_name, msg, exchange=''):
        self.queue.publish(queue_name, msg, exchange)

    def __call__(self, queue_name, msg):
        self.publish(queue_name, msg)
