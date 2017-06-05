# coding: utf-8
from __future__ import absolute_import

import abc


class Producer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def publish(self, *args, **kwargs):
        pass
