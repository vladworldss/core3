# coding: utf-8
import abc


class Worker(metaclass=abc.ABCMeta):
    """
    Абстрактный класс для запуска задач сервиса.
    """
    def __init__(self, msg, *args, **kw):
        self.msg = msg

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return: str info
        """
        pass


class Kill(Worker):
    """
    Класс уничтожения процесса.
    """
    pass


class Test(Worker):
    """
    Тестовый воркер.
    """
    def __init__(self, msg):
        super().__init__(msg)

    def run(self):
        from time import sleep
        from random import randint

        delay = randint(5, 60)
        sleep(delay)

        with open(f'test_file', 'a') as out:
            print(self.msg, file=out)
            print('#'*30, file=out)
