#!/usr/bin/env python
"""This script downloads NCBI records based on user search query.

   Requires the biopython package.
"""

import sys
import os

from Bio import Entrez

# -------------------------------------------------------
def find_IDs_with_ESearch(db, retmax, email, query):
  """Searches an NCBI database for a user search term, returns NCBI records."""

  # Provide your email to the NCBI so they may contact you prior 
  # to shutting down server access in the case of inadvertant over-use.
  Entrez.email = email

  # ESearch for NCBI IDs related to User Search...
  socket_handle = Entrez.esearch(
    db=db,
    retmax=retmax, 
    term=query,
    usehistory="y")
  record = Entrez.read(socket_handle)
  socket_handle.close()
  
  if 'IdList' in record and record['IdList']:
    return record
  else:
    raise Exception("NO IDS FOUND FOR '{}' SEARCH({})\n".format(db, query))


# -------------------------------------------------------
def EFetch_and_write(db, retmax, fout, typemode, record):
  """Fetches NCBI records returned from last search.

  For NCBI's online documentation of efetch:
    http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch 
  """
  tsv, log = get_log_names(fout)
  TSV = open(tsv, 'w')
  LOG = open(log, 'w')
  chk_num_IDs(LOG, record)
  for ID in record['IdList']:
    TSV.write('{}\n'.format(ID))

  # EFetch records found for IDs returned in ESearch...
  # Search for IDs returned using ID of the above Web Search
  socket_handle = Entrez.efetch(
    db        = db,
    retmax    = retmax, 
    rettype   = typemode[0],
    retmode   = typemode[1],
    webenv    = record['WebEnv'],
    query_key = record['QueryKey'])

  # Read the downloaded data from the socket handle
  downloaded_data = socket_handle.read()
  socket_handle.close()

  # Write record data into a file
  FOUT = open(fout, 'w')
  FOUT.write(downloaded_data)

  # Close files
  N = len(record['IdList'])
  FOUT.close(); sys.stdout.write("  WROTE: {}\n".format(fout))
  TSV.close();  sys.stdout.write("  WROTE: {}  Returned # {} IDs\n".format(tsv, N))
  LOG.close();  sys.stdout.write("  WROTE: {}\n".format(log))
  

# -------------------------------------------------------
def chk_num_IDs(PRT, record):
  """ALerts the User to increase retmax if not all records are returned."""
  if record['Count'] != record['RetMax']:
    txt = '**Note: {} PubMed IDs returned out of {} total found.\n'.format(
      record['RetMax'],
      record['Count'])
    PRT.write(txt)
    sys.stdout.write(txt)


# -------------------------------------------------------
def get_log_names(fout):
  """NCBI IDs are stored in a ".tsv" file.  Runtime notes written into ".log" file"""
  basename = os.path.basename(os.path.splitext(fout)[0])
  tsv = ''.join([basename, '_IDs.tsv'])
  log = ''.join([basename, '.log'])
  return tsv, log

# -------------------------------------------------------
def get_fetch_fout(filename):
  """Create a output file name where EFetch data will be stored."""
  return ''.join([os.path.basename(os.path.splitext(filename)[0]), '.Entrez_downloads'])

# -------------------------------------------------------
def get_args():
  email = "music_pupil@yahoo.com"
  query = "asthma[mesh] AND leukotrienes[mesh] AND 2009[pdat]"
  max_records = 500
  return email, query, max_records

