#!/usr/bin/env python
"""Test creation of SNPs."""

__copyright__ = "Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'
__license__ = "GPL"

import sys
import collections as cx
from pydvkbiology.util.chr_ab import ChrAB

def test_get_rng(prt=sys.stdout):
  """Various tests for creating a ChrAB which contains a SNP."""
  #pylint: disable=bad-whitespace
  ntobj = cx.namedtuple("NtSnp", "cab exp_isfwd exp_bp")
  test_data = [#                                          Expected
      # Input                                                 max_bp
      # SNP                                            is_fwd min_bp
      # ---------------------------------              ------ ------
      ntobj._make((ChrAB("1", 0, None)                , True ,    0,)),
      ntobj._make((ChrAB("1", None, 0)                , False,    0,)),
      ntobj._make((ChrAB("1", 10, None)               , True ,   10,)),
      ntobj._make((ChrAB("1", None, 20)               , False,   20,)),
      ntobj._make((ChrAB("1", 10, 10)                 , None ,   10,)),
      ntobj._make((ChrAB("1", 10, 10, orientation='+'), True ,   10,)),
      ntobj._make((ChrAB("1", 10, 10, orientation='-'), False,   10,)),
      ntobj._make((ChrAB("1", 10, orientation='+')    , True ,   10,)),
      ntobj._make((ChrAB("1", 10, orientation='-')    , False,   10,)),
      ntobj._make((ChrAB("1", 0, 0, orientation='+')  , True ,    0,)),
      ntobj._make((ChrAB("1", 0, 0, orientation='-')  , False,    0,)),
      ntobj._make((ChrAB("1", 0, orientation='+')     , True ,    0,)),
      ntobj._make((ChrAB("1", 0, orientation='-')     , False,    0,)),
  ]
  for ntd in test_data:
    cab = ntd.cab
    prt.write("snp({SNP}) len({LEN}) is_fwd({FWD})\n".format(
        SNP=cab, LEN=cab.get_len(), FWD=cab.is_fwd()))
    assert cab.get_len() == 1
    assert cab.is_fwd() is ntd.exp_isfwd, "EXP({}) {}".format(cab.is_fwd(), ntd)
    assert cab.get_min_bp() == ntd.exp_bp, "EXP({}) {}".format(cab.get_min_bp(), ntd)
    assert cab.get_max_bp() == ntd.exp_bp, "EXP({}) {}".format(cab.get_max_bp(), ntd)

if __name__ == '__main__':
  test_get_rng()

# Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved.
