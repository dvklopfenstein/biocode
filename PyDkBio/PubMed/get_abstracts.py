#!/usr/bin/env python
"""This script downloads PubMed abstracts from NCBI's PubMed based on a user query.

   Requires the biopython package.
"""

import sys
import os
import datetime

from Bio import Entrez
from Bio import Medline

import PyDkBio.NCBI.ESearch_Action_Helpers as FT

# -------------------------------------------------------
def main():
  """Get user's runtime arguments, query PubMed, and return results."""
  email, query, max_records = get_args()


# -------------------------------------------------------
def run_example():
  db = 'pubmed'

  # Input to FT.find_IDs_with_ESearch
  email = "music_pupil@yahoo.com"
  query = "asthma[mesh] AND leukotrienes[mesh] AND 2009[pdat]"
  query = 'autism[TI] AND "last 14 days" [DP]'
  max_abstracts = "100"

  # Input to FT.EFetch_and_write
  fout = 'medline.md'
  dout = FT.get_fetch_fout(fout)
  typemode = ('medline', 'text')

  # Get IDs, download Entrez records into a locally written file.
  if not os.path.isfile(dout):
    record = FT.find_IDs_with_ESearch(db, max_abstracts, email, query)
    FT.EFetch_and_write(db, max_abstracts, dout, typemode, record) 

  # Write PubMed Abstracts into a markdown text file
  MD = open(fout, 'w')
  MD.write('# NCBI Results for search query:\n* Query: `{Q}`\n* Date: {D}\n'.format(
    Q=query, D=datetime.date.today() ))
  wr_PMID_list(MD, dout)
  wr_PMID_Abstracts(MD, dout)
  MD.close()
  print "  WROTE:", fout


# -------------------------------------------------------
def wr_PMID_list(PRT, Entrez_data):
  """Prints a table of PubMed IDs with links to more detailed information."""
  PRT.write('\n# Table of all PubMed IDs returned with query\n')
  PRT.write("""
| PMID        | Pub           | Title |
| ----------- |:-------------:|:----- |
""")
  with open(Entrez_data) as FIN:
    for RX in Medline.parse(FIN): 
      PRT.write('|[{PMID}] (#PMID{PMID}) |{DP}|{TI}|\n'.format(
        PMID="" if 'PMID' not in RX else RX['PMID'],
        TI  ="" if   'TI' not in RX else RX['TI'],
        DP  ="" if   'DP' not in RX else RX['DP']))

# -------------------------------------------------------
def wr_PMID_Abstracts(PRT, Entrez_data):
  """Prints detailed information from PubMed."""
  PRT.write('\n# Abstracts for all PubMed IDs returned with the user query\n')
  with open(Entrez_data) as FIN:
    for idx,RX in enumerate(Medline.parse(FIN)):
      PRT.write("""
##################################################################
## <a name=PMID{PMID}></a>{idx}) PMID: [{PMID}] (http://www.ncbi.nlm.nih.gov/pubmed/?term={PMID})
* **Title**         : {TI}
* **Journal Title** : {JT}
* **Date of Pub.**  : {DP}
* **Affiliation**   : {AD}
* **Abstract**
{AB}
""".format(
      idx = idx,
      PMID="" if 'PMID' not in RX else RX['PMID'],
      TI  ="" if   'TI' not in RX else RX['TI'],
      JT  ="" if   'JT' not in RX else RX['JT'],
      DP  ="" if   'DP' not in RX else RX['DP'],
      AD  ="" if   'AD' not in RX else RX['AD'],
      AB  ="" if   'AB' not in RX else RX['AB']))

# -------------------------------------------------------
if __name__ == '__main__':
  if len(sys.argv) == 1:
    run_example()
  # Otherwise, get the abstracts the user requests.
  else:
    main()
