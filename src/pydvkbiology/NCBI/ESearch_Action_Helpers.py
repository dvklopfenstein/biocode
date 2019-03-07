#!/usr/bin/env python
"""This script downloads NCBI records based on user search query.

   Requires the biopython package.
"""

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2014-2018 DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import sys
import os
import shutil
import re
import traceback
import urllib

from Bio import Entrez

# -------------------------------------------------------
def find_IDs_with_ESearch(database, retmax, email, query, **esearch):
    """Searches an NCBI database for a user search term, returns NCBI records."""
    fcgi = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    # Provide your email to the NCBI so they may contact you prior
    # to shutting down server access in the case of inadvertant over-use.
    Entrez.email = email

    # ESearch for NCBI IDs related to User Search...
    record = None
    try:
        socket_handle = Entrez.esearch(
            db=database,
            term=query,
            retmax=retmax,
            usehistory="y", # NCBI prefers we use history(QueryKey, WebEnv) for next acess
            **esearch)
        record = Entrez.read(socket_handle)
        socket_handle.close()
    except urllib.error.HTTPError as errobj:
      print('HTTPError = {ERR}'.format(ERR=str(errobj.code)))
      traceback.print_exc()
    except urllib.error.URLError as errobj:
      print('URLError = {ERR}'.format(ERR=str(errobj.reason)))
      traceback.print_exc()
    #### except urllib.error.HTTPException as errobj:
    ####   print('urllib.error.HTTPException')
    ####   traceback.print_exc()
    except Exception as errobj:
      print(errobj)
      traceback.print_exc()

    if record is not None and 'IdList' in record and record['IdList']:
        return record

# -------------------------------------------------------
def EPost(database, ids, email, log=sys.stdout, step=10):
    """Posts to NCBI WebServer of any number of UIDs."""
    ## http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc112
    Entrez.email = email
    # Load the first 1...(step-1) UIDs to Entrez using epost. Get WebEnv to finish post."""
    str_ids = map(str, ids)
    id_str = ','.join(str_ids[:step])
    # epost produces WebEnv value ($web1) and QueryKey value ($key1)
    socket_handle = Entrez.epost(database, id=id_str)
    record = Entrez.read(socket_handle)
    if log is not None:
        log.write('FIRST EPOST RESULT: {}\n'.format(record))
        log.write("QueryKey({:>6})  ids={}\n".format(record['QueryKey'], id_str))
    socket_handle.close()
    if 'WebEnv' in record:
        webenv = record['WebEnv']
        num_ids = len(str_ids)
        # Load the remainder of the UIDs using epost
        for idx in range(step, num_ids, step):
            end_pt = idx+step
            if num_ids < end_pt:
                end_pt = num_ids
            #print '{:3} {:3} {:3}'.format(num_ids, idx, end_pt)
            id_str = ','.join(str_ids[idx:end_pt])
            socket_handle = Entrez.epost(database, id=id_str, WebEnv=webenv)
            record = Entrez.read(socket_handle)
            webenv = record['WebEnv']
            if log is not None:
                log.write("QueryKey({:>6})  str_ids={}\n".format(record['QueryKey'], id_str))
            socket_handle.close()
    else:
        raise Exception("NO WebEnv RETURNED FROM FIRST EPOST")
    if log is not None: log.write('LAST  EPOST RESULT: {}\n'.format(record))
    return record


# -------------------------------------------------------
def ESummary_from_Post(databse, querykey, WebEnv, email):
    """Give a post reoord. Get an esummary ."""
    Entrez.email = email
    socket_handle = Entrez.esummary(db=database, query_key=querykey, WebEnv=WebEnv)
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
    for database in dblist:
        PRT.write('{}\n'.format(database))


def get_DbStats(database, version='2.0', retmode='xml'):
    """Return stats about an Entrez database.

       database:      Use get_DbList to get valid entries
       retmode: 'xml' or 'json'
    """
    socket_handle = Entrez.einfo(
        db=database,
        version=version,
        retmode=retmode)
    record = Entrez.read(socket_handle)
    socket_handle.close()
    return record

# -------------------------------------------------------
def EFetch_and_write(desc, database, fout_entrez, typemode, record, batch_size=100, log=sys.stdout):
    """Fetches NCBI records returned from last search.

    For NCBI's online documentation of efetch:
      http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
    """
    if record is not None:
        num_ids = len(record['IdList'])
        # Write the list of UIDs in the record
        fout_tsv = get_tsv_filename(fout_entrez)
        _wrtsv_ids(fout_tsv, record, log)
        EFetch_and_write_N(desc, database, fout_entrez, typemode, record, num_ids, batch_size)


def download_records(desc, database, fout_dl, typemode, record, bnum, batch_size=100):
    """Download records and write to a text file."""
    with open(fout_dl, 'wb') as ostrm:
        downloaded_data = EFetch_and_write_WEQK_N(
            desc, database, ostrm, typemode,
            record['WebEnv'], record['QueryKey'], bnum, batch_size)
        sys.stdout.write("  WROTE: {}\n".format(fout_dl))
        return downloaded_data


def EFetch_and_write_N(desc, database, fout_dl, typemode, record, bnum, batch_size=100):
    downloaded_data = download_records(desc, database, fout_dl, typemode, record, bnum, batch_size)
    # sys.stdout.write("""
    #   Need to revisit reading XML reading another way.
    #   Biopython XML no longer working for XML files from NCBI Gene.\n""")
    if bnum > batch_size and typemode[1] == "xml": # DVK Biopython XML not working
        Entrez_strip_extra_eSummaryResult(fout)   # DVK Biopython XML not working
    return downloaded_data


def EFetch_and_write_WEQK_N(desc, database, ostrm, typemode, WE, QK, N, batch_size=100):
    downloaded_data = None
    # EFetch records found for IDs returned in ESearch...
    # Search for IDs returned using ID of the above Web Search
    #print "AAAA", N, batch_size
    for start in range(0, N, batch_size):
        #print "BBBB", start
        socket_handle = None
        msg = '  QueryKey({:>6}) EFetching(database={}) up to {:5} records, starting at {}; {}\n'.format(
            QK, database, batch_size, start, desc)
        #sys.stdout.write(msg)
        try:
            # pylint: disable=bad-whitespace
            socket_handle = Entrez.efetch(
                db        = database,
                retstart  = start,       # dflt: 1
                retmax    = batch_size,  # max: 10,000
                rettype   = typemode[0], # Ex: medline
                retmode   = typemode[1], # Ex: text
                webenv    = WE,
                query_key = QK)
        except IOError as err:
            msg = "\n*FATAL: EFetching FAILED: {}".format(err)
            sys.stdout.write(msg)
            sys.stdout.write("  database: {}\n".format(database))
            sys.stdout.write("  retstart: {}\n".format(start))
            sys.stdout.write("  retmax: {}\n".format(batch_size))
            sys.stdout.write("  rettype: {}\n".format(typemode[0]))
            sys.stdout.write("  retmode: {}\n".format(typemode[1]))
            sys.stdout.write("  WebEnv: {}\n".format(WE))
            sys.stdout.write("  QueryKey: {}\n".format(QK))
            if socket_handle is not None:
                socket_handle.close()
                socket_handle = None

        if socket_handle is not None:
            try:
                # Read the downloaded data from the socket handle
                downloaded_data = socket_handle.read()
                socket_handle.close()
                mtch = re.search(r'(ERROR.*\n)', downloaded_data)
                if mtch:
                    sys.stdout.write(mtch.group(1))
                ostrm.write(downloaded_data)
                ostrm.flush()
            except Exception as err:
                sys.stdout.write("*FATAL: PROBLEM READING FROM SOCKET HANDLE: {}\n".format(str(err)))
        else:
            sys.stdout.write("*FATAL: NO SOCKET HANDLE TO READ FROM\n")
    return downloaded_data


def ELink_webenvQK_num(desc, webenv, querykey, linkname, num, batch_size=100, log=sys.stdout):
    """https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink"""
    ids = []
    dbfrom = 'pubmed'
    # EFetch records found for IDs returned in ESearch...
    # Search for IDs returned using ID of the above Web Search
    #print "AAAA", N, batch_size
    for start in range(0, num, batch_size):
        #print "BBBB", start
        socket_handle = None
        msg = '  QueryKey({:>6}) ELinking(db={}) up to {:5} records, starting at {}; {}\n'.format(
            querykey, linkname, batch_size, start, desc)
        #log.write(msg); log.flush()
        #sys.stdout.write(msg)
        try:
            # pylint: disable=bad-whitespace
            socket_handle = Entrez.elink(
                dbfrom    = dbfrom,
                retstart  = start,       # dflt: 1
                retmax    = batch_size,  # max: 10,000
                linkname  = linkname,
                webenv    = webenv,
                query_key = querykey)
        except IOError as err:
            msg = "\n*FATAL: EFetching FAILED: {}".format(err)
            log.write(msg)
            sys.stdout.write(msg)
            sys.stdout.write("  dbfrom: {}\n".format(dbfrom))
            sys.stdout.write("  retstart: {}\n".format(start))
            sys.stdout.write("  retmax: {}\n".format(batch_size))
            sys.stdout.write("  linkname: {}\n".format(linkname))
            sys.stdout.write("  WebEnv: {}\n".format(webenv))
            sys.stdout.write("  QueryKey: {}\n".format(querykey))
            if socket_handle is not None:
                socket_handle.close()
                socket_handle = None

        if socket_handle is not None:
            try:
                # Read the downloaded data from the socket handle
                # [{u'LinkSetDb': [{u'DbTo': 'pubmed', u'Link': [{u'Id': '5668'}, {u'Id': ...
                #print "ddddd", socket_handle
                record = Entrez.read(socket_handle)
                #print "DDDDD", record
                socket_handle.close()
                if record:
                    if not record[0]["ERROR"]:
                        # keys: DbTo Link LinkName.    Link list:[{'Id':'NNNNN'}, {'Id': ...
                        # keys: LinkSetDb DbFrom IdList LinkSetDbHistory ERROR
                        if record[0][u'LinkSetDb']:
                            ids.extend([int(k2v[u'Id']) for k2v in record[0][u'LinkSetDb'][0][u'Link']])
                        #print "EEEEE", " ".join(record[0].keys())
                        #sys.stdout.write(record[0].keys())
            except Exception as err:
                sys.stdout.write("*FATAL: PROBLEM READING FROM SOCKET HANDLE: {}\n".format(str(err)))
        else:
            sys.stdout.write("*FATAL: NO SOCKET HANDLE TO READ FROM\n")
    return ids


def Entrez_strip_extra_eSummaryResult(entrez_datafile):
    """For an XML file EFetched in multiple batches, strip extra eSummaryResult lines.

    The first </eSummaryResult> will cause Entrez.parse to prematurely stop parsing.

    """
    trash = '_'.join([entrez_datafile, 'trash'])
    # Moved the poorly formatted XML file to <filename>_trash
    shutil.move(entrez_datafile, trash)
    # Write newly formatted XML file into original filename
    with open(entrez_datafile, 'w') as ofstrm:
        # pylint: disable=bad-whitespace
        xml_version  = None
        doctype      = None
        eresult      = None
        cmpdoc = re.compile(r'DOCTYPE\s+(\S+)\s+')
        # """Only write the xml_version|DOCTYPE|eSummaryResult once."""
        with open(trash) as ifstrm:
            for line in ifstrm:
                if   'xml version' in line:
                    if xml_version is None:
                        ofstrm.write(line) # Write line once, the first time it is seen
                        xml_version = True
                elif 'DOCTYPE' in line:
                    if doctype is None:
                        mtch = cmpdoc.search(line)
                        if mtch:
                            ofstrm.write(line) # Write line once, the first time it is seen
                            doctype = mtch.group(1)
                        else:
                            print("*FATAL: ERROR STRIPPING XML({})".format(entrez_datafile))
                elif doctype is not None and re.search(r'^</?{}>\s*$'.format(doctype), line):
                    if eresult is None:
                        ofstrm.write(line) # Write line once, the first time it is seen
                        eresult = True
                else:
                    ofstrm.write(line)
        ofstrm.write('</{}>\n'.format(doctype))


def _wrtsv_ids(fout_tsv, record, log=sys.stdout):
    """Write list of IDs in a tsv file."""
    if 'IdList' in record:
        with open(fout_tsv, 'wb') as ostrm:
            _chk_num_ids(log, record)
            for rec_id in record['IdList']:
                ostrm.write('{ID}\n'.format(ID=rec_id))
            msg = "  ESearch Returned {N:6,} IDs WROTE: {TSV}\n"
            log.write(msg.format(TSV=fout_tsv, N=len(record['IdList'])))

def _chk_num_ids(log, record):
    """Alerts the User to increase retmax if not all records are returned."""
    if 'Count' in record and 'RetMax' in record and record['Count'] != record['RetMax']:
        txt = '**Note: {} PubMed IDs returned out of {} total found.\n'.format(
            record['RetMax'],
            record['Count'])
        log.write(txt)
        sys.stdout.write(txt)

def get_tsv_filename(fout):
    """NCBI IDs are stored in a ".tsv" file.  Runtime notes written into ".log" file"""
    return ''.join([os.path.splitext(fout)[0], '_ESearch_IDs.tsv'])

def get_fetch_fout(filename):
    """Create a output file name where EFetch data will be stored."""
    return ''.join([os.path.basename(os.path.splitext(filename)[0]), '.Entrez_downloads'])


# Copyright (C) 2014-2018 DV Klopfenstein. All rights reserved.
