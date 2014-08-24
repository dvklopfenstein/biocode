# <a name=top></a>Scripts for frequently done lab tasks:

* [**Searching for and downloading NCBI PubMed abstracts**] (#abstracts)
* [**Searching for and downloading NCBI Gene Lists**] (#gene_lists)



## Task: <a name=abstracts></a>[**Searching for and downloading NCBI PubMed abstracts**] (#top):

1. Get PMIDs through the GUI at http://www.ncbi.nlm.nih.gov/pubmed:

(https://github.com/dklopfenstein/biocode/blob/master/doc/PyDkBio/PubMed_search.png)

2. Get PMIDs through the NCBI eutils using biopython and the function:
```
get_abstracts(
  'asthma_pubmed_ids.md',    # Markdown text File written and filled with PubMed Abstracts
  email  = 'myemail@gmail.com',
  query  = 'asthma[mesh] AND leukotrienes[mesh] AND "last 6 months" [DP]')
```

Writes the abstracts into the markdown text file, [asthma_pubmed_ids.md] (https://github.com/dklopfenstein/biocode/blob/master/doc/PyDkBio/asthma_pubmed_ids.md)

## Task: <a name=gene_lists></a>[**Searching for and downloading NCBI Gene Lists**] (#top):
