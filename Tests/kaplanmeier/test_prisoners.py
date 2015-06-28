#!/usr/bin/env python

import pydvkbiology.kaplanmeier.KaplanMeier as KM

def run():
  # Statistical Reasoning for Public Health 1: Estimation, Inference, & Interpretation
  # by John McGready, PhD, MS
  #
  # Homework 2B
  #
  # A pilot study was designed to evaluate the potential
  # efficacy of a program designed to reduce prison recidivism
  # amongst inmates who have a documented long-term history of
  # drug and/or alcohol problems.  A sample of 11 prisoners was
  # followed for up to 24 months after their most recent release
  # from prison. Six of the inmates returned to prison at 3, 7
  # 9, 11, 14 and 21 months respectively. Five of the inmates
  # had not returned to prison as of the last time they were
  # last contacted which was at 4, 8, 16, 24, and 24 months
  # respectively.
  ret = [3, 7, 9, 11, 14, 21]
  cen = [-4, -8, -16, -24, -24]
  km = KM.KaplanMeier(ret + cen)
  # 3, -4, 7, -8, 9, 11, 14, -16, 21, -24, -24
  km.prt_data_sorted()
         

if __name__ == '__main__':
  run()
