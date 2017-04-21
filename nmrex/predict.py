import os
from nmrex.utils import mkdir


def sparta(pdb, db_postfix=None, path='~/tools/SPARTA/', silent=True):

    exe = os.path.join(os.path.expanduser(path), 'sparta')

    if db_postfix is None:
        db = 'tab/sparta.tab'
        output = os.path.join('prediction/sparta', pdb)
    else:
        db = 'tab/sparta_' + db_postfix + '.tab'
        output = os.path.join('prediction/sparta_' + db_postfix, pdb)

    db = os.path.join(os.path.expanduser(path), db)

    command = '{exe} -in {pdb} -db {db} -predDir "{output}"'.format(
        exe=exe,
        pdb=pdb,
        db=db,
        output=output,
    )
    if silent:
        command += ' &> /dev/null'

    mkdir(output)
    return os.system(command)


def ppm_one(pdb, path='~/tools/ppm_imac', silent=True):

    exe = os.path.join(os.path.expanduser(path), 'ppm_imac')

    command = '{exe} -pdb {pdb} -pre "prediction/ppm_one/{pdb}"'.format(
        exe=exe,
        pdb=pdb,
    )
    if silent:
        command += ' &> /dev/null'

    mkdir('prediction/ppm_one')
    rv = os.system(command)

    os.remove('bb_predict.dat')
    os.remove('cs_rmsd.dat')
    os.remove('proton_predict.dat')

    return rv


def sparta_plus(pdb, path='~/tools/SPARTA+', silent=True):

    exe = os.path.join(os.path.expanduser(path), 'SPARTA+.mac')
    output = os.path.join('prediction/sparta+', pdb)

    command = '{exe} -in {pdb} -spartaDir {path} -out "{output}"'.format(
        exe=exe,
        pdb=pdb,
        path=path,
        output=output,
    )
    if silent:
        command += ' &> /dev/null'

    mkdir('prediction/sparta+')
    rv = os.system(command)

    os.remove('struct.tab')

    return rv


PYTHON26 = '/System/Library/Frameworks/Python.framework/Versions/2.6/bin/'


def shiftx2(pdb, path='~/tools/SHIFTX2', silent=True, python26=PYTHON26):

    command = '''
    PREV=$PATH
    export PATH={python26}:$PATH
    python {script} -i {pdb} {silent}
    mv {pdb}.cs {output}
    export PATH=$PREV
    '''.format(
        script=os.path.join(os.path.expanduser(path), 'shiftx2.py'),
        pdb=pdb,
        output=os.path.join('prediction/shiftx2', pdb),
        python26=python26,
        silent='&> /dev/null' if silent else '',
    )

    mkdir('prediction/shiftx2')
    rv = os.system(command)

    return rv