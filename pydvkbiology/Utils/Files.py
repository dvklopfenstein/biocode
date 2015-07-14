"""Read tab-separated files (.tsv) and comma-separated files (.csv). Store in lists, dicts, ..."""

# Copyright (C) 2014-2015 DV Klopfenstein. All rights reserved.
__author__ = 'DV Klopfenstein'

import re
import sys
import collections as cx

# I work on a small screen, so use 2 spaces instead of 4:
# pylint: disable=W0311

#------------------------------------------------------------------
# Users call these functions to read a tsv or csv file and load
# the file contents into:
#   1. A list of lists(1 list per line)
#   2. A list containing only one column in the file
#   3. A list of lists(1 list contains only some fields in the line)
#   4. A dictionary.  Can be used to return a GeneID-to-Symbol or vice versa
#   ...
#------------------------------------------------------------------
def tbl2hdrs(fin, sep=r'\t+', hdr_ex=None, log=sys.stdout):
  """Read tsv/csv and return header information.
     h2i = tbl2hdrs(fin)
  """
  sep = get_sep(fin)
  file_hndl = FileHelperObj(sep, None, None, hdr_ex, log)
  return file_hndl.get_h2i(fin, None)

def tbl2lists(fin,
              sep=r'\t', ints=None, floats=None, hdr_ex=None, log=sys.stdout):
  """Read tsv/csv and store data in list of lists.
     data, h2i = tbl2lists(fin)
  """
  sep = get_sep(fin)
  file_hndl = FileHelperObj(sep, ints, floats, hdr_ex, log)
  return file_hndl.run(file_hndl.tbl2lists, fin, None)

def tbl2namedtuple(fin, tuplename,
                   sep=r'\t', ints=None, floats=None, hdr_ex=None, log=sys.stdout):
  """Read tsv/csv and store data in list of named tuples.
     data = tbl2namedtuple(fin, 'NCBI_Gene')
  """
  sep = get_sep(fin)
  file_hndl = FileHelperObj(sep, ints, floats, hdr_ex, log)
  return file_hndl.run_namedtuple(fin, tuplename)

def tbl2list(fin, hdr,
             sep=r'\s*\t\s*', ints=None, floats=None, hdr_ex=None, log=sys.stdout):
  """Read tsv/csv and store data in a list."""
  sep = get_sep(fin)
  if hdr_ex is None:
    hdr_ex = hdr
  file_hndl = FileHelperObj(sep, ints, floats, hdr_ex, log)
  return file_hndl.run(file_hndl.tbl2list, fin, [hdr])[0]

def tbl2sublist(fin, hdrs,
                sep=r'\s*\t\s*', ints=None, floats=None, hdr_ex=None, log=sys.stdout):
  """Read tsv/csv and store data in list of sub-lists.
     data = tbl2sublist(fin, ['chromosome', 'start_bp', 'stop_bp', Symbol'])
  """
  sep = get_sep(fin)
  file_hndl = FileHelperObj(sep, ints, floats, hdr_ex, log)
  return file_hndl.run(file_hndl.tbl2sublist, fin, hdrs)[0]

def tbl2dict(fin, hdr, val,
             sep=r'\s*\t\s*', ints=None, floats=None, hdr_ex=None, log=sys.stdout):
  """Read tsv/csv and store data in a dictionary: d[key]=val."""
  sep = get_sep(fin)
  file_hndl = FileHelperObj(sep, ints, floats, hdr_ex, log)
  return dict(file_hndl.run(file_hndl.tbl2sublist, fin, [hdr, val])[0])

def tbl2dict2lst(fin, key_hdr, val_hdrs,
                 sep=r'\s*\t\s*', ints=None, floats=None, hdr_ex=None, log=sys.stdout):
  """Read tsv/csv and store data in a dictionary. d[key]=[val, val, ...]."""
  sep = get_sep(fin)
  file_hndl = FileHelperObj(sep, ints, floats, hdr_ex, log)
  data_h2i = file_hndl.run(file_hndl.tbl2sublist, fin, [key_hdr] + val_hdrs)
  return {elem[0]:elem[1:] for elem in data_h2i[0]}

def tbl2dicts(fin, key_hdr, val_hdrs,
              sep=r'\s*\t\s*', ints=None, floats=None, hdr_ex=None, log=sys.stdout):
  """Read tsv/csv and store data in a dictionary. d[key]={hdr0:val0, hdr1:val1, ...}."""
  sep = get_sep(fin)
  file_hndl = FileHelperObj(sep, ints, floats, hdr_ex, log)
  data_h2i = file_hndl.run(file_hndl.tbl2sublist, fin, [key_hdr] + val_hdrs)
  ret = {}
  for elem in data_h2i[0]:
    key = elem[0]
    ret[key] = {}
    for hdr, val in zip(val_hdrs, elem[1:]):
      ret[key][hdr] = val
  return ret


#------------------------------------------------------------------
# Non-user code.  This code is accessed by the user code.
#------------------------------------------------------------------
def get_sep(fin):
  """Uses extension(.tsv, .csv) to determine separator."""
  if '.tsv' in fin:
    return r'\t'
  elif '.csv' in fin:
    return r','
  else:
    return r'\t'

#------------------------------------------------------------------
class FileHelperObj(object):
  """Helps read files and write data structures."""

  def __init__(self, sep, ints, floats, hdr_ex, log):
    self.log = log
    self.int_hdrs = [
        'tax_id', 'GeneID', 'CurrentID',  # NCBI Gene
        'start_position_on_the_genomic_accession', # NCBI Gene
        'end_position_on_the_genomic_accession',   # NCBI Gene
        'exon_count',                              # NCBI Gene
        'OMIM',                                    # NCBI Gene
        'Start', 'start', 'End', 'end',   # Cluster
        'Len', 'len', 'Length', 'length', # cluster
        'Qty', 'qty', '# Genes']          # Cluster
    if ints is not None:
      if len(ints) != 0:
        self.int_hdrs.extend(ints)
      else:
        self.int_hdrs = []
    self.float_hdrs = ['Density', 'density', 'MinDensity']  # Cluster
    # These are formated for expected sorting: eg. Chr "09", "10"
    self.strpat_hdrs = {'Chr':'{:>2}', 'chromosome':'{:>2}'}
    if floats is not None:
      self.float_hdrs.extend(floats)
    self.idxs_float = []  # run() inits proper values
    self.idxs_int = []    # run() inits proper values
    self.idxs_strpat = [] # run() inits proper values
    # Data Members used by all functions
    self.fin = None
    self.hdr2idx = None
    self.len = 0
    self.sep = sep
    self.hdr_ex = hdr_ex
    # Data Members used by various functions
    self.ret_list = [] #             tbl2list
    self.hdrs_usr = []     # tbl2sublist tbl2list
    self.usr_max_idx = None

  def get_h2i(self, fin, hdrs_usr):
    """Read csv/tsv file and return specified data in a list of lists."""
    self.fin = fin
    with open(fin) as fin_stream:
      for line in fin_stream:
        line = line.rstrip('\r\n') # chomp
        if not self.hdr2idx:
          if self.do_hdr(line, hdrs_usr):
            return self.hdr2idx
    return None

  def do_hdr(self, line, hdrs_usr):
    """Initialize self.h2i."""
    # If there is no header hint, consider the first line the header.
    if self.hdr_ex is None:
      self._init_hdr(line, hdrs_usr)
      return True
    # If there is a header hint, examine each beginning line until header hint is found.
    elif self.hdr_ex in line:
      self._init_hdr(line, hdrs_usr)
      return True
    return False

  def run(self, fnc, fin, hdrs_usr):
    """Read csv/tsv file and return specified data in a list of lists."""
    self.fin = fin
    with open(fin) as fin_stream:
      for lnum, line in enumerate(fin_stream):
        line = line.rstrip('\r\n') # chomp
        # Obtain Data if headers have been collected from the first line
        if self.hdr2idx:
          self._init_data_line(fnc, fin, lnum, line)
        # Obtain the header
        else:
          self.do_hdr(line, hdrs_usr)
      if self.log is not None:
        self.log.write("  {:9} data READ:  {}\n".format(len(self.ret_list), fin))
    return self.ret_list, self.hdr2idx

  def run_namedtuple(self, fin, tuplename):
    """Read csv/tsv file and return specified data in a list of lists."""
    self.fin = fin
    data = []
    obj = None
    with open(fin) as fin_stream:
      for line in fin_stream:
        line = line.rstrip('\r\n') # chomp
        # Obtain Data if headers have been collected from the first line
        if obj is not None:
          data.append(obj._make(re.split(self.sep, line)))
        # Obtain the header
        else:
          line = line.replace('.', '_')
          hdrs = re.split(self.sep, line)
          if '' in hdrs:
            hdrs = FileHelperObj.replace_nulls(hdrs)
          obj = cx.namedtuple(tuplename, ' '.join(hdrs))
      if self.log is not None:
        self.log.write("  {:9} obj READ:  {}\n".format(len(self.ret_list), fin))
    return data

  @staticmethod
  def replace_nulls(hdrs):
    """Replace '' in hdrs."""
    ret = []
    idx = 0
    for hdr in hdrs:
      if hdr == '':
        ret.append("no_hdr{}".format(idx))
      else:
        ret.append(hdr)
    return ret

  def _init_data_line(self, fnc, fin, lnum, line):
    """Process Data line."""
    fld = re.split(self.sep, line)
    # Lines may contain different numbers of items.
    # The line should have all columns requested by the user.
    if self.usr_max_idx < len(fld):
      self.convert_ints_floats(fld)
      fnc(fld)
    else:
      for fld in enumerate(zip(self.hdr2idx.keys(), fld)):
        print fld
      for hdr in self.hdrs_usr:
        print hdr
      print '# ITEMS ON A LINE:', len(fld)
      print 'MAX USR IDX:', self.usr_max_idx
      raise Exception("ERROR ON LINE {} IN {}".format(lnum+1, fin))

  def convert_ints_floats(self, fld):
    """Convert strings to ints and floats, if so specified."""
    for idx in self.idxs_float:
      fld[idx] = float(fld[idx])
    for idx in self.idxs_int:
      dig = fld[idx]
      #print 'idx={} ({}) {}'.format(idx, fld[idx], fld) # DVK
      fld[idx] = int(fld[idx]) if dig.isdigit() else dig
    for idx in self.idxs_strpat:
      hdr = self.hdr2idx.items()[idx][0]
      pat = self.strpat_hdrs[hdr]
      fld[idx] = pat.format(fld[idx])

  def _init_hdr(self, line, hdrs_usr):
    """Initialize self.hdr2idx, self.len, self.idxs_float, and self.idxs_int"""
    self.hdr2idx = cx.OrderedDict([(v.strip(), i) for i, v in enumerate(re.split(self.sep, line))])
    self.len = len(self.hdr2idx)
    # If user is requesting specific data fields...
    if hdrs_usr is not None:
      # Loop through the user headers
      for usr_hdr in hdrs_usr:
        # If the user header is contained in the file....
        if usr_hdr in self.hdr2idx:
          # Add the user header and the field index to a list
          self.hdrs_usr.append([usr_hdr, self.hdr2idx[usr_hdr]])
        else:
          raise Exception("NO COLUMN({}) FOUND:\n  HDR={}\n".format(
              hdrs_usr, '\n  HDR='.join(self.hdr2idx.keys())))
    usr_hdrs = [E[0] for E in self.hdrs_usr] if self.hdrs_usr else self.hdr2idx
    self._init_idxs_float(usr_hdrs)
    self._init_idxs_int(usr_hdrs)
    self._init_idxs_strpat(usr_hdrs)
    self.usr_max_idx = max(E[1] for E in self.hdrs_usr) if self.hdrs_usr else len(self.hdr2idx)-1

  def _init_idxs_float(self, usr_hdrs):
    """List of indexes whose values will be floats."""
    self.idxs_float = [
        Idx for Hdr, Idx in self.hdr2idx.items() if Hdr in usr_hdrs and Hdr in self.float_hdrs]

  def _init_idxs_int(self, usr_hdrs):
    """List of indexes whose values will be ints."""
    self.idxs_int = [
        Idx for Hdr, Idx in self.hdr2idx.items() if Hdr in usr_hdrs and Hdr in self.int_hdrs]

  def _init_idxs_strpat(self, usr_hdrs):
    """List of indexes whose values will be strings."""
    strpat = self.strpat_hdrs.keys()
    self.idxs_strpat = [
        Idx for Hdr, Idx in self.hdr2idx.items() if Hdr in usr_hdrs and Hdr in strpat]


  def tbl2list(self, field):
    """Return the one item (a list of items) of interest to the user."""
    self.ret_list.extend([field[Hdr_Idx[1]] for Hdr_Idx in self.hdrs_usr])

  def tbl2sublist(self, field):
    """Return the items (a list of lists) of interest to the user."""
    self.ret_list.append([field[Hdr_Idx[1]] for Hdr_Idx in self.hdrs_usr])

  def tbl2lists(self, field):
    """Return all items (a list of lists) read from the tsv/csv file."""
    self.ret_list.append(field)


