#!/usr/bin/env python
"""Test getting a random location from a ChrAB for a range of a user-specified length."""

import sys
import numpy as np

from pydvkbiology.util.chr_ab import ChrAB

def test_get_ChrAB_rng(prt=sys.stdout):
    """Expand range of a ChrAB."""
    cabs =          [ChrAB('1',  5, 14), ChrAB('1', 14,  5)]
    chr_abs = [
        # Input               Expected results
        ([ 2    ],  [ChrAB('1',  3, 16)]), # , ChrAB('1', 16,  3)]),
        ([ 5    ],  [ChrAB('1',  0, 19)]), # , ChrAB('1', 19,  0)]),
        ([ 6    ],  [ChrAB('1',  0, 20)]), # , ChrAB('1', 20,  0)]),
    ]
    for vals, exp in chr_abs:
        assert cabs[0].get_ChrAB_rng(*vals) == exp[0]
        assert cabs[1].get_ChrAB_rng(*vals) == exp[0]
        

if __name__ == '__main__':
    test_get_ChrAB_rng()

