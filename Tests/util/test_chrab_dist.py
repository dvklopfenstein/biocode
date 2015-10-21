#!/usr/bin/env python

import sys
import os

# Use beta version of pydvkbiology
sys.path.insert(0, '{GIT}/biocode'.format(GIT=os.environ['GIT']))
from pydvkbiology.util.chr_ab import ChrAB


def test_dist(prt=sys.stdout):
  assert ChrAB("1", 0,  5).get_dist(ChrAB("1", 6, 10)) == 1
  assert ChrAB("1", 6, 10).get_dist(ChrAB("1", 0,  5)) == 1
  assert ChrAB("1", 9,  7).get_dist(ChrAB("1", 0,  1)) == 6
  assert ChrAB("1", 7,  7).get_dist(ChrAB("1", 1,  1)) == 6
  assert ChrAB("2", 9,  7).get_dist(ChrAB("1", 0,  1)) is None # Different chromosomes
  assert ChrAB("1", 0,  6).get_dist(ChrAB("1", 4, 10)) == 0 # Parital overlap
  assert ChrAB("1", 4, 10).get_dist(ChrAB("1", 0,  6)) == 0 # Partial overlap
  assert ChrAB("1", 5,  5).get_dist(ChrAB("1", 5,  5)) == 0 # Complete overlap L=1
  assert ChrAB("1", 1,  5).get_dist(ChrAB("1", 1,  5)) == 0 # Complete overlap
  assert ChrAB("1", 7,  5).get_dist(ChrAB("1", 1,  5)) == 0 # 'Kissing'
  assert ChrAB("1", 7,  5).get_dist(ChrAB("1", 5,  5)) == 0 # Overlap w/L=1 gene
  

if __name__ == '__main__':
  test_dist()
