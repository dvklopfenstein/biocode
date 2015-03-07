#!/usr/bin/env python

import unittest
import sys
from random import randrange

from PyBiocode.UCSC.CytoBandHg38 import *

__author__ = "DV Klopfenstein"
# Copyright (C) 2014-2015 DV Klopfenstein. All rights reserved.

O = CytoBand()

class CytoBandHsa_Tests(unittest.TestCase):

  def test_1(self):
    """Test functions in the CytoBandHsa class."""
    print "\ntest_1"
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

  def test_bp_to_cytomap(self, PRT=sys.stdout):
    print "\ntest_bp_to_cytomap"
    # Get the index of the 2nd to Last Chromosome
    iChr = O.num_chr - 2
    # Get the length of this chromosome
    L = O.get_len(iChr) 
    # Choose 10 bp numbers randomly less than the length of the Chromosome
    fmt = '{:>2} {:9} {:10}\n'
    PRT.write('\nchr       bp cytomap\n')
    for i in range(10):
      bp = randrange(L)
      PRT.write(fmt.format(O.get_sChr(iChr), bp, O.get_map_loc(iChr, bp)))
    # Choose a bp larger than the biggest bp for this chromosome
    bp_toobig = L + 10
    print "\nif bp value({}) is larger than the max bp value({}) for the chr({}), return the max cytomap".format(
     bp_toobig, L, O.get_sChr(iChr))
    PRT.write(fmt.format(O.get_sChr(iChr), bp_toobig, O.get_map_loc(iChr, bp_toobig, True)))
    


if __name__ == '__main__':
  unittest.main()

