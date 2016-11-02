"""Tracks official Symbol and alternate names, aliases, and other designations."""

__author__  = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2014-2015 DV Klopfenstein. All rights reserved."
__license__ = "GPL"

class SymAlts(object):
  """Stores and prints Symbol and alternate designations."""

  def __init__(self, Symbol, alts):
    self.Symbol = Symbol  # 'Official' Symbol
    self.alts = set(alts) # set of alternate values

  def __str__(self):
    """Given NtSymHits, return a string with gene Symbol AND alternate names."""
    if self.alts:
      alts = self.alts.difference(set([self.Symbol]))
      if alts:
        return "{}({})".format(self.Symbol, ', '.join(alts))
    return self.Symbol

  def __repr__(self):
    return "SymAlts('{Symbol}', {alts})".format(
      Symbol=self.Symbol, alts=self.alts)

