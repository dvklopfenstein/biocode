#!/usr/bin/env python
"""One of the disease genes downloads with no coordinates, but they are actually in the record."""

#pylint: disable=invalid-name

__copyright__ = "Copyright (C) 2016-2017, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

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
    _adjust_gstt1(fins)

def _adjust_gstt1(fins):
    """Read tsv files downloaded from NSBI gene. Add NCBI coordinates to GSST1."""
    for fin in fins:
        with open(fin) as ifstrm:
            fout_file = 'tmp_{}'.format(fin)
            fout_strm = open(fout_file, 'w')
            for line in ifstrm:
                if 'GSTT1' in line:
                    flds = line.split('\t')
                    if int(flds[2]) == 2952:
                        _prt_fields(flds, fin)
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
            sys.stdout.write("{CMD}\n".format(CMD=cmd))
            os.system(cmd)

def _prt_fields(flds, fin):
    """Print fields in an NCBI line."""
    sys.stdout.write("{FLDS}\n".format(FLDS=" ".join(flds)))
    sys.stdout.write("{FIN} GeneID       {VAL}\n".format(FIN=fin, VAL=flds[2]))
    sys.stdout.write("{FIN} Symbol       {VAL}\n".format(FIN=fin, VAL=flds[5]))
    sys.stdout.write("{FIN} map_location {VAL}\n".format(FIN=fin, VAL=flds[9]))
    sys.stdout.write("{FIN} chromosome   {VAL}\n".format(FIN=fin, VAL=flds[10]))
    sys.stdout.write("{FIN} b0           {VAL}\n".format(FIN=fin, VAL=flds[12]))
    sys.stdout.write("{FIN} bN           {VAL}\n".format(FIN=fin, VAL=flds[13]))
    sys.stdout.write("{FIN} +/-          {VAL}\n".format(FIN=fin, VAL=flds[14]))
    sys.stdout.write("{FIN} exon_count   {VAL}\n".format(FIN=fin, VAL=flds[15]))
    sys.stdout.write("{FIN} OMIM         {VAL}\n".format(FIN=fin, VAL=flds[16]))

if __name__ == '__main__':
    main()

# Copyright (C) 2016-2017, DV Klopfenstein. All rights reserved.
