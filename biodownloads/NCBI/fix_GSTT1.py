#!/usr/bin/env python
"""One of the disease genes downloads with no coordinates, but they are actually in the record."""

import sys
import os

# Col 2 C Hdr(GeneID)
# Col 5 F Hdr(Symbol)
# Col 9 J Hdr(map_location)
# Col 10 K Hdr(chromosome)
# Col 12 M Hdr(start_position_on_the_genomic_accession)
# Col 13 N Hdr(end_position_on_the_genomic_accession)
# Col 14 O Hdr(orientation)
# Col 15 P Hdr(exon_count)
# Col 16 Q Hdr(OMIM)

def main():
  fins = ["genes_NCBI_hsa_All.tsv", "genes_NCBI_hsa_ProteinCoding.tsv"]
  for fin in fins:
    with open(fin) as ifstrm:
      fout = 'tmp_{}'.format(fin)
      FOUT = open(fout, 'w')
      for line in ifstrm:
        if 'GSTT1' in line:
          F = line.split('\t')
          if int(F[2]) == 2952:
            print F
            print fin, 'GeneID      ', F[2]
            print fin, 'Symbol      ', F[5]
            print fin, 'map_location', F[9]
            print fin, 'chromosome  ', F[10]
            print fin, 'b0          ', F[12]
            print fin, 'bN          ', F[13]
            print fin, '+/-         ', F[14]
            print fin, 'exon_count  ', F[15]
            print fin, 'OMIM        ', F[16]
            F[12] = '270308'  # b0
            F[13] = '278486'  # bN
            F[14] = 'minus' # +/-
            F[15] = '6'       # b0
            F[16] = ''.join([F[16], '\t\r\n'])
            line = '\t'.join(F[:-1])
        FOUT.write(line)
      FOUT.close()
      sys.stdout.write("  READ:  {}\n".format(fin))
      sys.stdout.write("  WROTE: {}\n".format(fout))
      cmd = "mv {} {}".format(fout, fin)
      print cmd
      os.system(cmd)

if __name__ == '__main__':
  main()
