# coding: utf-8
from core3.services.exception.errors import Error, ImportWorkerError
import sys

_ParseErrors = ('ParseError', 'NotifyError', 'BadAssError')

# Здесь описывать кстомные исключения для парсинга


class ParseError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NotifyError(Error):
    """Класс ошибки нотификации"""
    __slots__ = ()


# Alternative method: нуждается в осмыслении!


def make_new_method(name):
    def new(Class, *args, **kwargs):
        return Error.__new__(Class, name, *args, **kwargs)
    return new


def make_errors():
    for er_name in _ParseErrors:
        new = make_new_method(er_name)
        new.__name__ = "__new__"
        Class = type(er_name, (Error, ), dict(__slots__=(), __new__=new))
        globals()[er_name] = Class
        # setattr(sys.modules[__name__], er_name, Class)
        print(sys.modules[__name__])
