# coding: utf-8
# flake8: noqa
"""
Модуль настроек для траспорта (служб передачи сообщений, системные зависимости и т.д.)
"""
from ..templates.config import create_conf

# Путь до RabbitMQ, который прописан в bash
RABBITMQ_PATH = '/usr/local/sbin/'
RABBITMQCTL = 'rabbitmqctl'
RABBITMQ_SERVER = 'rabbitmq-server'


def get_conf():
    """
    Фабричный метод для получения конфигов транспорта.
    :return:
    """
    return create_conf('rabbitmq', RABBITMQ_PATH=RABBITMQ_PATH, RABBITMQCTL=RABBITMQCTL,
                       RABBITMQ_SERVER=RABBITMQ_SERVER
                       )