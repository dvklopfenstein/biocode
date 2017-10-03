"""From colormaps, get discrete colors."""

# Copyright (C) 2014-2015 DV Klopfenstein.  All rights reserved.
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
__copyright__ = "Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved."
__license__ = "GPL"

# Helpful pages:
#   http://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
#
#   Create own colormap using matplotlig and plot color scale
#     http://stackoverflow.com/questions/16834861/

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

class MplColorHelper(object):
    """From colormaps, get discrete colors."""

    def __init__(self, cmap_name, start_val=0, stop_val=5):
        self.cmap_name = cmap_name
        self.cmap = plt.get_cmap(cmap_name)
        self.start_val = start_val
        self.stop_val = stop_val
        self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
        self.scalarmap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

    def get_rgb(self, val):
        """Return RGB tuple."""
        return self.scalarmap.to_rgba(val)

    def get_hexstr(self, val):
        """Given a value, return a hex string representing the color."""
        red, grn, blu, _ = self.get_rgb(val)
        return '#{:02x}{:02x}{:02x}'.format(int(red*255), int(grn*255), int(blu*255))

    def get_color_list(self):
        """Return colors as a list of hex strings."""
        return [self.get_hexstr(i) for i in range(self.start_val, self.stop_val+1)]

    def min_hexstr(self):
        """Return smallest hex string."""
        return self.get_hexstr(self.start_val)

    def max_hexstr(self):
        """Return largest hex string."""
        return self.get_hexstr(self.stop_val)

    def get_color_desc(self):
        """Get list of [(color0, description0), (color1, description1), ..."""
        color_desc = []
        for color_num in range(self.start_val, self.stop_val+1):
            col_hexstr = self.get_hexstr(color_num)
            color_desc.append((col_hexstr, col_hexstr))
        return color_desc


# Copyright (C) 2014-2017 DV Klopfenstein. All rights reserved.
