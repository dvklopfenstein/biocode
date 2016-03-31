#!/usr/bin/env python
"""Make your own colormaps."""

# This example is from:
# http://stackoverflow.com/questions/16834861/create-own-colormap-using-matplotlib-and-plot-color-scale

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    for E in seq: print "SEQ", E
    for E in cdict.items(): print "CDT", E
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

def main(N=1000):
    c = mcolors.ColorConverter().to_rgb
    rvb = make_colormap([
      c('red'), c('violet'), 0.33,
      c('violet'), c('blue'), 0.66,
      c('blue')])
    colors   = np.random.uniform(low=-2, high=2,  size=(N,))
    # Generate N "[x, y]"s where x and y values vary from 0...10: [[x0, y0], [x1, y1], ...
    XYs = np.random.uniform(low=0,  high=10, size=(N, 2)) 
    Xs, Ys = zip(*XYs)
    # Create Scatter Plot
    plt.scatter(Xs, Ys, c=colors, cmap=rvb)
    plt.colorbar()
    plt.show()

if __name__ == '__main__':
    main()
  


