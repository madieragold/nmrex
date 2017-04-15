import logging
import nmrex
import os


def fetch(path, df):
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


def get_items(path):
    path = os.path.expanduser(path)
    ps = [os.path.join(path, n)
          for n in os.listdir(path)
          if not n.startswith('.') and len(n) == 4]
    return [p for p in ps if os.path.isdir(p)]


def apply(func, path):
    peps = get_items(path)
    total = len(peps)
    for index, peppath in enumerate(peps, 1):
        with nmrex.utils.chdir(peppath):
            rcsb = nmrex.utils.fname(peppath)
            logging.info('applying <{func}> to {index}/{total} entry {rcsb}'
                .format(
                    func=func.__name__,
                    rcsb=rcsb,
                    index=index,
                    total=total,
                )
            )
            try:
                func(rcsb)
            except Exception as err:
                logging.error(
                    '{exception} occured: {msg}'.format(
                        exception=type(err).__name__,
                        msg=err.__str__(),
                    )
                )