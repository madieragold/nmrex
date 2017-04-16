from Bio.PDB import PDBParser, PDBIO
import os
from nmrex.utils import fname


def structure(name='peptide'):
    parser = PDBParser()
    file = '{}.pdb'.format(name)
    return parser.get_structure(fname(os.getcwd()), file)


def header(name='peptide'):

    with open('{}.pdb'.format(name), 'r') as f:
        file = f.read()

    model = file.find('\nMODEL')
    atom = file.find('\nATOM')

    if atom < 0:
        raise ValueError('no ATOM entries found in PDB')
    if model < 0:
        index = atom
    else:
        index = min(model, atom)

    return file[:index] + '\n'


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


