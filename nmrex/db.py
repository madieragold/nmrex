import logging
import nmrex
import os
import multiprocessing as mp
from functools import partial


def fetch(path, df):
    """Fetch new data base according to specified list of entries.
    
    Parameters
    ----------
    path : str
        Path to location of the new data base.
    df : pandas.DataFrame
        Data frame with columns `RCSB` and `BMRB` specifying entries for the
        new data base.

    """
    nmrex.utils.mkdir(path)
    with nmrex.utils.chdir(path):
        total = len(df)
        for index, rcsb, bmrb in df[['RCSB', 'BMRB']].itertuples():
            nmrex.utils.mkdir(rcsb)
            with nmrex.utils.chdir(rcsb):

                label = '{index}/{total} {rcsb}:{bmrb}'.format(
                    index=index + 1,
                    total=total,
                    rcsb=rcsb,
                    bmrb=bmrb,
                )

                try:
                    nmrex.fetch.structure(rcsb)
                    logging.info(
                        '{label} fetched structure'.format(
                            label=label
                        )
                    )
                except Exception as err:
                    logging.error(
                        ('{label} {exception} occured during structure '
                        'fetching: {msg}').format(
                            label=label,
                            exception=type(err).__name__,
                            msg=err.__str__(),
                        )
                    )

                try:
                    nmrex.fetch.shifts(bmrb)
                    logging.info(
                        '{label} fetched shifts'.format(
                            label=label
                        )
                    )
                except Exception as err:
                    logging.error(
                        ('{label} {exception} occured during shifts fetching: '
                        '{msg}').format(
                            label=label,
                            exception=type(err).__name__,
                            msg=err.__str__(),
                        )
                    )


def get_items(path, only=None):
    """Get paths to all entries in the data base.
    
    Parameters
    ----------
    path : str
        Path to data base.

    Returns
    -------
    list
        List of paths.

    """
    path = os.path.expanduser(path)
    ps = [os.path.join(path, n)
          for n in os.listdir(path)
          if not n.startswith('.') and len(n) == 4]
    ps = [p for p in ps if os.path.isdir(p)]
    if only is not None:
        ps = [p for p in ps if nmrex.utils.fname(p) in only]
    return ps


def _apply(func, total, index, path):
    with nmrex.utils.chdir(path):
        rcsb = nmrex.utils.fname(path)
        logging.info('applying <{func}> to {index}/{total} entry {rcsb}'
            .format(
                func=func.__name__,
                rcsb=rcsb,
                index=index,
                total=total,
            )
        )
        try:
            return func(rcsb)
        except Exception as err:
            logging.error(
                '{exception} occured: {msg}'.format(
                    exception=type(err).__name__,
                    msg=err.__str__(),
                )
            )
            return None


def apply(func, path, proc=1, only=None):
    """Apply a function to each entry in the data base.
    
    Parameters
    ----------
    func : callable
        Function to apply.
    path : str
        Path to data base,
    proc : int
        Number of processes to run application in. Default is 1. If less than
        1, `proc` is set to the number of cores.

    Returns
    -------
    list
        Results of application.

    """
    peps = get_items(path, only=only)
    total = len(peps)
    if proc < 1:
        proc = os.cpu_count()
    proc = min(total, proc)
    with mp.Pool(proc) as pool:
        return pool.starmap(partial(_apply, func, total), enumerate(peps, 1))