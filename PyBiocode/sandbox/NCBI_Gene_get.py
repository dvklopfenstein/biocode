#!/usr/bin/env python

# http://www.gnu.org/licenses/gpl-2.0.html#SEC1
# 
# one line to give the program's name and an idea of what it does.
# Copyright (C) yyyy  name of author
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from Bio import Entrez

def main():
  Entrez.email = "music_pupil@yahoo.com"
  Entrez.tool  = "MyLocalScript"
  handle = Entrez.einfo()
  result = handle.read()
  print result

def chk_Count_RetMax(I):
  if 'Count' in I and 'RetMax' in I:
    if I['RetMax'] == I['Count']:
      return
    msg = "ONLY %d OF %d FIELDS WERE FOUND\n"%(I['RetMax'], I['Count'])
    raise Exception(msg)
  else:
    raise Exception("FIELDS NOT FOUND: 'Count' and/or 'RetMax'")

def get_field_str(name,REC):
  chk_field(name,REC)
  val = REC[name]
  if isinstance(val,str):
    return val
  else:
    raise Exception("FIELD(%s) IS NOT A STRING"%val)

def chk_field(name,REC):
  if name in REC:
    return
  else:
    raise Exception("FIELD(%s) NOT FOUND: '%s'"%name)

def ex_ESearch_ESummary():
  """Download PubMed records that are indexed in MeSH for both asthma and 
     leukotrienes and were also published in 2009."""

  # http://www.ncbi.nlm.nih.gov/books/NBK25498/#chapter3.ESearch__ESummaryEFetch
  #use LWP::Simple;
  Entrez.email = "music_pupil@yahoo.com"
  
  db = 'pubmed'
  Query  = "asthma[mesh] AND leukotrienes[mesh] AND 2009[pdat]"
  handle = Entrez.esearch(db="pubmed", term=Query, retmax=5000)
  record = Entrez.read(handle)
  chk_Count_RetMax(record)
  print 'Found %s items with QueryTranslation:'%record['Count'], get_field_str('QueryTranslation',record)
  print 'FOUND:', record['Count'], "items"
  chk_field('IdList',record)
  #for I in record['IdList']: print I
  

  print 
  for idx, R in enumerate(record):
    val = record[R]
    print idx, R
    if isinstance(val,list):
      print R, len(val), val, '\n'
 
  #assemble the esearch URL
  #base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
  #url = ''.join([base, "esearch.fcgi?db=$db&term=$Query&usehistory=y"])
 
  #post the esearch URL
  #output = get(url);

#  #parse WebEnv and QueryKey
#  $web = $1 if ($output =~ /<WebEnv>(\S+)<\/WebEnv>/);
#  $key = $1 if ($output =~ /<QueryKey>(\d+)<\/QueryKey>/);
#  
#  ### include this code for ESearch-ESummary
#  #assemble the esummary URL
#  $url = $base . "esummary.fcgi?db=$db&Query_key=$key&WebEnv=$web";
#  
#  #post the esummary URL
#  $docsums = get($url);
#  print "$docsums";
#  
#  ### include this code for ESearch-EFetch
#  #assemble the efetch URL
#  $url = $base . "efetch.fcgi?db=$db&Query_key=$key&WebEnv=$web";
#  $url .= "&rettype=abstract&retmode=text";
#  
#  #post the efetch URL
#  $data = get($url);
#  print "$data";

if __name__ == '__main__':
  #main()
  ex_ESearch_ESummary()
