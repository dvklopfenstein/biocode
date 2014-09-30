#!/usr/bin/env python

# Copyright (C) 2014  D Klopfenstein.  All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

__author__ = 'DV Klopfenstein'

# Helpful pages:
#   http://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

class MplColorHelper:

  def __init__(self, cmap_name, start_val, stop_val):
    self.cmap_name = cmap_name
    self.cmap = plt.get_cmap(cmap_name)
    self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
    self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

  def get_rgb(self, val):
    return self.scalarMap.to_rgba(val)
    




def MplColorHelper_example1():
  import numpy as np
  # setup the plot
  fig, ax = plt.subplots(1,1, figsize=(6,6))

  # define the data between 0 and 20
  NUM_VALS = 20
  x = np.random.uniform(0, NUM_VALS, size=3*NUM_VALS)
  y = np.random.uniform(0, NUM_VALS, size=3*NUM_VALS)

  # define the color chart between 2 and 10 using the 'autumn_r' colormap, so
  #   y <= 2  is yellow
  #   y >= 10 is red
  #   2 < y < 10 is between from yellow to red, according to its value
  COL = MplColorHelper('autumn_r', 5, 15)

  scat = ax.scatter(x,y,s=200, c=COL.get_rgb(y))
  ax.set_title('Well defined discrete colors')
  plt.show()


if __name__ == '__main__':
  MplColorHelper_example1()
 
