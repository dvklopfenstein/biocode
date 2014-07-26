#!/usr/bin/env python

# Copyright (C) 2014 DV Klopfenstein
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# dvklopfenstein@gmail.com


import sys
import os
import re
import collections as cx
from string import Template
import chrInfo
import cytoBand
import get_NCBI_genes_data as din

def main():
  args  = getArgs()
  [ data, geneCnt ] = din.get_items_w_start_end(args['fin'])
  wr_plot(args['subj'], data, geneCnt)

def wr_plot(subj, chrsD, geneCnt):
  yProp = { 'init':20, 'delta':24, 'BarHeight':14, 
    'colorKey':cx.defaultdict(str)}
  yProp['label'] = None
  #FF0000 Red
  #FF6600 Dark Orange
  #FF9900 Light Orange
  #FFFF00 Yellow
  yProp['colorKey']['green']   = 'Disease Clusters'

  cHS1 = '#ff0000' # red
  cHS2 = '#ff9900' # Orange
  cHS3 = '#ffff00' # Yellow
  #cHS1 = '#ff0000' # red
  #cHS2 = '#3e4957' # purple
  #cHS3 = '#003366' # blue
  yProp['colorKey'][cHS1]  = 'Super-Hotspot'
  yProp['HS#1']   = cHS1
  yProp['colorKey'][cHS2]  = 'Hotspot Medium'
  yProp['HS#2']   = cHS2
  yProp['colorKey'][cHS3]  = 'Hotspot Lite'
  yProp['HS#3']   = cHS3
  
  fout, png = get_fout_png( subj )
  FOUT = open(fout,'w')
  FOUT.write('%s'%("""#!/usr/bin/python
import matplotlib.pyplot as plt
import sys
import operator

noshow = None
for arg in sys.argv[1:]:
  if arg == 'noshow':
    noshow = True

fig, ax = plt.subplots()
"""))

  ypos = get_ypos(yProp['init'], yProp['delta'] )

  # Print the genes using a broken_bar item for each gene
  prt_broken_barh(FOUT, chrsD, ypos, 'black', getYoffset_BarBottom(yProp), yProp['BarHeight'], 0.70)

  FOUT.write('\n# SET Y TICKS\n')
  FOUT.write('ax.set_yticks(%s)\n'%(get_yticks(chrsD,yProp))) #[15,25]
  FOUT.write('ax.set_yticklabels(%s)\n'%(get_yticklabels(chrsD)))

  TITLE = setTitle( FOUT, subj, geneCnt )
  yLinOffset = getYoffset_middle(yProp)
  yTxtOffset = getYoffset_BarTop(yProp)+1

  if yProp['label']:
    doLegend(FOUT)

  prtStopArrows( FOUT,chrsD,ypos,yProp,'cyan')
  setXaxisLabels( FOUT )
  FOUT.write('fig.set_size_inches(4,2)\n')
  FOUT.write("plt.savefig('{png}', bbox_inches=0, dpi=200)\n".format(png=png))
  FOUT.write('if not noshow:\n')
  FOUT.write('  plt.show()\n')
  FOUT.close(); print "  WROTE:", fout, TITLE
  os.chmod(fout, 0555)


def setTitle( FOUT, subj, geneCnt ):
  M = re.search(r'(\S+)distLT(\d+)', subj)
  TITLE = ' '.join( [ subj, str(geneCnt), 'Genes' ] )
  if M:
    TITLE = '%d %s Genes with Neighbors <= %s bp'%(geneCnt, M.group(1), M.group(2))
  FOUT.write("\nax.set_title('%s', fontsize=18)\n"%(TITLE))
  return TITLE


def setXaxisLabels( FOUT ):
  FOUT.write('%s'%("""
# SET THE X-AXIS LABELS FOR Mb
# Need to draw the canvas, otherwise the labels won't be positioned and we won't have values yet.
fig.canvas.draw()
# Divide the bps by 1,000,000 to get proper Mb numbers
labVal = [I/1000000 for I in ax.get_xticks()]
# Get the current x axis labels
labels = [item.get_text() for item in ax.get_xticklabels()]
# Replace the current x axis labels with the Mb values
for I,L in enumerate(labels): labels[I] = int(labVal[I])
ax.set_xticklabels(labels)

"""))


def doLegend(PRT):
  PRT.write("handles, labels = ax.get_legend_handles_labels()\n")
  PRT.write("# Sort by label\n")
  PRT.write("hl = reversed(sorted(zip(handles, labels), key=operator.itemgetter(1)))\n")
  PRT.write("handles2, labels2 = zip(*hl)\n")
  loc= 'best' 
  PRT.write("ax.legend(handles2, labels2, loc='%s')\n"%loc)

def getLabel(yProp, color):
  colorKey = yProp['colorKey']
  if color in colorKey and colorKey[color]:
    ret = ", label='%s'"%(colorKey[color])
    # Only print a color was on the legend once
    colorKey[color] = None 
    if not yProp['label']:
      yProp['label'] = True
    return ret
  return ''

def getYoffset_middle(yProp):    return  yProp['delta']/2
def getYoffset_BarBottom(yProp): return (yProp['delta'] - yProp['BarHeight'])/2
def getYoffset_BarTop(yProp):    return (yProp['delta'] + yProp['BarHeight'])/2
def getYmax(yProp,yNum):         return  yProp['init'] + yProp['delta']*yNum

def prt_genes_anno(FOUT,chrsD,ypos,ydelta):
  for Chr in chrsD: 
    FOUT.write('\n# chromosome %s (%d locations)\n'%(Chr,len(chrsD)))
    L = len(chrsD[Chr]) - 1 
    for i,pts in enumerate(chrsD[Chr]):
      FOUT.write("ax.annotate('%s', (%10s, %3s), fontsize=12, rotation=-45, horizontalalignment='right', verticalalignment='top', arrowprops=dict(facecolor='black'))\n"%
        (pts[2], pts[0], ypos[Chr]+ydelta))

# hatch: 
#  /   - diagonal hatching
#  \   - back diagonal
#  |   - vertical
#  -   - horizontal
#  +   - crossed
#  x   - crossed diagonal
#  o   - small circle
#  O   - large circle
#  .   - dots
#  *   - stars
def prt_broken_barh(FOUT,chrsD,ypos,color, y_offset, y_height, alpha=1.00):
  for iChr in chrsD: 
    sChr = chrInfo.chrIdx2txt(iChr)
    FOUT.write('\n# chromosome %s (%d locations)\nax.broken_barh([\n'%(sChr,len(chrsD)))
    L = len(chrsD[iChr]) - 1 
    for i,pts in enumerate(chrsD[iChr]):
      #FOUT.write('(%10s, %10s) '%(pts[0], pts[1]))  TBD 2014_0618
      FOUT.write('(%10s, %10s) '%(pts[0], 100)) # TBD 2014_0618
      if i<L:
        FOUT.write(', \n')
      else:
        FOUT.write("], (%d, %d), linewidths=1, edgecolors='k', facecolors='%s', alpha=%f)\n"%(
          ypos[sChr]+y_offset, y_height, color, alpha))


def prtStopArrows(FOUT,chrsD,ypos,yProp,color):
  endPos = chrInfo.getChrEnds()
  aLen = -10
  hWid = 20
  hLen = 5000000
  yOffset = getYoffset_middle(yProp)
  FOUT.write('\n# ARROWS MARKING THE END OF THE CHROMOSOME\n')
  for iChr in chrsD: 
    sChr = chrInfo.chrIdx2txt(iChr)
    FOUT.write("ax.arrow(%9d, %3d, %d, 0.0, fc='%s', ec='k', head_width=%f, head_length=%f ) # chr%s\n"%
     (endPos[sChr]+hLen-aLen, ypos[sChr]+yOffset, aLen, color, hWid, hLen, sChr ))
  FOUT.write('%s'%(Template("""
ax.set_ylim(0,${yMax})
ax.set_xlim(0,${xMax})
ax.grid(True)
ax.set_xlabel('Gene Locations (Mb)')
ax.set_ylabel('Chromosomes')
""").substitute(
  xMax = endPos['1'] + 1.5*hLen,
  yMax = getYmax(yProp,len(ypos)))))


def get_yticklabels(chrs):
  yticklabels = []
  for iChr in chrs:
    yticklabels.append(chrInfo.chrIdx2txt(iChr))
  return yticklabels

def get_ypos(init,delta):
  ypos = {}
  v = init
  ChrLst = chrInfo.get_chrIdx2StrLst()
  for i in range(len(ChrLst)-1,-1,-1):
    ypos[ChrLst[i]] = v
    v += delta
  return ypos

def get_yticks(chrs,yProp):
  delta = yProp['delta']
  ticks = get_ypos(yProp['init']+getYoffset_middle(yProp), delta )
  ytick = []
  for iChr in chrs:
    ytick.append(ticks[chrInfo.chrIdx2txt(iChr)])
  return ytick

def getArgs():
  args = {}
  for arg in sys.argv[1:]:
    if os.path.isfile(arg):
      args['fin'] = arg
  if 'fin' in args:
    args['subj'] = din.get_fin_subj(args['fin'])
    return args
  raise Exception("NO INPUT FILE FOUND")

def get_fout_png(subj):
  fout = '_'.join(['plot_genes', subj])
  return ''.join( [fout, '.py'] ), ''.join( [fout, '.png'] )

if __name__ == '__main__':
  main()
