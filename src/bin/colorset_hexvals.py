#!/usr/bin/env python
"""Example using MplColorHelper."""

# Copyright (C) 2014-2017 DV Klopfenstein.  All rights reserved.

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pydvkbiology.matplotlib.ColorObj import MplColorHelper
import numpy as np


#def run(palette='Set1', num_vals=10):
def run(palette='hsv', num_vals=12):
    """Creating hexvalues for discrete colors using a colormap."""
    fout_png = 'colors_{P}_{N}.png'.format(P=palette, N=num_vals)
    _, axis = plt.subplots(1, 1, figsize=(6, 6))
    colobj = MplColorHelper(palette, 0, num_vals-1)
    colors = [colobj.get_hexstr(yval) for yval in range(num_vals)]
    plt_color_text(colors)
    for idx, color in enumerate(reversed(colors)):
        print('{N:2} {COLOR}'.format(N=idx, COLOR=color))
    axis.set_title('{N} Discrete Colors from {MAP}'.format(N=num_vals, MAP=palette))
    plt.show()
    plt.savefig(fout_png)
    print('  WROTE: {PNG}'.format(PNG=fout_png))

def plt_color_text(colors):
    """Plot a block of color and label it with text"""
    num_vals = len(colors)
    xvals = [10]*num_vals
    yvals = range(num_vals)
    for idx, (xval, yval, color) in enumerate(zip(xvals, yvals, colors)):
        plt.scatter(xval, yval, s=1000, marker='s', color=color)
        plt.text(xval+.004, yval, color, fontsize=20, va='center')

def cli():
    """Command-line interface for creating hexvalues for discrete colors from a colormap."""
    palette = "Set1"
    num_vals = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            num_vals = int(arg)
        else:
            palette = arg
    run(palette, num_vals)

def main():
    """For testing specific color combinations"""
    fout_png = 'color0.png'
    _, axis = plt.subplots(1, 1, figsize=(6, 6))
    colors = [
        '#0032ff',
        '#00ebff',
        '#fdfe02',
        '#ff0000',
        '#8500ff',
    ]
    plt_color_text(colors)
    plt.savefig(fout_png)


if __name__ == '__main__':
    cli()
    #main()

# Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved.
