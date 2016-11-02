#!/usr/bin/env python
"""Used to test ChrAB's get_rng method."""

import sys
import os

# Use beta version of pydvkbiology
sys.path.insert(0, '{GIT}/biocode'.format(GIT=os.environ['GIT']))
from pydvkbiology.util.chr_ab import ChrAB

def test_get_rng(prt=sys.stdout):
  """Various tests for ChrAB's get_rng method."""
  assert ChrAB("1", 10, 20).get_rng( 5   ) == [ 5, 25]
  assert ChrAB("1", 10, 20).get_rng( 5, 3) == [ 5, 23]
  assert ChrAB("1", 10, 20).get_rng(10, 3) == [ 0, 23]
  assert ChrAB("1", 10, 20).get_rng(11   ) == [ 0, 31]

if __name__ == '__main__':
  test_get_rng()
