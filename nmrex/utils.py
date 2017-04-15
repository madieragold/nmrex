import os
import contextlib


@contextlib.contextmanager
def chdir(path):
    starting_directory = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(starting_directory)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def rm(pattern):
    os.system('find . -name \{} -type f -delete'.format(pattern))


def fname(path):
    if path[-1] == '/':
        path = path[:-1]
    return os.path.split(path)[1]
