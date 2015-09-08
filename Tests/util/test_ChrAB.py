#!/usr/bin/env python
"""Tests ChrAB."""

import sys
import os
# Use beta version of pydvkbiology
sys.path.insert(0, '{GIT}/biocode'.format(GIT=os.environ['GIT']))
from pydvkbiology.util.tsvread import tbl2namedtuple
from pydvkbiology.util.chr_ab import ChrAB
from PyBiocode.UCSC.CytoBandMm10 import CytoBand

def test():
  """Read a tsv file containing chrAB info. Store/retrieve data from ChrAB object."""
  fin_tsv = '../data/overlap_ENS_genes.tsv'
  data_nts = tbl2namedtuple(fin_tsv, "Nt")
  hdrs_chrAB = ['chromosome', 
                'start_position_on_the_genomic_accession', 
                'end_position_on_the_genomic_accession', 
                'orientation']
  orgn = CytoBand() # Cytoband info for Mouse genome
  for nt in data_nts:
    chr_ab = ChrAB(
      getattr(nt, hdrs_chrAB[0]),      # schr
      int(getattr(nt, hdrs_chrAB[1])), # start_bp
      int(getattr(nt, hdrs_chrAB[2])), # stop_bp
      getattr(nt, hdrs_chrAB[3]),      # orientation
      orgn)
    print chr_ab.get_plotXs()


if __name__ == '__main__':
  test()
