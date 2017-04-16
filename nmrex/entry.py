import os
import io
import pandas as pd
import numpy as np
from Bio.PDB import PDBParser, PDBIO
from Bio.SeqUtils import seq1
import nmrstarlib
from nmrex.utils import fname


def structure(name='peptide'):
    parser = PDBParser()
    file = '{}.pdb'.format(name)
    return parser.get_structure(fname(os.getcwd()), file)


def header(name='peptide'):
    """
    
    Parameters
    ----------
    name

    Returns
    -------

    """

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


def to_letter(df, col):
    df[col] = df[col].map(seq1)
    return df


def star2():

    cs = next(nmrstarlib.nmrstarlib.read_files('star2.str')) \
        .chem_shifts_by_residue(nmrstar_version='2')

    assert 0 < len(cs)
    assert len(cs) < 2

    df = pd.DataFrame.from_dict(cs[0], orient='index')

    dtypes = {c: float for c in df.columns}
    dtypes['AA3Code'] = str
    dtypes['Seq_ID'] = int

    to_letter(df, 'AA3Code')
    df = df.astype(dtypes)
    df.rename(columns={'AA3Code': 'RESNAME', 'Seq_ID': 'RESID'}, inplace=True)
    df.sort_values('RESID', inplace=True)
    df.set_index(['RESID', 'RESNAME'], inplace=True)

    return df


def sparta(name='peptide', db_postfix=None):

    if db_postfix is None:
        fpath = 'prediction/sparta'
    else:
        fpath = 'prediction/sparta_' + db_postfix
    fpath = os.path.join(fpath, name + '.pdb', 'pred.tab')

    with open(fpath, 'r') as f:
        ss = filter(lambda s: not (
                    s.startswith('REMARK') or
                    s.startswith('DATA') or
                    s.startswith('VARS') or
                    s.startswith('FORMAT')
        ), f)
        ss = io.StringIO(''.join(list(ss)))

    tox = pd.read_table(ss, delim_whitespace=True, header=None,
                        names=['RESID' ,'RESNAME', 'ATOMNAME', 'SS_SHIFT' ,
                               'SHIFT', 'RC_SHIFT' ,'HM_SHIFT', 'SIGMA',
                               'SOURCE'])

    tox['RESNAME'] = tox['RESNAME'].map(lambda s: s.upper())
    tox = tox.groupby(['RESID', 'RESNAME']) \
        .apply(
            lambda df: pd.DataFrame(data=df['SHIFT'].values[np.newaxis, :],
                                    columns=df['ATOMNAME'])) \
        .reset_index() \
        .drop('level_2', axis=1)
    tox.set_index(['RESID', 'RESNAME'], inplace=True)

    return tox


def ppm_one(name='peptide'):
    fpath = os.path.join('prediction/ppm_one', name + '.pdb')

    with open(fpath, 'r') as f:

        df = [l.lstrip() for l in f if l.startswith('    ')]
        df = [l for l in df if l[0].isdigit()]

        df = pd.read_table(
            io.StringIO(''.join(df)),
            delim_whitespace=True,
            usecols = [1,2,3,5],
            names=['RESID','RESNAME','ATOMNAME','SHIFT']
        )

        to_letter(df, 'RESNAME')
        df = df.groupby(['RESID', 'RESNAME']) \
            .apply(
                lambda df: pd.DataFrame(data=df['SHIFT'].values[np.newaxis, :],
                                        columns=df['ATOMNAME'])) \
            .reset_index() \
            .drop('level_2', axis=1)
        df.set_index(['RESID', 'RESNAME'], inplace=True)

        return df
