import os
import argparse
import logging
import nmrex


def predict(rcsb):
    inputs = [file for file in os.listdir()
              if not file.startswith('.') and file.endswith('.pdb')]
    for file in inputs:
        nmrex.predict.sparta(file, 'original')
        nmrex.predict.ppm_one(file)
        nmrex.predict.sparta_plus(file)


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()

    parser.add_argument('db', metavar='PATH', type=str,
                        help='path data base')

    args = parser.parse_args()

    nmrex.db.apply(predict, os.path.expanduser(args.db))


if __name__ == '__main__':
    main()