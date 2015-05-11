#!/usr/bin/python

# Copyright (C) 2014-2015 DV Klopfenstein. All rights reserved.
__author__ = "DV Klopfenstein"

import sys
import os
import re

def main():
  args = getArgs()
  doCols(args) 

def doCols(args):
  PRT = sys.stdout
  if args['fout']:
    PRT  = open(args['fout'],'w')
  hdr_help = 'H' in args 

  # Open NCBI Gene file (or other tab-delimited file containing a header)
  for fin in args['fins']:
    colHdrs = []
    colIdx  = []
    delim   = args['delim']
    tab     = args['tab']
    colStrs = args['colStrs']
    do_re   = 're' in args
    XY = None
    with open(fin, "rU") as FIN:
      # Loop through each line in the file
      #print 'FIN', fin
      for lnum,line in enumerate(FIN):
        line = line.rstrip('\n')
        # If hdrs already collected, looking at data
        if colHdrs:
          if colIdx: 
            prt_vals(PRT, line, lnum, delim, tab, colHdrs, colIdx, XY, args['prt_lnum'])
          elif do_re:
            get_cols_match(PRT, line, lnum, delim, tab, colHdrs, args['re'])
  
        elif (not hdr_help and lnum==0) or (hdr_help and args['H'] in line):
          if '#Format: ' in line: line = get_NCBI_gene_info(line) 
          colHdrs = re.split(delim,line)
          #print 'FFFFFFFFFFFFF', line
          #print colHdrs
          colHdrs = [ H.strip('"') for H in colHdrs ] # Strip leading and trailing "
          if not colStrs:
            prtColHdrs(colHdrs)
          if all(colstr in colHdrs for colstr in colStrs):
            colIdx = [colHdrs.index(colstr) for colstr in colStrs]
          # Bail unless doing a grep
          elif not do_re:
          # else:
            print 'colIdx', colIdx
            errMsgHdr( args, colHdrs )
  
      if do_re: prt_re_colhdrs( args['re'], colHdrs)
    FIN.close()

  if args['fout']:
    PRT.close()
    print 'WROTE:', args['fout']


def prt_vals(PRT, line, lnum, delim, tab, colHdrs, colIdx, XY, prt_lnum):
  colVals = re.split(delim,line)
  tab = ' '
  #return # DVK
  for idx in colIdx:
    if idx<len(colHdrs):
      h = colHdrs[idx].replace('_position_on_the_genomic_accession','')
      fmt = '%s=%2s'+tab    if  h=='chromosome' else \
            '%s=%9s'+tab    if (h=='start' or h=='end') else \
            '%s=%-10s'+tab  if (h=='Symbol') else \
            '%s=%-10s'+tab  if (h=='GeneID') else \
            '%s=%-13s'+tab  if (h=='map_location') else \
            '%s=%s'+tab
      if idx<(len(colVals)):
        elem = colVals[idx]
        if h=='Symbol': elem = elem.upper()
        PRT.write(fmt%(h,elem))
  if prt_lnum:
    PRT.write('#%3d '%lnum)
  if not XY:
    PRT.write('\n')
  else:
    PRT.write('X%s%s\n'%(tab,XY[2:]))
    PRT.write('Y%s%s\n'%(tab,XY[2:]))
    XY = None
    
def get_cols_match(PRT, line, lnum, delim, tab, colHdrs, re_set):
  # Look for a match
  found = False
  for key in re_set:
    if re.search( key, line, re.I):
      found = True
      break
  if not found:
    return
  # Match was found, log column header
  print "\n", line
  colVals = re.split(delim,line)
  for idx, V in enumerate(colVals):
    found = ""
    for key in re_set:
      if re.search( key, V, re.I):
        re_set[key].add(idx)
        found = "*"
    PRT.write('{:1} {:2} {:20} {}\n'.format(found, idx, colHdrs[idx], V))

def prt_re_colhdrs( re_set, colHdrs):
  print 
  for key in re_set:
    for I in re_set[key]:
      print key, 'FOUND UNDER COLUMN', colHdrs[I]
    

def prtColVals( line, colHdrs, colVals):
  h = len(colHdrs)
  v = len(colVals)
  print 'AAA', min(h,v), line
  for I in range(min(h,v)):
    sys.stdout.write('AAA %50s %s\n'%(colHdrs[I],colVals[I]))


def errMsgHdr( args, colHdrs ):
  prtColHdrs(colHdrs)
  for colstr in args['colStrs']:
    if colstr not in colHdrs:
      print ''.join(['YOUR COLUMN HEADER(', colstr, ') DOES NOT EXIST IN HEADER ARRAY'])
  print args
  raise Exception(''.join(['YOUR COLUMN HEADER(s) DOES NOT EXIST IN HEADER ARRAY delim(', args['delim'], ')']))


# ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz
def get_NCBI_gene_info( line ):
  line = line.replace('#Format: ','')
  line = line.replace(' (tab is used as a separator, pound sign - start of a comment)','')
  return line.replace(' ','\t')

def prtColHdrs(colHdrs):
  for idx,hdr in enumerate(colHdrs): print 'Col {} {} Hdr({})'.format(idx, chr(idx+65), hdr)

def getArgs():
  args = {'fins':[], 'fout':None, 'prt_lnum':False, 'colStrs':[]}
  args['delim'] = r'\t';
  args['tab']   =  '\t';
  fout = None
  for arg in sys.argv[1:]:
    # Get lst of column headers whose value matches
    if os.path.isfile(arg): args['fins'].append(arg)
    elif arg[0:3] == 're=': args['re']       = { arg[3:]:set() } 
    elif arg=='lnum':       args['prt_lnum'] = True
    elif arg=='o':          fout = True
    elif arg[0:2]=='o=':    args['fout'] = arg[2:]
    elif arg=='delim=space':
      args['delim'] = r'\s+' 
      args['tab']   = ' ' 
    # Give aid as to what the headers are
    elif 'H='in arg:        args['H'] = arg[2:]
    elif arg == 'all':      
      args['fins'].append('../../../DiseaseGenes/data/background/gene_lists/genes_NCBI_All_Homo_sapiens.tsv')
    else:
      args['colStrs'].append(arg)

  chkExt(args,args['fins'])

  if fout:
    args['fout'] = getFout(fin)

  return args

def chkExt(args, fins):
  """Check ext on one file."""
  for fin in fins:
    ext = os.path.splitext(fin)[1]
    if ext == '.csv':
      args['delim'] = r',';
      args['tab']   = ',';
    return

#def doColsArgs( fin, colHdrs, H, delim, fout):
#  args = {'prt_lnum':False}
#  args['fins'].append(fin)
#  args['colStrs']=colHdrs
#  args['H']=H
#  if delim=='space':
#    args['delim'] = r'\s+';
#    args['tab']   = ' ';
#  if fout=='o':
#    args['fout'] = getFout(fin)
#  doCols( args )

# HapMap/dumped_region_MEX_hs9_chr19_2014_0220.txt
# HapMap/HapMap_MEX_hs9_chr19_2014_0220.txt
def getFout(fin):
  if 'dumped_region_' in fin:
    return fin.replace('dumped_region_','HapMapReduced_')
  raise Exception('DOES NOT LOOK LIKE A HAPMAP FILE')

if __name__ == '__main__':
  main()
