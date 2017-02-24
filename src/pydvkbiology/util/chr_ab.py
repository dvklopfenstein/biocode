"""Manages chromosome name, start bp, stop bp with different sources."""

__author__  = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2014-2016 DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import collections as cx
import numpy as np

class ChrAB(object):
  """Class to hold the chromosome name, and the start and end base pair values."""
  # Uses convention that rev. strand start_bp > stop_bp
  # so that this class may be used without an orientation arg.

  fwd = ['+', 'plus']
  rev = ['-', 'minus']
  typ = cx.namedtuple("ChrAB", "chr start_bp stop_bp fwd_strand ichr")

  def __init__(self, schr, start_bp, stop_bp=None, **kws):
    """Initialize data members."""
    # Data members
    self.schr = schr
    self.start_bp = start_bp if isinstance(start_bp, int) else None
    self.stop_bp = self._init_stop_bp(stop_bp)
    # Key-word args(4): name, ichr, orgn, orientation, N-based
    self._init_ichr(**kws) # kws: Either of: ichr orgn
    self.name = kws['name'] if 'name' in kws else None
    if 'orientation' in kws:
      self._init_orientation(kws['orientation'])

  def _init_stop_bp(self, stop_bp):
    """Initialize stop_bp."""
    if stop_bp is None: # Length of 1
      return self.start_bp
    if isinstance(stop_bp, int):
      return stop_bp

  def _init_ichr(self, **kws):
    """Initialize ichr if ichr or orgn is provided, otherwise ichr=None."""
    ichr = kws.get('ichr', None)
    if 'orgn' in kws:
      orgn_ichr = kws.get('orgn').get_iChr(self.schr)
      if ichr is not None: 
        assert ichr == orgn_ichr
      ichr = orgn_ichr
    self.ichr = ichr
 
  def _init_orientation(self, orientation):
    """Use orientation to set start and stop."""
    # Set:  Fwd: Start < Stop;   Rev: Start > Stop.
    # Use orientation if available (Forward/Reverse) strand.
    if orientation in ChrAB.rev:
      # biocode uses convention that rev. strand start_bp > stop_bp
      if self.start_bp < self.stop_bp:
        self.start_bp, self.stop_bp = self.stop_bp, self.start_bp
    elif orientation in ChrAB.fwd:
      pass
    # An expected orientation is only relevant if there are both start_bp and stop_bp
    elif self.start_bp is not None and self.stop_bp is not None:
      raise Exception("UNKNOWN ORIENTATION({})".format(orientation))

  # 1-based:     1 2 3 4 5 6 7 8 9    CAGC => 2-5  len = 4 = 5 - 2 + 1
  #              A C A G C T A C A G
  #                -------
  # 0-based:     0 1 2 3 4 5 6 7 8 9  CAGC => 1-5  len = 4 = 5 - 1
  # This class:  0 1 2 3 4 5 6 7 8 9  CAGC => 1-4  len = 4 = 4 - 1 + 1
  def get_start_stop_0based(self):
    """Return coordinates in 0-based format."""
    if self.is_fwd(): 
      return self.start_bp, self.stop_bp+1
    raise Exception("TIME TO IMPLEMENT FOR REV: get_start_stop_0based()")
    
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
  # Note: get_rng returns expanded plotXs

  def get_len(self):
    return abs(self.stop_bp - self.start_bp) + 1

  def has_abs(self):
    return self.start_bp is not None and self.stop_bp is not None

  def get_dist(self, rhs_chrab):
    """Return intergenic distance between two genes. Return 0 if overlapping or 'kissing'."""
    if self.has_same_chr(rhs_chrab):
      # Put gene coords in list and sort genes by smallest coord. eg [[0, 5], [6, 10]]
      if self.has_abs() and rhs_chrab.has_abs():
        genes_ab = sorted([self.get_plotXs(), rhs_chrab.get_plotXs()], key=lambda t: t[0])
        if genes_ab[0][1] < genes_ab[1][0]: # Not 'kissing'
          return genes_ab[1][0] - genes_ab[0][1]
        return 0 
    return None # genes are on separate chromosomes or lack bp values

  def get_overlap_cab(self, rhs_chrab):
    """Return cab representing overlap of chr_a and chr_b. None if no overlap."""
    if self.has_same_chr(rhs_chrab):
      # If start_bp and stop_bp exist for both input cabs
      if self.has_abs() and rhs_chrab.has_abs():
        # Put gene coords in list and sort genes by smallest coord. eg [[0, 5], [4, 10]]
        genes_ab = sorted([self.get_plotXs(), rhs_chrab.get_plotXs()], key=lambda t: t[0])
        if genes_ab[0][1] >= genes_ab[1][0]: # If there is an overlap
          start_bp = genes_ab[1][0] 
          stop_bp = min(genes_ab[0][1], genes_ab[1][1])
          assert start_bp <= stop_bp, "START({}) STOP({})".format(start_bp, stop_bp)
          return ChrAB(self.schr, start_bp, stop_bp)
    return None # genes are on separate chromosomes or lack bp values

  def overlaps_cab(self, rhs_chrab):
    """Return True if rhs_chrab overlaps self. None if no overlap."""
    if self.has_same_chr(rhs_chrab):
      # If start_bp and stop_bp exist for both input cabs
      if self.has_abs() and rhs_chrab.has_abs():
        # Put gene coords in list and sort genes by smallest coord. eg [[0, 5], [4, 10]]
        genes_ab = sorted([self.get_plotXs(), rhs_chrab.get_plotXs()], key=lambda t: t[0])
        return genes_ab[0][1] >= genes_ab[1][0] # True if there is an overlap
    return False # genes are on separate chromosomes or lack bp values

  def overlaps_cabs(self, cabs):
    for cab in cabs:
      if self.overlaps_cab(cab):
        return True
    return False

  def has_same_chr(self, rhs_chrab):
    """Return True if rhs_chrab is on the same chr as self."""
    if self.ichr is not None and rhs_chrab.ichr is not None:
      return self.ichr == rhs_chrab.ichr
    if rhs_chrab is not None: 
      return self.schr == rhs_chrab.schr
    return False

  def get_rand_loc(self, rng_len):
    """Returns a random start location for a range length within this ChrAB."""
    assert rng_len > 0
    self_len = self.get_len()
    b0, bN = self.get_plotXs()
    if rng_len < self_len:
      return np.random.randint(b0, bN - rng_len + 1)
    elif self_len == rng_len:
      return b0
    return None

  def get_rand_cab(self, rng_len):
    """Return a new cab from an area randomly chosen from inside this cab."""
    start_bp = self.get_rand_loc(rng_len)
    if start_bp is not None:
      return ChrAB(self.schr, start_bp, start_bp + rng_len - 1, 
        ichr=self.ichr, name=self.name)

  def minus_cab(self, cab):
    """Subtract cab from self. Return remaining cab(s)."""
    cab_overlap = self.get_overlap_cab(cab)
    kwargs = {'ichr':self.ichr, 'name':self.name}
    b0, bN = self.get_plotXs()
    if cab_overlap is None:
      # self       ==========            ==========       
      # cab    --  .        .            ==========       
      # cab        .        . --         ==========       
      return [ChrAB(self.schr, b0, bN, **kwargs)]
    o0, oN = cab_overlap.start_bp, cab_overlap.stop_bp
    if b0 == o0 and bN == oN:
      # self       ==========            ==========       
      # cab        ----------            None
      # cab     ---------------          None
      return None
    if o0 == b0:
      # self       ==========            ==========       
      # cab     -------     .                ======       
      # cab        -------  .                   ===       
      return [ChrAB(self.schr, oN+1, bN, **kwargs)]
    if cab_overlap.stop_bp == bN:
      # self       ==========            ==========       
      # cab4       .  -------            ===              
      # cab5       .     -------         ======           
      return [ChrAB(self.schr, b0, o0-1, **kwargs)]
    # self       ==========            ==========       
    # cab        . -------.            ==       =       
    # cab        . ----   .            ==    ====
    assert b0 < o0 and oN < bN
    return [ChrAB(self.schr, b0, o0-1, **kwargs), ChrAB(self.schr, oN+1, bN, **kwargs)]

  def get_rng(self, margin_lhs=0, margin_rhs=None):
    """Return an expanded range: Expand orignal from left, right, or both."""
    # return e.g.: [31425567, 31728336]
    if margin_lhs is None:
      margin_lhs = 0
    x0, xN = self.get_plotXs()
    if margin_lhs == 0 and margin_rhs is None:
        return x0, xN
    rng0 = x0 - margin_lhs
    if rng0 < 0: # rng0 minimum value is 0
      rng0 = 0
    rngN = xN + (margin_lhs if margin_rhs is None else margin_rhs)
    return [rng0, rngN]

  def get_ChrAB_rng(self, margin_lhs=0, margin_rhs=None):
    """Create ChrAB w/expanded range: Expand orignal from left, right, or both."""
    # return e.g.: ChrAB("6", 31425567, 31728336)
    x0, xN = self.get_rng(margin_lhs, margin_rhs)
    return ChrAB(self.schr, x0, xN, ichr=self.ichr)

  def get_min_bp(self):
    """Returns the smallest base pair value."""
    if self.valid_start_stop():
      return min(self.start_bp, self.stop_bp)
    return None

  def get_ichr(self, orgn=None):
    """Gets chromosome index if it is available. If not, sets it in this object, then returns it."""
    if self.ichr is not None:
      return self.ichr
    self.ichr = orgn.get_iChr(self.schr)
    return self.ichr

  @staticmethod
  def rng_g_cabs(cab_lst):
    """Given a list of ChrABs, give the min bp and maxbp."""
    bps = set()
    for cab in cab_lst:
      bps |= set([cab.start_bp, cab.stop_bp])
    return min(bps), max(bps)

  @staticmethod
  def get_aart_len(win_start, win_end, bpsPchar=20000):
    """Returns the number of characters in an ASCII Art line."""
    return int(float(win_end-win_start)/bpsPchar)+1

  def get_aart_line(self, win_start, win_end, bpsPchar=20000):
    """Get an ASCII Art line representing a gene in a region."""
    gene_start, gene_end = self.get_plotXs()
    totPts = self.get_aart_len(win_start, win_end, bpsPchar)
    picStr = list(' '*(totPts))
    # Find gene start and end points relative to the print window
    loc_start = int(float(gene_start - win_start)/bpsPchar)
    loc_end   = int(float(gene_end   - win_start)/bpsPchar)
    picStr[-1] = '.' # Note the end of the window
    picStrL = len(picStr) 
    IDX_RNG = range(loc_start,loc_end+1) if loc_start <= loc_end else range(loc_end, loc_start+1)
    for i in IDX_RNG:
      # If this part of the gene is in the print window, print 'G' for 'gene in this spot'
      gene_pm = self.is_fwd()
      if i>=0 and i<picStrL:
        if gene_pm is True:
          picStr[i] = '>'
        elif gene_pm is False:
          picStr[i] = '<'
        else:
          picStr[i] = 'G'
        #if i==totPts: 
        #  picStr[totPts] = 'g' # Print 'g' instead of '.'
    return ''.join(picStr)

  def __hash__(self):
    return hash(self.__key())

  def __key(self):
    return (self.ichr, self.schr, self.start_bp, self.stop_bp, self.name)

  def __eq__(self, rhs):
    if rhs is not None:
      bp_eq = self.start_bp == rhs.start_bp and self.stop_bp == rhs.stop_bp
      if self.ichr is not None and rhs.ichr is not None:
        return self.ichr == rhs.ichr and bp_eq
      return self.schr == rhs.schr and bp_eq
    return False

  def __ne__(self, rhs):
    return not self.__eq__(rhs)

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
    
  def __str__(self):
    txt = []
    bp1 = self.start_bp == self.stop_bp
    if not bp1:
      txt.append("({})".format("+" if self.stop_bp > self.start_bp else "-"))
    if 'chr' not in self.schr.lower():
      txt.append("chr")
    txt.append("{SCHR:<2} {START:>9}".format(SCHR=self.schr, START=self.start_bp))
    if bp1:
      return ''.join(txt)
    txt.append(" {STOP:>9}".format(STOP=self.stop_bp))
    return ''.join(txt)

  def __repr__(self):
    ret = ['ChrAB("{schr}", {start_bp}'.format(schr=self.schr, start_bp=self.start_bp)]
    if self.start_bp != self.stop_bp:
      ret.append(', {stop_bp}'.format(stop_bp=self.stop_bp))
    if self.name is not None:
      ret.append(", name={NAME}".format(NAME=self.name))
    if self.ichr is not None:
      ret.append(", ichr={ICHR}".format(ICHR=self.ichr))
    ret.append(")")
    return ''.join(ret)
    #, orientation=None, orgn=None, name=None):

# Copyright (C) 2014-2016 DV Klopfenstein. All rights reserved.
