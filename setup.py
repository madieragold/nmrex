from distutils.core import setup


setup(
    name='nmrex',
    version='1.0.0',
    description='Exploratory data science for NMR and structural biology',
    author='Leonid Vlasenkov MIPT & IBCh',
    url='https://github.com/vlasenkov/nmrex',
    license='MIT',
    packages=['nmrex'],
    install_requires=[
        'numpy',
        'pandas>=0.19',
        'biopython>=1.68',
        'nmrstarlib>=1.1.0',
        'lxml>=3.7.3',
    ],
    entry_points={
        'console_scripts': [
            'nmrex.fetch = nmrex.scripts.fetch:main',
            'nmrex.predict = nmrex.scripts.predict:main',
            'nmrex.transform = nmrex.scripts.transform:main',
        ],
    },
)
