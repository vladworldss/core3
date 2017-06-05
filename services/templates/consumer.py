# coding: utf-8
import abc


class Consumer(metaclass=abc.ABCMeta):
    """
    Абстрактный класс консьюмера очереди сообщиний.
    """

    @abc.abstractproperty
    def pid(self, *args, **kwargs):
        pass

    @abc.abstractproperty
    def consumer_tag(self, *args, **kwargs):
        """
        Уникальный тэг консьюмера.
        Выдается при связывании консьюмера с каналом очереди сообщений.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    # ________Main_consuming_method

    @abc.abstractmethod
    def callback(self, *args, **kwargs):
        """
        Метод вызывается, когда брокер направляет сообщение на обработку.
        """
        pass

    # _________

    @abc.abstractclassmethod
    def publish(self, *args, **kwargs):
        """
        Метод публикации сообщения в очередь.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_store(self):
        """
        Метод получения worker_store, уникального для каждого сервиса.

        :return:
        """
        pass

    # _________Verify_methods

    @staticmethod
    def _isinstance(instance, Class):
        """
        Статичный метод-обертка над isinstance.
        В случае, если первый аргумент не является экземпляром класса,
        переданного во втором аргументе, возбуждается TypeError.

        :param instance:
        :param Class:
        :return:
        """
        if not isinstance(instance, Class):
            msg = f"{instance.__class__} must be subclass of <class {Class.__name__}>"
            raise TypeError(msg)
        return instance

    @staticmethod
    def _issubclass(SubClass, Class):
        """
        Статичный метод-обертка над issubclass.
        В случае, если первый аргумент не является дочерним классом класса,
        переданного во втором аргументе, возбуждается TypeError.

        :param SubClass:
        :param Class:
        :return:
        """
        if not issubclass(SubClass, Class):
            msg = f"{SubClass.__name__} must be subclass of <class {Class.__name__}>"
            raise TypeError(msg)
        return SubClass

    # ________

    class Msg(metaclass=abc.ABCMeta):
        """
        Абстрактрый класс сообщений-тасок (задач), которые передаются между
        сервисами и обрабатываются консьюмерами.

        Атрибут required_args определяется для каждого сервиса,
        исходя из его бизнес-логики.
        """

        @abc.abstractproperty
        def required_fields(self):
            """
            Свойство возвращает необходимые базовые поля сообщения.
            """
            pass

        @abc.abstractproperty
        def service_fields(self):
            """
            Свойство возвращает уникальный для каждого сервиса набор полей в 'service_fileds'.
            """
            pass

        @abc.abstractmethod
        def set_result(self, status, info):
            """
            Метод проставляет результат в сообщение + info

            :param msg:
            :param kwargs:
            :return:
            """
            pass
