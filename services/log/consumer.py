# coding: utf-8
from __future__ import absolute_import

from ..transport.consumer import Consumer


class LogConsumer(Consumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
