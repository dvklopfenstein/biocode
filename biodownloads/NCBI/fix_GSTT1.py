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
    """Add missing coordinates to a disease gene."""
    fins = ["genes_NCBI_hsa_All.tsv", "genes_NCBI_hsa_ProteinCoding.tsv"]
    for fin in fins:
        with open(fin) as ifstrm:
            fout_file = 'tmp_{}'.format(fin)
            fout_strm = open(fout_file, 'w')
            for line in ifstrm:
                if 'GSTT1' in line:
                    flds = line.split('\t')
                    if int(flds[2]) == 2952:
                        print flds
                        print fin, 'GeneID      ', flds[2]
                        print fin, 'Symbol      ', flds[5]
                        print fin, 'map_location', flds[9]
                        print fin, 'chromosome  ', flds[10]
                        print fin, 'b0          ', flds[12]
                        print fin, 'bN          ', flds[13]
                        print fin, '+/-         ', flds[14]
                        print fin, 'exon_count  ', flds[15]
                        print fin, 'OMIM        ', flds[16]
                        flds[12] = '270308'  # b0
                        flds[13] = '278486'  # bN
                        flds[14] = 'minus' # +/-
                        flds[15] = '6'       # b0
                        flds[16] = ''.join([flds[16], '\t\r\n'])
                        line = '\t'.join(flds[:-1])
                fout_strm.write(line)
            fout_strm.close()
            sys.stdout.write("  READ:  {}\n".format(fin))
            sys.stdout.write("  WROTE: {}\n".format(fout_file))
            cmd = "mv {} {}".format(fout_file, fin)
            print cmd
            os.system(cmd)

if __name__ == '__main__':
    main()
