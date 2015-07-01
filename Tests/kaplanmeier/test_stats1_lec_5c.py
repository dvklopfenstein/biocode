#!/usr/bin/env python

import sys

# Use beta version for testing
sys.path.insert(0, '../../')
import pydvkbiology.kaplanmeier.KaplanMeier as KM

def run():
  # Statistical Reasoning for Public Health 1: Estimation, Inference, & Interpretation
  # by John McGready, PhD, MS
  #
  # Lecture 5C: Part 1 Time to Event Data: Graphical Summarization: Kaplan-Meier (15:41)
  #
  # respectively.
  #
  #   2 .92 
  #   6 .74 
  #  10 .64
  #  15 .52
  #  16 .39
  #  27 .26
  #  30 .13
  #  32 0
  #
  #  2: Subject was in study and had event at 2 months
  # -3: Subject was in study and dropped out at 3 months
  data = [2, -3, 6, 6, -7, 10, -15, 15, 16, 27, 30, 32] 
  print data
  km = KM.KaplanMeier(data)
  km.get_cumulative_survival(sys.stdout)
         

if __name__ == '__main__':
  run()
