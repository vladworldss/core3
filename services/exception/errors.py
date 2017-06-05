# coding: utf-8


class __Error(Exception):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(self.__doc__, *args, **kwargs)


# Transport Errors - - - - - - - - -

class TransportError(__Error):
    """Ошибка транспортного процесса"""


class RabbitError(TransportError):
    """Ошибка службы rabbitmq"""


# MsgQueue Errors - - - - - - - - -

class MsgQueueError(__Error):
    """Ошибка очереди сообщений"""


class BindConsumerError(MsgQueueError):
    """Ошибка при биндинге консьюмера"""


# Consumer Errors - - - - - - - - -

class ConsumerError(__Error):
    """Ошибка процесса консьюмера"""


class ImportWorkerError(ConsumerError):
    """Ошибка при импорте worker'a из worker_store"""


# Worker Errors - - - - - - - - -

class WorkerError(__Error):
    """Ошибка воркера"""


class RunWorkerError(WorkerError):
    """Ошибка выполнения worker'а."""


# Msg Errors - - - - - - - - -

class MsgError(__Error):
    """Ошибка сообщения"""



