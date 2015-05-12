from setuptools import setup

setup(
    name="PyDkBio",
    packages=['PyDkBio'],
    version='0.1',
    description='Python scripts used in my biology/bioinformatics research',
    author='DV Klopfenstein',
    author_email='music_pupil@yahoo.com',
    scripts=['./PyDkBio/NCBI/cols.py'],
    license='BSD',
    url='http://github.com/dvklopfenstein/biocode',
    download_url='http://github.com/dvklopfenstein/biocode/tarball/0.1',
    keywords=['NCBI'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering :: Bio-Informatics']
    )
