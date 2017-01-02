#!/usr/bin/env python
"""This scildreaming@travelript downloads PubMed abstracts from NCBI's PubMed based on a user query.

   Requires the biopython package.
"""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2014-2015 DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import PyBiocode.NCBI.EUtils_Apps as EA

# Copyright (C) 2014-2015 DV Klopfenstein.  All rights reserved.

__author__ = "DV Klopfenstein"


# -------------------------------------------------------
def run_example():
  email = "music_pupil@yahoo.com"
  query = "disease gene identification strategies for exome sequencing"
  query = "asthma[mesh] AND leukotrienes[mesh] AND 2009[pdat]"
  query = 'autism[TI] AND "last 14 days" [DP]'
  retmax = "100"
  EA.get_abstracts('medline.md', email, query, retmax)

def example2():
  EA.get_abstracts(
    'asthma_pubmed_ids.md',    # Markdown text File written and filled with PubMed Abstracts
    email = 'music_pupil@yahoo.com',
    query = 'asthma[mesh] AND leukotrienes[mesh] AND "last 6 months" [DP]')
  

# -------------------------------------------------------
if __name__ == '__main__':
  #run_example()
  example2()