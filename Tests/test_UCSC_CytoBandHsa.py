#!/usr/bin/env python

import unittest
import sys
from random import randrange

from PyBiocode.UCSC.CytoBandHsa import *

__author__ = "DV Klopfenstein"

O = CytoBand()

class CytoBandHsa_Tests(unittest.TestCase):

  def test_1(self):
    """Use all the functions in the CytoBandHsa class."""
    O = CytoBand()
    L = O.get_len_genome()
    sys.stdout.write("   {:>12}=L summed over all chromosomes in the genome\n".format(L))
    for iChr in range(O.num_chr):
      chrL = O.get_len(iChr)
      assert( chrL == O.get_max_bp(iChr) )
      sys.stdout.write('{:>2} {:>2} {:9}=L centromere({:7}=L {:9}=start {:9}=end)\n'.format(
        iChr,
        O.get_sChr(iChr),
        chrL,
        O.cen_get_len(iChr),
        O.cen_get_start(iChr),
        O.cen_get_end(iChr)))

  def test_bp_to_cytomap(self):
    # Get the index of the 2nd to Last Chromosome
    iChr = O.num_chr - 2
    # Get the length of this chromosome
    L = O.get_len(iChr) 
    # Choose 10 bp numbers randomly less than the length of the Chromosome
    sys.stdout.write('\nchr       bp cytomap\n')
    for i in range(10):
      bp = randrange(L)
      self.prt_bp_map(sys.stdout, iChr, bp, O.get_map_loc(iChr, bp))
    # Choose a bp larger than the biggest bp for this chromosome
    self.prt_bp_map(sys.stdout, iChr, L, O.get_map_loc(iChr, L+10))
    
  def prt_bp_map(self, PRT, iChr, bp, cmap):
    PRT.write('{:>2} {:9} {:10}\n'.format(
      O.get_sChr(iChr), bp, O.get_map_loc(iChr, bp)))


if __name__ == '__main__':
  unittest.main()

