#!/usr/bin/env python

import sys
import os
import get_NCBI_genes_data as din
import collections as cx
import chrInfo
import get_genes
import numpy as np
import pylab as plt
import re

def main():
  args = get_args()
  data, mask, stats = get_data_n_mask( args['fin'], args['maxDist'] )
  fout = wr_fout( data, mask, args['fin'], args['maxDist'])

def run_stats():
  """Create a plot of 'Distance between genes to be counted in a cluster' and 'percentage genes in clusters'."""
  fin  = get_fin()
  data = get_data( fin )
  Min, Max = get_min_max_dist( data )
  X = []
  Y = []
  for maxDist in np.arange(0,Max,10000):
    mask, stats = get_mask( data, maxDist )
    title = get_genes.getTitle(fin)
    sys.stdout.write('  %4d of %4d (%3d%s) DNA elements had neighbors < %d bp apart: %s\n'%
      (stats['numLT'],stats['tot'],stats['percent'],'%',maxDist,title))
    X.append( maxDist )
    Y.append( stats['percent'] )
    if stats['percent'] == 100:
      break
  plt_stats(fin,X,Y,title)

def plt_stats(fin,X,Y,title):
  fig, ax = plt.subplots()
  plt.rc('font', size=16)
  plt.plot(X,Y)

  # SET THE X-AXIS LABELS FOR Mb
  # Need to draw the canvas, otherwise the labels won't be positioned and we won't have values yet.
  fig.canvas.draw()
  # Divide the bps by 1,000,000 to get proper Mb numbers
  labVal = [float(I)/1000000 for I in ax.get_xticks()]
  # Get the current x axis labels
  labels = [item.get_text() for item in ax.get_xticklabels()]
  # Replace the current x axis labels with the Mb values
  for I,L in enumerate(labels): labels[I] = float(labVal[I])
  ax.set_xticklabels(labels)

  ax.set_xlabel('Distance cutoff for close neigbors Mb)')
  ax.set_ylabel('Perentage of genes w/close neigbors')
  ax.set_title(title, fontsize=26)
  fig.set_size_inches(8,4)
  plt.subplots_adjust(top=0.90,bottom=0.20,left=0.10,right=0.95)
  png = ''.join(["Dist_vs_Perc_",title,".png"])
  plt.savefig(png, bbox_inches=0, dpi=200)
  print "  WROTE:", png
  plt.show()

def get_data( fin ):
  data = read_sorted_NCBI(fin)
  set_neighbor_dist( data )
  return data

def get_data_n_mask( fin, maxDist ):
  data = get_data( fin )
  mask, stats  = get_mask( data, maxDist )
  #sys.stdout.write('  %4d of %4d (%3d%s) DNA elements had neighbors < %d bp apart: %s\n'%
  #  (stats[0],stats[1],stats[2],'%',maxDist,title))
  return data, mask, stats
  #dists = get_neighbor_dist( data )
  #plot_histogram_dists( dists, get_genes.getTitle(args['fin']))
  #prt_sorted_NCBI( data )
  #mrg_sorted_NCBI( data )

def prtMask( mask ):
  for CHR in mask:
    for ID in mask[CHR]:
      print CHR, ID, mask[CHR][ID]

def test():
  data = gen_test_data()
  set_neighbor_dist( data )
  for CHR in data: 
    for E in data[CHR]: print E
  mask, stats = get_mask( data, 3 )
  for CHR in mask: 
    for ID in mask[CHR]: print ID, mask[CHR][ID]

def get_mask( data, max_dist ):
  """Create a mask where value is True if gene has neghbors closer tha max_dist, otherwisre false."""
  mask = cx.defaultdict( dict )
  totCnt = 0
  numLT  = 0
  for CHR in data:
    for E in data[CHR]:
      totCnt += 1
      T1 = (E[4]!=0 and E[6]!=0) and (E[4]<=max_dist or E[6]<=max_dist)
      if T1 or (E[4]==0 and E[6]<=max_dist) or (E[4]<=max_dist and E[6]==0):
        mask[CHR][E[0]] = True
        numLT += 1
      else:
        mask[CHR][E[0]] = False
  perc = int((float(numLT)/totCnt)*100)
  return mask, {"numLT":numLT, "tot":totCnt, "percent":perc}

def getMinMax( mn, mx, lhs, rhs ):
  pass
  #if ( lhs!=0 and rhs!=0 ):

def plot_histogram_dists( x, title ):
  data = np.array(x)
 
  plt.figure(0)
  barwidth  = 10000
  plotlimit = 1000000 
  hist1 = np.histogram(data, bins=np.arange(data.min(), data.max(), barwidth))
  #plt.bar(hist1[1][:-1], hist1[0], width=barwidth)
  # Mask of bools for bin values between 0 and 1,000,000
  mask = (hist1[1][:-1] > 0) * (hist1[1][:-1] < plotlimit)
  plt.bar(hist1[1][mask], hist1[0][mask], width=barwidth)

  #m = min( x )
  #M = max( x )
  #barwidth = 1000000
  #print m, M
  #n, bins, patches = plt.hist( x, bins = range( m, M+barwidth, barwidth) )
  plt.title('%s: %d Genes, dist<%s (barwidth=%d)'%(title,len(x),plotlimit,barwidth))
  saveFig(title)
  plt.show()

def saveFig(title):
  png = '%s_dist_hist.png'%(title)
  plt.savefig(png, bbox_inches=0, dpi=100)
  print "  WROTE:", png

def get_neighbor_dist( data ):
  """Get a list of all the nighbor distances."""
  dists = []
  for CHR in sorted(data):
    for E in data[CHR]:
      if E[4] != 0:
        dists.append(E[4])
  return dists

def get_min_max_dist( data ):
  dists = get_neighbor_dist( data )
  return min(dists), max(dists)
    

def prt_sorted_NCBI(data):
  """Print list of elements per chromosome."""
  for CHR in sorted(data):
    objLst = data[CHR]
    objOrdLst = sorted( objLst, key=lambda clusObj: int(clusObj[1]) )
    for C in objOrdLst: print CHR, C[0], C[4]
    #for C in objOrdLst: print CHR, C[0], C[4]
    #min_idx, min_value = min(enumerate(objOrdLst), key=lambda clusObj: int(clusObj[4]) )
    #print min_idx, min_value
    for E in objOrdLst:
      print chrInfo.chrIdx2txt(CHR), len(objOrdLst), E, E[1]

def mrg_sorted_NCBI(data):
  """Print list of elements per chromosome."""
  for CHR in sorted(data):
    chrLst = data[CHR]
    chrOrdLst = sorted( chrLst, key=lambda clusObj: int(clusObj[4]) )
    print
    for E in chrOrdLst:
      print chrInfo.chrIdx2txt(CHR), len(chrOrdLst), E[4], E

def set_neighbor_dist(data):
  """Set LHSdist and LHSidlist of elements per chromosome."""
  for CHR in sorted(data): # Sort chromosomes
    chrLst = data[CHR]
    chrOrdLst = sorted( chrLst, key=lambda clusObj: int(clusObj[1]) )
    for I,E in enumerate(chrOrdLst[1:]):  set_LH_dist( chrOrdLst[I], E )
    for I,E in enumerate(chrOrdLst[:-1]): set_RH_dist( E, chrOrdLst[I+1] )
    
def set_LH_dist( LHS, RHS ):
  RHS[4] = RHS[1] - LHS[1]
  RHS[5] = LHS[0]

def set_RH_dist( LHS, RHS ):
  LHS[6] = RHS[1] - LHS[1]
  LHS[7] = RHS[0]

def gen_test_data():
  data = cx.defaultdict( list )
  data[0].append([0,  1,  2, [], 0, None, 0, None])
  data[0].append([1,  5,  7, [], 0, None, 0, None])
  data[0].append([2, 20, 21, [], 0, None, 0, None])
  data[0].append([3, 22, 25, [], 0, None, 0, None])
  data[0].append([4, 30, 31, [], 0, None, 0, None])
  data[0].append([5, 33, 38, [], 0, None, 0, None])
  return data

def read_sorted_NCBI(fin):
  """Read a file containing sorted NCBI Gene data."""
  #CluElem = cx.namedtuple('CluElem', ['id', 'start', 'end', 'elems', 'LHdist', 'LHid', 'RHdist', 'RHid'])
  data = cx.defaultdict( list )
  ID = 0
  with open(fin) as FIN:
    for line in FIN:
      M, msg = din.getChrMatch(line)
      if M:
        E = din.getElem( M, line )
        S = E[1]
        data[ chrInfo.txt2Idx( E[0] ) ].append([ID, S, S, [S], 0, None, 0, None])
        ID += 1
  print "  READ: ", fin
  if data is not None:
    return data
  raise Exception("NO DATA FOUND IN {0}".format(fin))


def wr_fout( data, mask, fin, maxDist):
  """Print only those DNA elements which have close neighbors."""
  fout = getFoutName( fin, maxDist )
  ID = 0
  FOUT = open( fout, 'w' )
  with open(fin) as FIN:
    for line in FIN:
      M, msg = din.getChrMatch(line)
      if M:
        E = din.getElem( M, line )
        Chr = chrInfo.txt2Idx( E[0] )
        S   = E[1]
        if mask[ Chr ][ ID ]:
          FOUT.write(line)
        ID += 1
  FOUT.close()
  print "  WROTE:", fout
  return fout


def getFoutName( fin, maxDist ):
  p, e = os.path.splitext(fin)
  fout = ''.join( [p, '_distLT',  str(maxDist), e])
  return fout

def get_fin():
  args = get_args()
  return args['fin']

def get_args():
  """Get arguments for clustering algorithm."""
  args = { 'maxDist':50000 }
  for arg in sys.argv[1:]:
    if os.path.isfile(arg):
      args['fin'] = arg
      args['title'] = get_genes.getTitle(arg)
    elif re.search(r'^\d+$',arg):
      args['maxDist'] = int(arg)
  if 'fin' not in args:
    raise Exception("Need a sorted NCBI file as input")  
  return args

if __name__ ==  '__main__':
  #run_stats()
  main()
  #test()
