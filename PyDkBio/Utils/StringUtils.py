#!/usr/bin/env python
"""String Utilities helpful in my research."""

import numpy as np


def or_string_list(lst_of_strings, chr2zeros_lst, zeros2chr):
  """ORs a list of strings.  Returns one string resulting from the OR.

    Args:
      lst_of_strings: Input list of strings to be ORed.
      chr2zeros_lst:  Input list of characters that do not change the return value.
      zeros2chr:      Output character of "nul" of zero values
  """
  ORDS = None
  for cur_string in lst_of_strings:
    cur_ords = np.empty(len(cur_string), dtype=np.int)
    # Populate the current ords using the current string chrs
    for idx, letter in enumerate(cur_string):
      cur_ords[idx] = 0 if letter in chr2zeros_lst else ord(letter)
    # Perform bitwise or of current ords and running ords
    if ORDS is not None:
      ORDS = np.bitwise_or(ORDS, cur_ords)
    # Initialize the running ords
    else: 
      ORDS = cur_ords
    # Replace 0's with a character. Ex: ord(32)=' ', ord(46)= '.'
  ORDS[ORDS == 0] = ord(zeros2chr) # Change 0s to user-defined ord
  return ''.join([chr(Ord) for Ord in ORDS])


def prt_or_string_list(
    lst_of_strings = [
      '..........................................Ab....................................',
      '..........................Cn....................................................',
      '..........Cf....................................................................',
      '..Cb........................................Ac............................Nc....',
      '..Cb......Cf........Ck......Ia....................Af............................',
      '..Cb........Cg........................IfAa..Ac..................................',
      '............................................Ac..................................',
      '............................................Ac..................................',
      '............................................Ac..................................',
      '._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._',
      '..Cb..Cd....CgCh..CjCkCl..Cn..Ib..........AbAc..............Hb..Hd..Hf......Nd..',
      '._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._',
      '............Cg..................................................................',
      'Ca..........Cg..Ci....Cl........................................................',
    ],
  #    In this default example, the OR of the strings above is ored_str:
  # -> CaCb..Cd..CfCgChCiCjCkCl..CnIaIb......IfAaAbAc....Af........Hb..Hd..Hf....NcNd..
    chr2zeros_lst = ['.', '_'],
    zeros2chr = '.'
  ):
  """Prints input and output."""
  for cur_string in lst_of_strings:
    print "INPUT: ", cur_string
  ored_str = or_string_list(lst_of_strings, chr2zeros_lst, zeros2chr)
  print "OUTPUT:", ored_str
  return ored_str


if __name__ == '__main__':
  prt_or_string_list()

