from setuptools import setup
classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    ]

exec(open("goatools/version.py").read())
setup(
    name="PyDkBio",
    packages=['PyDkBio'],
    version='0.1',
    description='Python scripts used in my research',
    author='DV Klopfenstein',
    author_email='music_pupil@yahoo.com',
    scripts=['./PyDkBio/NCBI/cols.py']
    license='BSD',
    classifiers=classifiers,
    url='http://github.com/dvklopfenstein/biocode',
    download_url='http://github.com/dvklopfenstein/biocode/tarball/0.1',
    description="Python scripts to find enrichment of GO terms",
    keywords=['NCBI']
    )
