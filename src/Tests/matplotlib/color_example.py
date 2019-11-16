#!/usr/bin/env python
"""Example using MplColorHelper."""

# Copyright (C) 2014-2015 DV Klopfenstein.  All rights reserved.

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pydvkbiology.matplotlib.ColorObj import MplColorHelper
import numpy as np


def main():
    """ Plots all the named colors in matplotlib.

        From: http://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
    """
    import math
    import matplotlib.patches as patches
    import matplotlib.colors as colors

    fig = plt.figure()
    axis = fig.add_subplot(111)

    ratio = 1.0 / 3.0
    count = math.ceil(math.sqrt(len(colors.cnames)))
    x_count = count * ratio
    y_count = count / ratio
    xval = 0
    yval = 0
    width = 1 / x_count
    height = 1 / y_count

    for color_name in colors.cnames:
        pos = (xval / x_count, yval / y_count)
        axis.add_patch(patches.Rectangle(pos, width, height, color=color_name))
        axis.annotate(color_name, xy=pos)
        if yval >= y_count-1:
            xval += 1
            yval = 0
        else:
            yval += 1

    plt.show()
    plt.savefig('color_example.png')


if __name__ == '__main__':
    main()

# Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved.
