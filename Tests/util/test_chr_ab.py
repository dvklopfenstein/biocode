#!/usr/bin/env python
"""Tests ChrAB."""

from pydvkbiology.util.chr_ab import ChrAB
from PyBiocode.UCSC.CytoBandMm10 import CytoBand
from PyBiocode.dnld.NCBI.genes_NCBI_mus_ProteinCoding import GeneID2nt

def test():
  """Read a tsv file containing chrAB info. Store/retrieve data from ChrAB object."""
  #fin_tsv = '../data/overlap_ENS_genes.tsv'
  data_nts = GeneID2nt.values()
  hdrs_chrAB = ['chromosome', 
                'start_position_on_the_genomic_accession', 
                'end_position_on_the_genomic_accession', 
                'orientation']
  orgn = CytoBand() # Cytoband info for Mouse genome
  for nt in data_nts:
    schr   = getattr(nt, hdrs_chrAB[0]) # schr
    bp0    = getattr(nt, hdrs_chrAB[1]) # start_bp
    bpN    = getattr(nt, hdrs_chrAB[2]) # stop_bp
    fwdrev = getattr(nt, hdrs_chrAB[3]) # orientation
    if schr and bp0 and bpN:
      chr_ab = ChrAB(schr, int(bp0), int(bpN), orientation=fwdrev, orgn=orgn)
      print schr, bp0, bpN, fwdrev, chr_ab.is_fwd(), chr_ab.get_plotXs()


if __name__ == '__main__':
  test()
