"""Manages chromosome name, start bp, stop bp with different sources."""

import collections as cx

class ChrAB(object):
  """Class to hold the chromosome name, and the start and end base pair values."""
  # Uses convention that rev. strand start_bp > stop_bp
  # so that this class may be used without an orientation arg.

  fwd = ['plus']
  rev = ['minus']
  typ = cx.namedtuple("ChrAB", "chr start_bp stop_bp fwd_strand ichr")

  def __init__(self, schr, start_bp, stop_bp, orientation=None, orgn=None, name=None):
    """Initialize data members."""
    self.name = name
    self.schr = schr
    self.ichr = None
    self.start_bp = start_bp if isinstance(start_bp, int) else None
    self.stop_bp = stop_bp if isinstance(stop_bp, int) else None
    self._init(orientation, orgn)

  def _init(self, orientation, orgn):
    """Set:  Fwd: Start < Stop;   Rev: Start > Stop."""
    # Use orientation if available (Forward/Reverse) strand.
    if orientation is not None:
      self._init_orientation(orientation)
    if orgn is not None:
      self.ichr = orgn.get_iChr(self.schr)

  def _init_orientation(self, orientation):
    """Use orientation to set start and stop."""
    if orientation in ChrAB.rev:
      # biocode uses convention that rev. strand start_bp > stop_bp
      if self.start_bp < self.stop_bp:
        self.start_bp, self.stop_bp = self.stop_bp, self.start_bp
    elif orientation in ChrAB.fwd:
      pass
    else:
      raise Exception("UNKNOWN ORIENTATION({})".format(orientation))

  def is_fwd(self):
    """Return True if this is forward-stranded data."""
    if self.valid_start_stop():
      return self.start_bp < self.stop_bp
    return None

  def in_range(self, rng_start_bp, rng_stop_bp):
    """Determine if gene is in the range(start_rng, stop_rng)."""
    if self.start_bp is not None and self.stop_bp is not None:
      return self._in_range(rng_start_bp, rng_stop_bp)
    else:
      return None

  def _in_range(self, rng_start_bp, rng_stop_bp):
    """Determine if gene is in the range(start_rng, stop_rng)."""
    if self.start_bp <= self.stop_bp: # plus orientation
      if self.stop_bp < rng_start_bp or self.start_bp > rng_stop_bp:
        return False
    else: # minus orientation
      if self.start_bp < rng_start_bp or  self.stop_bp > rng_stop_bp:
        return False
    return True

  def is_start_stop(self):
    """return start and stop bp."""
    return self.schr is not None and self.start_bp is not None and self.stop_bp is not None

  def get_start_stop(self):
    if self.is_start_stop():
      # ChrAB: chr start_bp stop_bp fwd_strand ichr
      return ChrAB.typ([self.schr, self.start_bp, self.stop_bp, self.ichr])
    else:
      return None

  def valid_start_stop(self):
    return self.start_bp is not None and self.stop_bp is not None

  def get_plotXs(self):
    """Returns start_bp and stop_bp such that startbp < stop_bp, no matter the gene orientation."""
    if self.valid_start_stop():
      return sorted([self.start_bp, self.stop_bp])
    return None

  def get_dist(self, rhs_chrab):
    """Return intergenic distance between two genes. Return 0 if overlapping or 'kissing'."""
    if self.schr == rhs_chrab.schr:
      # Put gene coords in list and sort genes by smallest coord. eg [[0, 5], [6, 10]]
      genes_ab = sorted([self.get_plotXs(), rhs_chrab.get_plotXs()], key=lambda t: t[0])
      if genes_ab[0][1] < genes_ab[1][0]: # Not 'kissing'
        return genes_ab[1][0] - genes_ab[0][1]
      #if genes_ab[0][1] != genes_ab[1][0]: # Not 'kissing'
        #coords = sorted(set(genes_ab[0] + genes_ab[1])) # List of ALL coords, e.g. each genes a & b
        #L = len(coords)
        #if L == 4 and coords[1] == genes_ab[0][1]: # Separated
        #  return coords[2] - coords[1] # GGGG<---->GGGG
        #elif L == 2 and coords[0] == genes_ab[0][1] and coords[1] == genes_ab[1][0]:
        #  return coords[1] - coords[0] # G<---->G
        #elif L == 3:
        #  if coords[0] == genes_ab[0][1] and coords[1] == genes_ab[1][0]:
        #    return coords[1] - coords[0] # G<---->GGGGGG
        #  elif coords[1] == genes_ab[0][1] and coords[2] == genes_ab[1][1]:
        #    return coords[2] - coords[1] # GGGGGG<---->G
      # No intergenic distance between these 2 DNA items:
      #   1. Genes are on top off each other or 'kissing'
      #   2. Genes have no distance between them
      #   3. Genes may be overlapping: coords[1] == genes_ab[1][0]
      return 0 
    return None # genes are on separate chromosomes

  def get_min_bp(self):
    """Returns the smallest base pair value."""
    if self.valid_start_stop():
      return min(self.start_bp, self.stop_bp)
    return None

  def __eq__(self, rhs):
    bp_eq = self.start_bp == rhs.start_bp and self.stop_bp == rhs.stop_bp
    if self.ichr is not None and rhs.ichr is not None: 
      return self.ichr == rhs.ichr and bp_eq
    return self.schr == rhs.schr and bp_eq

  def __lt__(self, rhs):
    if self.ichr is not None and rhs.ichr is not None: 
      if self.ichr < rhs.ichr:
        return True
      elif self.ichr > rhs.ichr:
        return False
      else:
        return self._lt_bps(rhs)
    else:
      if self.schr < rhs.schr:
        return True
      elif self.schr > rhs.schr:
        return False
      else:
        return self._lt_bps(rhs)

  def _lt_bps(self, rhs):
    # TBD: Use PlotXs?
    if self.start_bp < rhs.start_bp:
      return True
    elif self.start_bp > rhs.start_bp:
      return False
    else:
      if self.stop_bp < rhs.stop_bp:
        return True
      elif self.stop_bp > rhs.stop_bp:
        return False
      else:
        return False
    
