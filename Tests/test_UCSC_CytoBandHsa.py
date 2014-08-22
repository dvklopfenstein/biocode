#!/usr/bin/env python

import unittest
import sys

from PyBiocode.UCSC.CytoBandHsa import *


class CytoBandHsa_Tests(unittest.TestCase):

  def test_1(self):
    """Use all the functions in the CytoBandHsa class."""
    O = CytoBand()
    L = O.get_len_genome()
    sys.stdout.write("   {:>12}=L summed over all chromosomes in the genome\n".format(L))
    for iChr in range(O.num_chr):
      sys.stdout.write('{:>2} {:>2} {:9}=L centromere({:7}=L {:9}=start {:9}=end)\n'.format(
        iChr,
        O.get_sChr(iChr),
        O.get_len(iChr),
        O.cen_get_len(iChr),
        O.cen_get_start(iChr),
        O.cen_get_end(iChr)))


if __name__ == '__main__':
  unittest.main()

