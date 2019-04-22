import glob
from threading import Thread

from src.utils.constants import HOME_PATH


def find_file(name, path, file_type):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c

    if path[-1] == "/":
        path = path[:-1]
    glob_arg = '{}/**/{}.{}'.format(path, ''.join(map(either, name)), file_type)
    return glob.glob(glob_arg, recursive=True)


def get_home_path():
    return HOME_PATH


def threaded(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


def debug():
    return True


def log(message):
    if debug():
        print(message)

