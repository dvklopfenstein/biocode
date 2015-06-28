#!/usr/bin/env python

import sys

# Use beta version for testing
sys.path.insert(0, '../../')
import pydvkbiology.kaplanmeier.KaplanMeier as KM

def run():
  # Statistical Reasoning for Public Health 1: Estimation, Inference, & Interpretation
  # by John McGready, PhD, MS
  #
  # Lecture 5C: Part1 Time to Event Data: Graphical Summarization: Kaplan-Meier
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
  data = [2, -3, 6, 6, -7, 10, -15, 15, 16, 27, 30, 32]
  km = KM.KaplanMeier(data)
  print km.get_cumulative_survival()
         

if __name__ == '__main__':
  run()
