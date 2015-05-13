"""Initialize the matplotlib subpackage of the PyDkBio package.

This sub-package can be helpful when using color maps in matplotlib.
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

