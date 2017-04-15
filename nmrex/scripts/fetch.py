import os
import pandas as pd
import argparse
import logging
import nmrex


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()

    parser.add_argument('csv', metavar='CSV', type=str,
                        help='path to list with RCSB and BMRB IDs')

    parser.add_argument('--db', metavar='DIR', type=str, dest='db',
                        help='directory to store fetched data', default='')

    args = parser.parse_args()

    df = pd.read_csv(os.path.expanduser(args.csv), dtype=str)
    nmrex.db.fetch(os.path.expanduser(args.db), df)


if __name__ == '__main__':
    main()