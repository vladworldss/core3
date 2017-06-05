import abc
import re
import pysftp

from core3.services.templates.decorators import has_methods


@has_methods('close')
class Connection(metaclass=abc.ABCMeta): pass


class Loader(metaclass=abc.ABCMeta):

    def __init__(self, confs):
        self.__confs = []
        self.__connection = None

    @property
    def confs(self):
        return self.__confs

    @confs.setter
    def confs(self, _confs):
        self.__confs = []
        self.__confs.extend(_confs)

    @abc.abstractmethod
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, conn):
        if not isinstance(conn, Connection):
            raise TypeError('Settings does not have required attrs')
        elif self.__connection:
            self.__connection.close()
        self.__connection = conn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.__connection = None

    @abc.abstractmethod
    def load(self, *args, **kw):
        pass

    @abc.abstractmethod
    def close(self, *args, **kw):
        pass









class Sftp(Loader):

    def load(self, **kw):
        """
        Загрузка с удаленного sftp-сервера

        :return: код ошибки (0 --- ошибки нет, 1 --- ошибка есть)
        :rtype: int
        """
        for id_serv, configs in self.confs.items():
            for i, config in enumerate(configs):
                if not i:
                    credentials = {
                        'host': config['server_name'],
                        'username': config['login'],
                        'password': config['password']
                    }
                    self.

        sftp = pysftp.Connection(**credentials)

        full_path_to = self.raw_path + '/' + self.dir_to

        # получение списка файлов с фильтрацией по self.masks
        sftp_files = self.get_sftp_files_list(sftp, self.dir_from, self.masks)


        # загрузка файлов
        sftp_binary(sftp, sftp_file, full_path_to)

        return 0

    def get_sftp_files_list(self, sftp, path, mask):
        """
        Получение списка файлов по маске и сохранение их в рабочую дирректорию.

        :param sftp: sftp-клиент
        :param path: путь к файлам
        :param mask: маска для поиска файлов
        :return: sftp_list - список файлов
        """

        sftp.cwd(path)
        sftp_list = sftp.listdir()

        mask = mask.replace('.', '\.').replace('*', '.*?') + '$'
        regex = re.compile(mask)

        return [i for i in sftp_list if re.match(regex, i)]