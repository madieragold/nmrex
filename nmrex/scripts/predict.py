import os
import argparse
import logging
import nmrex


shiftx2 = False


def predict(rcsb):
    inputs = [file for file in os.listdir()
              if not file.startswith('.') and file.endswith('.pdb')]
    for file in inputs:
        nmrex.predict.sparta(file, 'original')
        nmrex.predict.ppm_one(file)
        nmrex.predict.sparta_plus(file)
        if shiftx2:
            nmrex.predict.shiftx2(file)


def main():
    global shiftx2

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()

    parser.add_argument('db', metavar='PATH', type=str,
                        help='path to data base')

    parser.add_argument('-p', metavar='N', type=int, dest='proc', default=1,
                        help='number of processes')

    parser.add_argument('--shiftx2', action='store_true',
                        help='run shiftx2 predictions', dest='shiftx2')

    args = parser.parse_args()
    shiftx2 = args.shiftx2
    if shiftx2:
        proc = 1
    else:
        proc = args.proc

    nmrex.db.apply(predict, os.path.expanduser(args.db), proc=proc)


if __name__ == '__main__':
    main()