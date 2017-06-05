# coding: utf-8
import abc


class Queue(metaclass=abc.ABCMeta):
    """
    Абстрактный класс для очереди сообщений протокола AMQP.
    """

    # Service methods - - - - - - - - -

    @abc.abstractmethod
    def start_consuming(self, *args, **kwargs):
        """
        Метод старта прослушивания канала очереди сообщений.
        На момент запуска должны быть привязаны консьюмер и назначены их callback.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abc.abstractmethod
    def stop_consuming(self, *args, **kwargs):
        """
        Метод отвязки консьюмера и завершение прослушивания канала связи.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abc.abstractmethod
    def restart_consuming(self, *args, **kwargs):
        """
        Метод рестарта прослушивания канала очереди сообщений.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    # Creating methods - - - - - - - - -

    @abc.abstractmethod
    def make_queue(self, *args, **kwargs):
        """
        Метод создания и регистрации очереди сообщений.
        Установка режимов работы очереди.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    # Binding methods - - - - - - - - -

    @abc.abstractmethod
    def bind(self, *args, **kwargs):
        """
        Метод связывания канала очереди с консьюмером.
        Консьюмеру назначается уникальный идентификационный тэг.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abc.abstractmethod
    def unbind(self, *args, **kwargs):
        """
        Метод отвязки консьюмера от канала очереди.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    # Class methods - - - - - - - - -

    @abc.abstractclassmethod
    def get_new_connection(self, *args, **kwargs):
        """
        Получение объекта соединения со службой rabbitmq.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abc.abstractclassmethod
    def get_publish_properties(self, *args, **kwargs):
        """
        Метод получения настроек для публикации сообщения в очередь.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abc.abstractclassmethod
    def publish(self, *args, **kwargs):
        pass

    # Property's - - - - - - - - -

    @abc.abstractproperty
    def name(self, *args, **kwargs):
        pass
