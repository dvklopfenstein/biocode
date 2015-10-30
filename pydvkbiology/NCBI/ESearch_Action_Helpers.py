#!/usr/bin/env python
"""This script downloads NCBI records based on user search query.

   Requires the biopython package.
"""

# Copyright (C) 2014-2015 DV Klopfenstein.  All rights reserved.
#
# http://www.gnu.org/licenses/gpl-2.0.html#SEC1
#
# Helpers for using the NCBI's EUtils through biopython as used in my research.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


# To cite this script, please use:
#
# Klopfenstein D.V. (2014) Access to the NCBI's EUtils through biopython as used in daily lab work. [Computer program]. 
# Available at://github.com/dklopfenstein/biocode/blob/master/PyDkBio/NCBI/ESearch_Action_Helpers.py 


import sys
import os
import shutil
import re

from Bio import Entrez
import requests

__author__ = "DV Klopfenstein"

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
    usehistory="y") # NCBI prefers we use history(QueryKey, WebEnv) for next acess
  record = Entrez.read(socket_handle)
  socket_handle.close()
  
  if 'IdList' in record and record['IdList']:
    return record
  else:
    raise Exception("NO IDS FOUND FOR '{}' SEARCH({})\n".format(db, query))

# -------------------------------------------------------
def EPost(db, IDs, email, LOG=sys.stdout, step=10):
  """Posts to NCBI WebServer of any number of UIDs."""
  ## http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc112
  Entrez.email = email
  # Load the first 1...(step-1) UIDs to Entrez using epost. Get WebEnv to finish post."""
  strIDs = map(str, IDs)
  id_str = ','.join(strIDs[:step])
  # epost produces WebEnv value ($web1) and QueryKey value ($key1) 
  socket_handle = Entrez.epost(db, id=id_str)
  record = Entrez.read(socket_handle)
  if LOG is not None:
    LOG.write('FIRST EPOST RESULT: {}\n'.format(record))
    LOG.write("QueryKey({:>6})  IDs={}\n".format(record['QueryKey'], id_str))
  socket_handle.close()
  if 'WebEnv' in record:
    WebEnv = record['WebEnv']
    num_IDs = len(strIDs)
    # Load the remainder of the UIDs using epost
    for idx in range(step, num_IDs, step):
      end_pt = idx+step
      if num_IDs < end_pt:
        end_pt = num_IDs
      #print '{:3} {:3} {:3}'.format(num_IDs, idx, end_pt)
      id_str = ','.join(strIDs[idx:end_pt])
      socket_handle = Entrez.epost(db, id=id_str, WebEnv=WebEnv)
      record = Entrez.read(socket_handle)
      WebEnv = record['WebEnv']
      LOG.write("QueryKey({:>6})  strIDs={}\n".format(record['QueryKey'], id_str))
      socket_handle.close()
  else:
    raise Exception("NO WebEnv RETURNED FROM FIRST EPOST")
  if LOG is not None: LOG.write('LAST  EPOST RESULT: {}\n'.format(record))
  return record
  

# -------------------------------------------------------
def ESummary_from_Post(db, QueryKey, WebEnv, email):
  """Give a post reoord. Get an esummary ."""
  Entrez.email = email
  socket_handle = Entrez.esummary(db=db, query_key=QueryKey, WebEnv=WebEnv)
  record = Entrez.read(socket_handle) 
  socket_handle.close()
  return record


# -------------------------------------------------------
# einfo: http://www.ncbi.nlm.nih.gov/books/NBK25499/
def get_DbList():
  """Gets a list of valid Entrez databases."""
  socket_handle = Entrez.einfo()
  record = Entrez.read(socket_handle)
  socket_handle.close()
  return record['DbList']

def prt_DbList(PRT=sys.stdout):
  dblist = get_DbList()
  for db in dblist:
    PRT.write('{}\n'.format(db)) 


def get_DbStats(db, version='2.0', retmode='xml'):
  """Return stats about an Entrez database.

     db:      Use get_DbList to get valid entries
     retmode: 'xml' or 'json'
  """
  socket_handle = Entrez.einfo(
    db=db, 
    version=version, 
    retmode=retmode)
  record = Entrez.read(socket_handle)
  socket_handle.close()
  return record

# -------------------------------------------------------
def EFetch_and_write(db, fout, typemode, record, batch_size=100, PRT=sys.stdout):
  """Fetches NCBI records returned from last search.

  For NCBI's online documentation of efetch:
    http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch 
  """
  downloaded_data = None 
  # Write the list of UIDs in the record
  tsv = get_tsv_filename(fout)
  wr_IDs(tsv, record)

  # EFetch records found for IDs returned in ESearch...
  # Search for IDs returned using ID of the above Web Search
  FOUT = open(fout, 'w')
  N  = len(record['IdList'])
  WE = record['WebEnv']
  QK = record['QueryKey']
  #print "AAAA", N, batch_size
  for start in range(0, N, batch_size):
    #print "BBBB", start
    socket_handle = None
    msg = '  EFetching up to {:5} records, starting at {}\n'.format(batch_size,start)
    PRT.write(msg); PRT.flush()
    sys.stdout.write(msg)
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
      print "db:", db
      print "retstart:", start
      print "retmax:", batch_size
      print "rettype:", typemode[0]
      print "retmode:", typemode[1]
      print "WebEnv:", WE
      print "QueryKey:", QK
      msg = "*FATAL: NETWORK OR MEMORY PROBLEM: {}".format(e)
      PRT.write(msg)
      sys.stdout.write(msg)
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
  PRT.write("  WROTE: {}\n".format(fout))
 
  sys.stdout.write("""
    Need to revisit reading XML reading another way. 
    Biopython XML no longer working for XML files from NCBI Gene.\n""")
  if N > batch_size and typemode[1] == "xml": # DVK Biopython XML not working
    Entrez_strip_extra_eSummaryResult(fout)   # DVK Biopython XML not working

  return downloaded_data


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
  if 'IdList' in record:
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
  if 'Count' in record and 'RetMax' in record and record['Count'] != record['RetMax']:
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

