#!/usr/bin/env python
"""Test getting a random location from a ChrAB for a range of a user-specified length."""

import sys
import numpy as np

from pydvkbiology.util.chr_ab import ChrAB

def test_minus_cab(prt=sys.stdout, random_seed=None):
    """Subtract cab from self. Return remaining cab(s).

          INPUT                 OUTPUT 
          0         1           0         1           
          01234567890123456789  01234567890123456789  
    curr       ==========            ==========       
    cab0    -------     .                ======       
    cab1       . -------.            ==       =       
    cab2       . ----   .            ==    ====
    cab3       -------  .                   ===       
    cab4       .  -------            ===              
    cab5       .     -------         ======           
    cab6       ----------            None
    cab7    ---------------          None
    cab8   --  .        .            ==========       
    cab9       .        . --         ==========       
    """
    cab_cur = ChrAB('1', 5, 14)
    chr_abs = [
        # Input               Expected results
        (ChrAB('1',  2,  8),  [ChrAB('1',  9, 14)]), # cab0
        (ChrAB('1',  7, 13),  [ChrAB('1',  5,  6), ChrAB('1', 14, 14)]), # cab1
        (ChrAB('1',  7, 10),  [ChrAB('1',  5,  6), ChrAB('1', 11, 14)]), # cab2
        (ChrAB('1',  5, 11),  [ChrAB('1', 12, 14)]), # cab3
        (ChrAB('1',  8, 14),  [ChrAB('1',  5,  7)]), # cab4
        (ChrAB('1', 11, 17),  [ChrAB('1',  5, 10)]), # cab5
        (ChrAB('1',  5, 14),  [None              ]), # cab6
        (ChrAB('1',  2, 16),  [None              ]), # cab7
        (ChrAB('1',  1,  2),  [ChrAB('1',  5, 14)]), # cab8
        (ChrAB('1', 16, 17),  [ChrAB('1',  5, 14)]), # cab9
    ]
    for cab_m, exp in chr_abs:
        cabs = cab_cur.minus_cab(cab_m)
        prt.write("ChrAB({A}) minus ({B:28}) -> {cabs}\n".format(A=cab_cur, B=cab_m, cabs=cabs))
        

if __name__ == '__main__':
    test_minus_cab()

