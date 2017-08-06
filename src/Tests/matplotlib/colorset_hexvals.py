#!/usr/bin/env python
"""Example using MplColorHelper."""

# Copyright (C) 2014-2017 DV Klopfenstein.  All rights reserved.

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import sys
import matplotlib.pyplot as plt
from pydvkbiology.matplotlib.ColorObj import MplColorHelper
import numpy as np


def run(palette='Set1', num_vals=10):
    """Creating hexvalues for discrete colors using a colormap."""
    _, axis = plt.subplots(1, 1, figsize=(6, 6))
    xvals = [10]*num_vals
    yvals = range(num_vals)
    colobj = MplColorHelper(palette, 0, num_vals-1)
    colors = [colobj.get_hexstr(yval) for yval in yvals]
    for xval, yval, color in zip(xvals, yvals, colors):
        plt.scatter(xval, yval, s=1000, color=color)
        plt.text(xval+.004, yval, color, fontsize=20, va='center')
    axis.set_title('{N} Discrete Colors from {MAP}'.format(N=num_vals, MAP=palette))
    plt.show()


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


if __name__ == '__main__':
    cli()

# Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved.
