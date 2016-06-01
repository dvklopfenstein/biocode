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
    for cab_cur, rng_len in chr_abs:
        cab_sub = cab_cur.get_rand_cab(rng_len)
        prt.write("ChrAB({A}) RNG_LEN({L:2}) -> RAND BP({BP:28}) L({LEN:>4})\n".format(
            A=cab_cur, L=rng_len, BP=cab_sub, LEN=cab_sub.get_len() if cab_sub is not None else None))
        if cab_sub is not None:
            assert cab_sub.get_len() == rng_len
            assert cab_sub.stop_bp <= cab_cur.stop_bp
            assert cab_sub.start_bp >= cab_cur.start_bp
        else:
            assert cab_cur.get_len() < rng_len
        

if __name__ == '__main__':
    test_get_rand_loc()

