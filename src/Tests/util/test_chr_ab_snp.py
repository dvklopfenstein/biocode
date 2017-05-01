#!/usr/bin/env python
"""Test creation of SNPs."""

__copyright__ = "Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'
__license__ = "GPL"

import sys
from pydvkbiology.util.chr_ab import ChrAB

def test_get_rng(prt=sys.stdout):
  """Various tests for creating a ChrAB which contains a SNP."""
  #pylint: disable=bad-whitespace
  snps = [
      # Input                             Expected
      # SNP                                 is_fwd
      # ---------------------------------   ------
      (ChrAB("1", 0, None)                , True ),
      (ChrAB("1", None, 0)                , False),
      (ChrAB("1", 10, None)               , True ),
      (ChrAB("1", None, 20)               , False),
      (ChrAB("1", 10, 10)                 , None ),
      (ChrAB("1", 10, 10, orientation='+'), True ),
      (ChrAB("1", 10, 10, orientation='-'), False),
      (ChrAB("1", 10, orientation='+')    , True ),
      (ChrAB("1", 10, orientation='-')    , False),
      (ChrAB("1", 0, 0, orientation='+')  , True ),
      (ChrAB("1", 0, 0, orientation='-')  , False),
      (ChrAB("1", 0, orientation='+')     , True ),
      (ChrAB("1", 0, orientation='-')     , False),
  ]
  for snp, exp_isfwd in snps:
    prt.write("snp({SNP}) len({LEN}) is_fwd({FWD})\n".format(
        SNP=snp, LEN=snp.get_len(), FWD=snp.is_fwd()))
    assert snp.get_len() == 1
    assert snp.is_fwd() is exp_isfwd, "FWD: actual({A}) expected({E}) ({CAB})".format(
        A=snp.is_fwd(), E=exp_isfwd, CAB=snp)

if __name__ == '__main__':
  test_get_rng()

# Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved.
