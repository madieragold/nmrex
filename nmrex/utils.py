import os
import contextlib


@contextlib.contextmanager
def chdir(path):
    """Temporary change working directory. Should be used with the `with`
    statement.
    
    Parameters
    ----------
    path : str
        Path to the target directory.

    """
    starting_directory = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(starting_directory)


def mkdir(path):
    """Create all directories in the path if they do not exist yet.
    
    Parameters
    ----------
    path : str
        Path to the target directory.

    """
    if not os.path.exists(path):
        os.makedirs(path)


def rm(pattern):
    os.system('find . -name \{} -type f -delete'.format(pattern))


def fname(path):
    """Get name of directory or file.

    Parameters
    ----------
    path : str
        Path to the directory or file.

    Returns
    -------
    str
        Name of the directory or file.

    """
    if path[-1] == '/':
        path = path[:-1]
    return os.path.split(path)[1]


def subtract(df1, df2):
    return (df1 - df2).dropna(axis=1, how='all')