#!/usr/bin/env python3
"""Print hex digits for seaborn colors"""

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn

# Print the HEX codes of seaborn colors
pal_hls = seaborn.hls_palette(12, l=.3, s=.8).as_hex()

import seaborn as sns
num_shades = 8
sns.palplot(sns.cubehelix_palette(num_shades))
plt.savefig('seaborn.png')


print(pal_hls)
