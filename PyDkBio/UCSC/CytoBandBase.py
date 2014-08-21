#!/usr/bin/env python

# CytoBandBase.py stores CytoBandIdeo data downloaded from UCSC and
# Allows easy access to the CytoBand information from a Python script
# in a species-independent manner.
# Copyright (C) 2014 DV Klopfenstein;
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
# Drexel University., hereby disclaims all copyright interest in the program
# `CytoBandBase' written by DV Klopfenstein.
#
# Aydin Tozeren, Distinguished Professor
# August 2014


# To cite this script, please use: 
#
# Klopfenstein D.V. (2014) Storage and Python Access to UCSC's Cytoband Data In A Species-Independent Manner (Version 2.0) [Computer program]. Available at https://github.com/dklopfenstein/biocode/blob/master/PyDkBio/UCSC/CytoBandBase.py (Accessed [NN Month 20NN])

__version__ = '2.0'

class CytoBandBase:
  """Python Interface to Species-Independent UCSC cytoBandIdeo.txt information."""

  def __init__(self, data):
    """Initialize variables using data downloaded from a UCSC Cytoband file."""
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
    self.gvars   = data['gvars']
    self.stalks  = data['stalks']

  def get_sChr_list(self):
    """Return dictionary with list index as the key and value as commonly known Chromosome name."""
    return [sChr for sChr in self.chr_i2s]

  def get_gvarL(self, idx):
    """Return the length of the gvar areas on a chromosome, if they exist."""
    if self.gvars[idx] is not None:
      L = 0
      for E in self.gvars[idx]:
        L += E[2] # Add lengths of each gvar on a chromosome
      return L # return total gvar length
    else:
      return None

  def get_stalkL(self, idx):
    """Return the length of the stalk areas on a chromosome, if they exist."""
    if self.stalks[idx] is not None:
      L = 0
      for E in self.stalks[idx]:
        L += E[2] # Add lengths of each gvar on a chromosome
      return L # return total gvar length
    else:
      return None

  def get_lens(self, idx): 
    """Return a list containing the length of each chromosome."""
    return self.lengths

  def get_len(self, idx):
    """Get the length of one particular chromosome."""
    if idx < self.num_chr:
      return self.lengths[idx]
    
  def get_iChr(self, sChr):
    """Given the commonly known chromosome name, return the chr list index used by this class."""
    if sChr in self.chr_s2i:
      return self.chr_s2i[sChr]
    return None

  def get_sChr(self, idx):
    """Given a chromosome list index, return the commonly known chromosome name."""
    if idx is not None and idx < self.num_chr:
      return self.chr_i2s[idx]
    raise Exception("\n**\n** FATAL: CANNOT DETERMINE CHR NAME WITH ({})\n**\n".format(idx))

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


 
