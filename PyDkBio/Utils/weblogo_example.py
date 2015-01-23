#!/usr/bin/env python

#import weblogolib as WL
from weblogolib import *
import re

def ex1(filein='cap_dna.fa'):
  """http://weblogo.threeplusone.com/manual.html """
  fin = open(filein)
  seqs = read_seq_data(fin)
  print seqs
  data = LogoData.from_seqs(seqs)
  print data
  options = LogoOptions()
  print options
  options.title = "A Logo Title"
  fmt = LogoFormat(data, options)
  print fmt
  fout = re.sub('.fa', '.png', filein)
  print fout
  png = png_formatter( data, fmt)
  FOUT = open(fout, 'w')
  FOUT.write(png)
  FOUT.close()



if __name__ == '__main__':
  ex1()
