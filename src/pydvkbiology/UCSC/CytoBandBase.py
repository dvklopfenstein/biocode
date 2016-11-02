#!/usr/bin/env python

# Copyright (C) 2014-2015 DV Klopfenstein. All rights reserved.
#
# CytoBandBase.py stores CytoBandIdeo data downloaded from UCSC and
# Allows easy access to the CytoBand information from a Python script
# in a species-independent manner.
# note2debra at gmail dot com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details:
#
#   https://www.gnu.org/licenses/gpl-2.0.txt
#
#
# Aydin Tozeren, Distinguished Professor
# August 2014


# To cite this script, please use: 
#
# Klopfenstein D.V. (2014) Storage and Python Access to UCSC's Cytoband Data In A Species-Independent Manner (Version 2.0) 
# [Computer program]. Available at https://github.com/dklopfenstein/biocode/blob/master/PyDkBio/UCSC/CytoBandBase.py (Accessed [NN Month 20NN])

import sys
import re
import collections as cx
import numpy as np

__author__  = 'DV Klopfenstein'
__version__ = '2.0'
__copyright__ = "Copyright 2014-2015, DV Klopfenstein. All rights reserved."
__license__ = "GPL"
__maintainer__ = "DV Klopfenstein"

class CytoBandBase:
  """Python Interface to Species-Independent UCSC cytoBandIdeo.txt information."""

  flds_rpt_orgn = ['iChr', 'sChr', 'len_chr', 'len_adj', 'perc_chr', 'perc_adjDchr']
  NtOrgnRpt = cx.namedtuple("NtOrgnRpt", " ".join(flds_rpt_orgn))

  def __init__(self, data):
    """Initialize variables using data downloaded from a UCSC Cytoband file."""
    self.log = sys.stdout
    # Species w/version of build
    self.species = data['species']
    # Number of Chromosomes for this species
    self.num_chr = data['num_chr']
    # Index to Chromosome Name
    self.chr_i2s = data['chr_i2s']
    # Chromosome name (and synonyms) to index
    self.chr_s2i = data['chr_s2i']
    # Length of each Chromosome
    self.lengths = data['lengths']
    # Data
    self.centromeres = data['centromeres']
    self.gvars    = data['gvars']
    self.stalks   = data['stalks']
    self.map2info = data['map2info']
    self.coarse   = data['coarse']
    self.chr_plt  = data['chr_legend'] # Location for legend in genome plots

  def get_summary_iChr2orgninfo(self):
    """Collect summary chr data: chr length, adjusted length, etc."""
    summary_iChr2orgninfo = {}
    for iChr in range(self.num_chr):
      sChr = self.get_sChr(iChr)
      len_chr = self.get_len(iChr)
      len_adj = self.get_len_adj(iChr) # length minus gene-poor areas
      perc_chr = 100.0*len_chr/self.get_len_max()
      perc_adjDchr = 100.0*len_adj/len_chr
      summary_iChr2orgninfo[iChr] = self.NtOrgnRpt(iChr, sChr, len_chr, len_adj, perc_chr, perc_adjDchr)
    return summary_iChr2orgninfo

  def isChr(self, sChr):
    """Returns True if the name of the chromosome is recognized."""
    return True if sChr.strip() in self.chr_s2i else False

  def getCytobandRange_ChrAB(self, cab, ret_max=None, shorten=True):
    return self.getCytobandRange(cab.schr, cab.start_bp, cab.stop_bp, ret_max, shorten)

  def getCytobandRange(self, sChr, start, end, ret_max=None, shorten=True):
    iChr = self.get_iChr(sChr)
    bp0 = self.get_map_loc(iChr, start, ret_max)
    bpN = self.get_map_loc(iChr, end,   ret_max)
    return self._get_CytobandRange(sChr, bp0, bpN, shorten)

  def _get_CytobandRange(self, sChr, bp0, bpN, shorten):
    """Shortern the print of the range if possible."""
    # No shortening; This is a single cytomap location, not a range.
    if bp0 == bpN: 
      if sChr != bp0:
        return ''.join([sChr, bp0])
      else:
        return sChr
    if shorten:
      #print "CHR({}) BP0({}) BPN({})".format(sChr, bp0, bpN)
      pq_0, coarse_0, detailed_0 = self.split_cytomap(bp0)
      pq_N, coarse_N, detailed_N = self.split_cytomap(bpN)
      # Fly genome case on 2R: None 41B3 None -> None 41C1 None
      if (pq_0 is None and coarse_0 is not None and detailed_0 is None) and \
         (pq_N is None and coarse_N is not None and detailed_N is None):
        return ''.join([sChr, ':', coarse_0, '-', coarse_N])
      # No shortening; Cytomap ends are on different chromosome arms
      if pq_0 is not None and pq_N is not None and pq_0 != pq_N: 
        return ''.join([ sChr, bp0, '-', bpN ])
      # Shorten 'pq' only; coarse regions are different
      if coarse_0 != coarse_N:
        return ''.join([ sChr, pq_0, bp0[1:], '-', bpN[1:]])
      # Shorten 'pq' and 'coarse':
      return ''.join([ sChr, pq_0, coarse_0, '.', detailed_0, '-', detailed_N ])
    else:
      return ''.join([sChr, bp0, '-', bpN])

  def split_cytomap(self, pRA_rb):
    """Splits cytomap into "p or q", coarse "Region A", and detailed "region b"."""
    if pRA_rb:
      pq = None
      word = pRA_rb
      arm  = word[0]
      if arm == 'p' or arm == 'q':
        pq = arm
        word = word[1:]
      if "." not in word:
        return pq, word, None
      else:
        fields = word.split(r".")
        if len(fields) == 2:
          return pq, fields[0], fields[1]
      return (pq, None, None)
    return (None, "", None)
    

  def getCytoband(self, sChr, bp, ret_max=None):
    iChr = self.get_iChr(sChr)
    return ''.join([sChr, self.get_map_loc(iChr, bp, ret_max)])

  def get_sChr_list(self):
    """Return dictionary with list index as the key and value as commonly known Chromosome name."""
    return [sChr for sChr in self.chr_i2s]

  def get_gvarL(self, chr_idx):
    """Return the length of the gvar areas on a chromosome, if they exist."""
    if self.gvars[chr_idx] is not None:
      L = 0
      for E in self.gvars[chr_idx]:
        L += E[2] # Add lengths of each gvar on a chromosome
      return L # return total gvar length
    else:
      return None

  def get_stalkL(self, chr_idx):
    """Return the length of the stalk areas on a chromosome, if they exist."""
    if self.stalks[chr_idx] is not None:
      L = 0
      for E in self.stalks[chr_idx]:
        L += E[2] # Add lengths of each gvar on a chromosome
      return L # return total gvar length
    else:
      return None

  def get_lens(self): 
    """Return a list containing the length of each chromosome."""
    return self.lengths

  def get_len(self, chr_idx):
    """Get the length of one particular chromosome."""
    if chr_idx < self.num_chr:
      return self.lengths[chr_idx]

  def get_len_adj(self, chr_idx):
    """Get the length of one particular chromosome minus centromere/stalk/gvar if exists."""
    len_chr = self.get_len(chr_idx)
    len_adj = self.adj_len(len_chr, chr_idx, self.get_gvarL)
    len_adj = self.adj_len(len_adj, chr_idx, self.get_stalkL)
    len_adj = self.adj_len(len_adj, chr_idx, self.cen_get_len)
    return len_adj

  def adj_len(self, len_chr, chr_idx, get_genepoor_len):
    """Subtract gene-poor areas from overall chromosome length."""
    len_genepoor = get_genepoor_len(chr_idx)
    if len_genepoor is not None:
      return len_chr - len_genepoor
    return len_chr

  def get_len_max(self):
    """Get the length of the largest Chromosome in the genome."""
    return max(L for L in self.lengths)

  def get_len_genome(self):
    """Returns the sum of the length of all chromosomes."""
    return sum(self.lengths)
    
  def get_iChr(self, sChr):
    """Given the commonly known chromosome name, return the chr list index used by this class."""
    if isinstance(sChr, str):
      schr = sChr.strip()
      if schr in self.chr_s2i: return self.chr_s2i[schr]
      schr = re.sub("chr", "", schr)
      if schr in self.chr_s2i: return self.chr_s2i[schr]
      return None
    else:
      raise Exception("UNEXPECTED sChr({}) VALUE in get_iChr".format(sChr))

  def get_iChr_from_maploc(self, maploc):
    """Given the commonly known chromosome name, return the chr list index used by this class."""
    M = re.search(r'(\S+)(p|q)', maploc)
    return self.get_iChr(M.group(1) if M else maploc)

  def get_max_bp(self, chr_idx):
    """Returns the largest base pair in the UCSC file for a given chromosome.""" 
    return self.get_len(chr_idx)
    
  def get_map_loc(self, iChr, bp, ret_max=None):
    """Given a chromosome and a base pair value, return a cyto map location.
      
    Return the cytomap for the bp location if it is found
    If bp > max_bp for that chromosome:
      Return cytomap at the highest bp value if the user specifies ret_max=True
      Return cytomap at the highest bp value if the bp is within a user-specified range
      Otherwise return None
    If bp < max_bp and the map was not found, raise an exception
    """
    # Search for bp in UCSC's data and return the UCSC cytomap
    info = self.map2info[iChr]
    for cmap in info:
      elem = info[cmap]
      if bp >= elem[0] and bp <= elem[1]:
        return cmap

    max_bp = self.get_max_bp(iChr)
    # If the bp > max_bp for that chromosome
    if ret_max is not None and bp > max_bp:
      # Return cytomap at the highest bp value if the user specifies ret_max=True
      if ret_max is True:
        return next(reversed(self.map2info[iChr])) 
      # Return cytomap at the highest bp value if the bp is within a user-specified range
      elif isinstance(int, ret_max) and bp <= (max_bp + ret_max):
        return next(reversed(self.map2info[iChr]))
      # Else return None
      else:
        return None
    else:
      # return sChr if there is no cytomap found for the user's 'bp' value
      return self.get_sChr(iChr)
    # Raise an Exception if there is no cytomap found for the user's 'bp' value
    #  raise Exception('*FATAL: retmax({R}) get_map_loc(chr({CHR}), bp({BP:,})): NO map VALUE AVAILABLE; MAX_BP({MBP:,}) DELTA({D:,})'.format(
    #    R=ret_max, CHR=self.get_sChr(iChr), BP=bp, MBP=self.get_max_bp(iChr), D = bp - self.get_max_bp(iChr) ))


  def get_sChr(self, chr_idx):
    """Given a chromosome list index, return the commonly known chromosome name."""
    if chr_idx is not None and chr_idx < self.num_chr:
      return self.chr_i2s[chr_idx]
    raise Exception("\n**\n** FATAL: CANNOT DETERMINE CHR NAME WITH ({})\n**\n".format(chr_idx))

  def cen_get_len(self, iChr): 
    """Return the length of the centromere, given a chromosome list index."""
    if iChr < self.num_chr and  \
      self.centromeres[iChr] is not None  and \
      self.centromeres[iChr]['p'] is not None and \
      self.centromeres[iChr]['q'] is not None:
      return self.centromeres[iChr]['p'][1] - self.centromeres[iChr]['q'][0]
    return None

  def cen_get_start(self, iChr): 
    """Return the start base pair of the centromere, given a chromosome list index."""
    if iChr < self.num_chr and \
      self.centromeres[iChr] is not None and \
      self.centromeres[iChr]['q'] is not None:
      return self.centromeres[iChr]['q'][0]
    return None

  def cen_get_end(self, iChr): 
    """Return the end base pair of the centromere, given a chromosome list index."""
    if iChr < self.num_chr and \
      self.centromeres[iChr] is not None and \
      self.centromeres[iChr]['q'] is not None: 
      return self.centromeres[iChr]['p'][1]
    return None

  def get_centromere_midpoint(self, iChr):
    """Return the center base pair of the centromere, given a chromosome list index."""
    if iChr < self.num_chr and \
      self.centromeres[iChr] is not None and \
      self.centromeres[iChr]['q'] is not None: 
      return self.centromeres[iChr]['q'][1]
    return None

  def get_centromere_midpoints(self):
    """Return the center base pair of all centromeres in the genome."""
    # [ unicode(x.strip()) if x is not None else '' for x in row ]
    return [ E['q'][1] if E is not None else None for E in self.centromeres]

  def get_prtdata_cytoband(self, Keys):
    """Get cytoband data in a format amenable to plotting broken bars."""
    range_data = {}
    for iChr, chr_data in enumerate(self.map2info):
      for mapname in chr_data:
        D = chr_data[mapname]
        Start = D[0]
        Len   = D[1] - D[0]
        Key   = D[2]
        if Key not in range_data:
          range_data[Key] = cx.defaultdict(list)
        if Key in Keys: 
          range_data[Key][iChr].append([ Start, Len, mapname])
        else:
          raise Exception('\n**\n** FATAL: NO COLOR ASSIGNED TO MAP TYPE: "{}"\n**\n'.format(Key))
    return cx.OrderedDict(sorted(range_data.items()))

  def wr_genome_lens(self, pre=""):
    """Write bedtools genome file containing lengths of all chromosomes."""
    fout_genome = "{SPECIES}.genome".format(SPECIES=self.species)
    with open(fout_genome, 'w') as prt:
      for ichr in range(self.num_chr):
        prt.write("{PRE}{CHR}\t{CHR_LEN}\n".format(
          PRE=pre, CHR=self.get_sChr(ichr), CHR_LEN=self.get_len(ichr)))
      sys.stdout.write("  WROTE bedtools GENOME LENGTHS FILE: {FOUT}\n".format(FOUT=fout_genome))
    return fout_genome
  

 
