#!/usr/bin/env python
"""Test overlap values between two ChrABs."""

import sys
from pydvkbiology.util.chr_ab import ChrAB

def test_get_overlap_cab(prt=sys.stdout):
    chr_abs = [
        #    A                   B                Expected overlap    
        # -----------------  ------------------  ------------------
        (ChrAB('1',  0,  5), ChrAB('1',  4, 10), ChrAB('1',  4,  5)),
        (ChrAB('1',  4, 10), ChrAB('1',  0,  5), ChrAB('1',  4,  5)),
        (ChrAB('1',  0,  5), ChrAB('1',  0, 10), ChrAB('1',  0,  5)),
        (ChrAB('1',  1,  5), ChrAB('1',  0, 10), ChrAB('1',  1,  5)),
        (ChrAB('1',  0, 10), ChrAB('1',  1,  5), ChrAB('1',  1,  5)),
        (ChrAB('1',  0,  5), ChrAB('1',  1,  4), ChrAB('1',  1,  4)),
        (ChrAB('1',  0,  5), ChrAB('1',  6, 10), None              ),
        (ChrAB('1',  0,  5), ChrAB('1',  5, 10), ChrAB('1',  5,  None)),
        (ChrAB('1',  0,  5), ChrAB('1',  3,  4), ChrAB('1',  3,  4)),
    ]
    for cab_a, cab_b, cab_exp in chr_abs:
        cab_act = cab_a.get_overlap_cab(cab_b)
        prt.write("ACTUAL({OL:28}) A({A}) B({B})\n".format(OL=cab_act, A=cab_a, B=cab_b))
        assert cab_act == cab_exp, "EXPECTED({EXP})".format(EXP=cab_exp)
        

if __name__ == '__main__':
    test_get_overlap_cab()
