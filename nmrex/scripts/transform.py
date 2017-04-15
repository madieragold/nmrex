import os
import argparse
import logging
import nmrex
import numpy as np
import copy


def transform(rcsb):
    structure = nmrex.entry.structure()

    # save separate models
    for model in structure.child_list:
        new = copy.deepcopy(structure)
        new.child_list = [model]
        nmrex.entry.save_structure(new, 'model{}'.format(model.get_id()))

    # save mean and median atom coordinates
    coord = np.array([
         np.array([atom.coord for atom in model.get_atoms()])
         for model in structure.child_list
         ])

    n_models, n_atoms, _ = coord.shape

    mean = coord.mean(axis=0)
    median = np.median(coord, 0)

    new = copy.deepcopy(structure)
    new.child_list = [new.child_list[0]]
    it = new.child_list[0].get_atoms()
    for i in range(n_atoms):
        atom = next(it)
        atom.coord = mean[i]
        nmrex.entry.save_structure(new, 'mean')

    new = copy.deepcopy(structure)
    new.child_list = [new.child_list[0]]
    it = new.child_list[0].get_atoms()
    for i in range(n_atoms):
        atom = next(it)
        atom.coord = median[i]
        nmrex.entry.save_structure(new, 'median')


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()

    parser.add_argument('db', metavar='PATH', type=str,
                        help='path to data base')

    parser.add_argument('-p', metavar='N', type=int, dest='proc', default=1,
                        help='number of processes')

    args = parser.parse_args()

    nmrex.db.apply(transform, os.path.expanduser(args.db), proc=args.proc)


if __name__ == '__main__':
    main()