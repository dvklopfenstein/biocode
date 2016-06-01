#!/usr/bin/env python
"""Test getting a random location from a ChrAB for a range of a user-specified length."""

import sys
import numpy as np

from pydvkbiology.util.chr_ab import ChrAB

def test_get_rand_loc(prt=sys.stdout, random_seed=None):
    chr_abs = [
        (ChrAB('1',  0,  5), 2),
        (ChrAB('1',  4, 10), 6),
        (ChrAB('1',  0,  5), 1),
        (ChrAB('1',  0, 10), 11),
        (ChrAB('1',  0, 10), 12),
        (ChrAB('1',  7,  1),  5),
    ]
    chr_abs.extend([(ChrAB('1', np.random.randint(10), np.random.randint(10)), np.random.randint(1, 10)) for i in range(100)])
    if random_seed is None:
        random_seed = np.random.randint(0, sys.maxint)
    for cab_cur, rng_len in chr_abs:
        cab_sub = cab_cur.get_rand_cab(rng_len)
        prt.write("ChrAB({A}) RNG_LEN({L:2}) -> RAND ({cab:28}) L({LEN:>4})\n".format(
            A=cab_cur, L=rng_len, cab=cab_sub, LEN=cab_sub.get_len() if cab_sub is not None else None))
        if cab_sub is not None:
            b0, bN = cab_cur.get_plotXs()
            assert cab_sub.get_len() == rng_len
            assert cab_sub.stop_bp <= bN
            assert cab_sub.start_bp >= b0
        else:
            assert cab_cur.get_len() < rng_len
    prt.write("RANDOM SEED(0x{S:0x})".format(S=random_seed))
        

if __name__ == '__main__':
    test_get_rand_loc()

