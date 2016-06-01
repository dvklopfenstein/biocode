#!/usr/bin/env python
"""Test getting a random location from a ChrAB for a range of a user-specified length."""

import sys
from pydvkbiology.util.chr_ab import ChrAB

def test_get_rand_loc(prt=sys.stdout):
    chr_abs = [
        (ChrAB('1',  0,  5), 2),
        (ChrAB('1',  4, 10), 6),
        (ChrAB('1',  0,  5), 1),
        (ChrAB('1',  0, 10), 11),
        (ChrAB('1',  0, 10), 12),
    ]
    for cab, rng_len in chr_abs:
        bp = cab.get_rand_loc(rng_len)
        prt.write("RAND BP({BP:4}) ChrAB({A}) RNG_LEN({L:2})\n".format(A=cab, L=rng_len, BP=bp))
        #assert cab_act == cab_exp, "EXPECTED({EXP})".format(EXP=cab_exp)
        

if __name__ == '__main__':
    test_get_rand_loc()
