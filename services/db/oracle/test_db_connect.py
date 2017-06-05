from core3.services.db.oracle import layer
from core3.services.db.oracle.settings import OracleDbConf as DbConf
from core3.services.db.oracle.executor import DbExecutor
# # # # # # # #


def get_config_test():
    with DbExecutor(DbConf) as ex:
        dlraw = layer.DlRaw(ex)
        session = layer.Session(ex)
        data = dlraw.get_confs(811)
        for key, value in data.items():
            print(f'\nCONFDATA: {key}={value}')
        data = session.get_data('ERC01')
        for key, value in data.items():
            print(f'\nDATA: {key}={value}')

get_config_test()
