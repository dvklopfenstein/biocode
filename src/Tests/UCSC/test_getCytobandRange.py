#!/usr/bin/env python

from PyBiocode.UCSC.CytoBandHg38 import *
import sys

def chk_results(sChr, bp0, bp1, actual, expected):
  orig = '{C}{BP0}-{C}{BP1}'.format(C=sChr, BP0=bp0, BP1=bp1)
  if actual == expected:
    sys.stdout.write("MATCH: ORIG: {:15} ACTUAL={:15} EXPECTED={:15}\n".format(
      orig, actual, expected))
    return
  sys.stdout.write(
    "FATAL MISMATCH: ORIG: {:15} ACTUAL={:15} EXPECTED={:15}\n".format(
      orig, actual, expected))

def test():
  data = [
    # Actual Data In            Expected Data Out
    ( "5", "q35.2",  "q35.3" , "5q35.2-3"  ),
    ( "6", "p21.33", "p21.31", "6p21.33-31"),
    ( "6", "p22.1",  "p21.33", "6p22.1-21.33"),
    ( "3", "p21.31", "p21.2" , "3p21.31-2" ),
    ("14", "q11.2",  "q12"   , "14q11.2-12"),
    ( "X", "qA2",    "qA3.1" , "XqA2-A3.1"),
    ( "X", "qA3.1",  "qA2"   , "XqA3.1-A2"),
  ]
  orgn = CytoBand()
  for sChr, bp0, bp1, expected in data:
    actual = orgn._get_CytobandRange(sChr, bp0, bp1, shorten=True)
    chk_results(sChr, bp0, bp1, actual, expected)
  

if __name__ == '__main__':
    test()

