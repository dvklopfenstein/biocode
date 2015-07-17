"""Initialize the util subpackage of the pydvkbiology package.

This sub-package is used with data downloaded from UCSC.
"""

from pkg_resources import get_distribution, DistributionNotFound

__project__ = 'pydvkbiology'
__version__ = None # required for initial installation

try:
  __version__ = get_distribution('pydvkbiology').version
except DistributionNotFound:
  VERSION = __project__ + '-' + '(local)'
else:
  VERSION = __project__ + '-' + __version__

