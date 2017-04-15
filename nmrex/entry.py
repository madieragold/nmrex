from Bio.PDB import PDBParser, PDBIO
import os
from nmrex.utils import fname


def structure(name='peptide'):
    parser = PDBParser()
    file = '{}.pdb'.format(name)
    return parser.get_structure(fname(os.getcwd()), file)


def header(name='peptide'):
    file = '{}.pdb'.format(name)
    file = open(file, 'r')
    lines = file.read()
    file.close()
    return lines[:lines.find('\nMODEL')] + '\n'


def save_structure(struct, name):
    file = '{}.pdb'.format(name)

    io = PDBIO()
    io.set_structure(struct)
    io.save(file)
    del io

    with open(file, 'r') as f:
        atoms = f.read()

    data = header() + atoms

    with open(file, 'w') as f:
        f.write(data)


