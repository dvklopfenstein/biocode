#!/usr/bin/env python
"""This script downloads NCBI records based on user search query.

   Requires the biopython package.
"""

import sys
import os
import shutil
import re

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
def EFetch_and_write(db, retmax, fout, typemode, record, batch_size=100):
  """Fetches NCBI records returned from last search.

  For NCBI's online documentation of efetch:
    http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch 
  """
  tsv = get_tsv_filename(fout)
  wr_IDs(tsv, record)

  # EFetch records found for IDs returned in ESearch...
  # Search for IDs returned using ID of the above Web Search
  FOUT = open(fout, 'w')
  N  = len(record['IdList'])
  WE = record['WebEnv']
  QK = record['QueryKey']
  for start in range(0, N, batch_size):
    socket_handle = None
    sys.stdout.write('  EFetching up to {:5} records, starting at {}\n'.format(
      batch_size,start))
    try:
      socket_handle = Entrez.efetch(
        db        = db,
        retstart  = start,
        retmax    = batch_size, 
        rettype   = typemode[0],
        retmode   = typemode[1],
        webenv    = WE,
        query_key = QK)
    except IOError, e:
      print "*FATAL: NETWORK OR MEMORY PROBLEM: {}".format(e)
      if socket_handle is not None:
        socket_handle.close()
        socket_handle = None

    if socket_handle is not None:
      try:
        # Read the downloaded data from the socket handle
        downloaded_data = socket_handle.read()
        socket_handle.close()
        FOUT.write(downloaded_data)
      except Exception:
        print "*FATAL: PROBLEM READING FROM SOCKET HANDLE: {}"
    else:
      print "*FATAL: NO SOCKET HANDLE TO READ FROM"
      

  # Close files
  FOUT.close(); 
  sys.stdout.write("  WROTE: {}\n".format(fout))
  
  if N > batch_size and typemode[1] == "xml":
    Entrez_strip_extra_eSummaryResult(fout)


# -------------------------------------------------------
def Entrez_strip_extra_eSummaryResult(Entrez_datafile):
  """For an XML file EFetched in multiple batches, strip extra eSummaryResult lines.

  The first </eSummaryResult> will cause Entrez.parse to prematurely stop parsing.

  """
  trash = '_'.join([Entrez_datafile, 'trash'])
  # Moved the poorly formatted XML file to <filename>_trash
  shutil.move(Entrez_datafile, trash)
  # Write newly formatted XML file into original filename
  FOUT = open(Entrez_datafile, 'w')
  xml_version  = None
  DOCTYPE      = None
  eResult      = None
  S = re.compile(r'DOCTYPE\s+(\S+)\s+')
  """Only write the xml_version|DOCTYPE|eSummaryResult once."""
  with open(trash) as FIN:
    for line in FIN:
      if   'xml version' in line:
        if xml_version is None:
          FOUT.write(line) # Write line once, the first time it is seen
          xml_version = True
      elif 'DOCTYPE' in line:
        if DOCTYPE is None:
          M = S.search(line)
          if M:
            FOUT.write(line) # Write line once, the first time it is seen
            DOCTYPE = M.group(1)
          else:
            print "*FATAL: ERROR STRIPPING XML({})".format(Entrez_datafile)
      elif DOCTYPE is not None and re.search(r'^</?{}>\s*$'.format(DOCTYPE), line):
        if eResult is None:
          FOUT.write(line) # Write line once, the first time it is seen
          eResult = True
      else:
        FOUT.write(line)
  FOUT.write('</{}>\n'.format(DOCTYPE))
  FOUT.close()
  FIN.close()


# -------------------------------------------------------
def wr_IDs(tsv, record):
  TSV = open(tsv, 'w')
  chk_num_IDs(sys.stdout, record)
  for ID in record['IdList']:
    TSV.write('{}\n'.format(ID))
  TSV.close();  
  sys.stdout.write("  WROTE: {}  ESearch Returned # {} IDs\n".format(
    tsv, len(record['IdList'])))

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
def get_tsv_filename(fout):
  """NCBI IDs are stored in a ".tsv" file.  Runtime notes written into ".log" file"""
  basename = os.path.basename(os.path.splitext(fout)[0])
  tsv = ''.join([basename, '_ESearch_IDs.tsv'])
  return tsv

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

