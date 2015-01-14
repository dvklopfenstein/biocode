"""Initialize the GENCODE subpackage of the PyDkBio package.

This sub-package is used with data downloaded from GENCODE:
  ftp://ftp.sanger.ac.uk/pub/gencode/_README.TXT
  ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_21/

"""

from pkg_resources import get_distribution, DistributionNotFound

__project__ = 'PyDkBio'
__version__ = None # required for initial installation

try:
  __version__ = get_distribution('PyDkBio').version
except DistributionNotFound:
  VERSION = __project__ + '-' + '(local)'
else:
  VERSION = __project__ + '-' + __version__

