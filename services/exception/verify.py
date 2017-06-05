import sys


def version_verify(version=(3, 3)):
    """
    Функция проверки на python3.3+. Принимает tuple
    :param version:
    :return:
    """
    if not isinstance(version, tuple):
        raise Exception('argument must be tuple!')
    if sys.version_info < (3, 3):
        print('requires Python 3.3+ for collections.ChainMap')
        sys.exit(1)


def isInstance(instance, Class, ClsError=TypeError):
    """
    Полиморфный isinstance, возбуждающий ClsError.
    :param instance:
    :param Class:
    :param ClsError:
    :return:
    """
    if not isinstance(instance, Class):
        raise ClsError(f"{instance.__class__} "
                        f"must be subclass of <class {Class.__name__}>")
    return instance
