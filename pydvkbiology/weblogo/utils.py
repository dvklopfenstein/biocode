"""Utilities for using WebLogo from Python."""

import os
import sys

import weblogolib as WL
import corebio as CB
from corebio.seq import Seq, SeqList, Alphabet

class BcSeqList(SeqList):
  """Accepts list of sequences from a script, rather from a file (i.e. fasta file)."""

  def __init__(self, seq_list, alphabet, name=None, description=None):
    abc_obj = Alphabet(alphabet)
    # Convert user list of characters into list of corebio.seq Seq objects
    seqs = [Seq(seq_line, abc_obj) for seq_line in seq_list]
    super(SeqList, self).__init__(seqs)
    self.alphabet = abc_obj
    self.name = name
    self.description = description
   
 

def wr_image(fout_image, logo_data, logo_options):
  """Wrapper around weblogo's formatter wr_imager."""
  basename, ext = os.path.splitext(fout_image)
  ext = ext[1:] # strip '.' from file extension
  # WebLogo formatters are used to print the WebLogo image
  if ext in WL.formatters:
    fmt = WL.LogoFormat(logo_data, logo_options)
    pnglogo_data = WL.formatters[ext](logo_data, fmt)
    # Write png, eps, pdf, svg, logodata, png_print, jpg, etc...
    with open(fout_image, 'w') as pngstrm:
      pngstrm.write(pnglogo_data)
      sys.stdout.write("  WROTE: {}\n".format(fout_image))
  else:
    # User did not use one of the WebLogo image formatters
    raise Exception("BAD EXT({}). CHOOSE FROM: {}\n".format(
      ext, ' '.join(WL.formatters.keys())))

