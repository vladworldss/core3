# coding: utf-8
from __future__ import absolute_import
import sys
import collections
import functools
from multiprocessing import freeze_support

# must be Python 3.3+
from core3.services.exception.verify import version_verify
version_verify()


def has_methods(*methods):
    """
    Декоратор класса, позволяющий использовать duck-type исходя из
    набора методов.

    :param methods: множество требуемых методов.
    :return: декоратор класса.
    """
    def decorator(Base):
        def __subclasshook__(Class, Subclass):
            if Class is Base:
                attrs = collections.ChainMap(
                    *(SuperClass.__dict__ for SuperClass in Subclass.__mro__)
                )
                if all(method in attrs for method in methods):
                    return True
            return NotImplemented
        Base.__subclasshook__ = classmethod(__subclasshook__)
        return Base
    return decorator


def freeze(func):
    """
    Декоратор функции, реализующий мультипроцессную логику для семейства OS Windows.

    :param func: декорируемая функция.
    :return: декоратор функции.
    """
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        if sys.platform[:3].lower() == 'win':
            freeze_support()
        res = func(*args, **kwargs)
        return res
    return wrap
