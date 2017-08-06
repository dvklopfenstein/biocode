#!/usr/bin/env python
"""Create scatter plot with hombre-style fade using MplColorHelper."""

# Copyright (C) 2014-2015 DV Klopfenstein.  All rights reserved.

__author__ = 'DV Klopfenstein'
__copyright__ = "Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved."
__license__ = "GPL"

import matplotlib.pyplot as plt
from pydvkbiology.matplotlib.ColorObj import MplColorHelper
import numpy as np


def main():
    """Create scatter plot with hombre-style fade using MplColorHelper."""
    _, axis = plt.subplots(1, 1, figsize=(6, 6))

    num_vals = 20
    #pylint: disable=no-member
    xval = np.random.uniform(0, num_vals, size=3*num_vals)
    yval = np.random.uniform(0, num_vals, size=3*num_vals)

    # define the color chart between 2 and 10 using the 'autumn_r' colormap, so
    #   yval <= 2  is yellow
    #   yval >= 10 is red
    #   2 < yval < 10 is between from yellow to red, according to its value
    objcol = MplColorHelper('autumn_r', 5, 15)

    axis.scatter(xval, yval, s=200, c=objcol.get_rgb(yval))
    axis.set_title('Well defined discrete colors')
    plt.show()


if __name__ == '__main__':
    main()

# Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved.
