#!/usr/bin/env python

import sys
from random import randrange

from PyBiocode.UCSC.CytoBandDm6 import CytoBand

__author__ = "DV Klopfenstein"
__copyright__ = "Copyright (C) 2014-2015 DV Klopfenstein. All rights reserved."

O = CytoBand()

def test_1(prt=sys.stdout):
  """Test functions in the CytoBandHg38 class."""
  prt.write("\ntest_1\n")
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

def test_bp_to_cytomap(prt=sys.stdout):
  prt.write("\ntest_bp_to_cytomap\n")
  # Get the index of the 2nd to Last Chromosome
  iChr = O.num_chr - 2
  # Get the length of this chromosome
  L = O.get_len(iChr) 
  # Choose 10 bp numbers randomly less than the length of the Chromosome
  fmt = '{:>2} {:9} {:10}\n'
  prt.write('\nchr       bp cytomap\n')
  for i in range(10):
    bp = randrange(L)
    prt.write(fmt.format(O.get_sChr(iChr), bp, O.get_map_loc(iChr, bp)))
  # Choose a bp larger than the biggest bp for this chromosome
  bp_toobig = L + 10
  prt.write("\nif bp value({}) is larger than the max bp value({}) for the chr({}), return the max cytomap\n".format(
   bp_toobig, L, O.get_sChr(iChr)))
  prt.write(fmt.format(O.get_sChr(iChr), bp_toobig, O.get_map_loc(iChr, bp_toobig, True)))

def run_getCytobandRange(sChr, bp0, bp1, expected, prt=sys.stdout):
  cmap = O.getCytobandRange(sChr, bp0, bp1, ret_max=True) 
  prt.write('{CMAP} = getCytobandRange("{CHR}", {BP0}, {BP1}, ret_max=True)\n'.format(
    CMAP=cmap, CHR=sChr, BP0=bp0, BP1=bp1))
  assert cmap == expected

def test_getCytobandRange(prt=sys.stdout):
  run_getCytobandRange("2R",  1343403,  1443935, expected="2R")
  run_getCytobandRange("2R",  4671853,  4758048, expected="2R:41B3-41C1")
  run_getCytobandRange("2R", 22982542, 25139627, expected="2R:59C1-")
    
def run_all(prt=sys.stdout):
  test_1(prt)
  test_bp_to_cytomap(prt)
  test_getCytobandRange(prt)

if __name__ == '__main__':
  run_all()

# Copyright (C) 2014-2016 DV Klopfenstein. All rights reserved.
