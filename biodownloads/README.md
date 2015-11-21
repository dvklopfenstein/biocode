# Biodownloads Summary

## Downloads in original source format
* **UCSC**
  * <a name="top"></a>[cytoBandIdeo.txt] (./UCSC/hg38/cytoBandIdeo.txt) from **UCSC**'s 
    [Human Genome](http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/) released 
    [Dec 2013 hg38, GRCh38] (http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/cytoBandIdeo.txt.gz)
  * <a name="top"></a>[cytoBandIdeo.txt] (./UCSC/mm10/cytoBandIdeo.txt) from **UCSC**'s 
    [Mouse Genome](http://hgdownload.soe.ucsc.edu/goldenPath/mm10/database/) released 
    [Dec 2011 mm10](http://hgdownload.soe.ucsc.edu/goldenPath/mm10/database/cytoBandIdeo.txt.gz)
  * <a name="top"></a>[cytoBandIdeo.txt] (./UCSC/dm6/cytoBandIdeo.txt) from **UCSC**'s 
    [Fly Genome](http://hgdownload.soe.ucsc.edu/goldenPath/dm6/database/) released 
    [Aug 2014 (dm6, BDGP Release 6 + ISO1 MT)](http://hgdownload.soe.ucsc.edu/goldenPath/dm6/database/cytoBandIdeo.txt.gz)
* **NCBI Gene** Downloaded **October 24, 2015**
  * **Homo sapiens (human)**: Taxonomy ID 9606
    * [genes_NCBI_hsa_All.tsv](./NCBI/genes_NCBI_hsa_All.tsv) using this
      [**Search for All Human DNA Items**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=%229606%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (59542 items)
    * [genes_NCBI_hsa_ProteinCoding.tsv](./NCBI/genes_NCBI_hsa_ProteinCoding.tsv) using this
      [**Search for Human Protein-Coding Genes**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=genetype+protein+coding%5BProperties%5D+AND+%229606%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (20922 items)
    * [genes_NCBI_hsa_microRNA.tsv](./NCBI/genes_NCBI_hsa_microRNA.tsv) using this
      [**Search for All Human microRNA**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=9606%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D+AND+genetype+ncRNA%5BProperties%5D+AND+microRNA%5BTI%5D)
      (1882 items)
  * **Mus musculus (house mouse)**: Taxonomy ID 10090
    * [genes_NCBI_mus_All.tsv](./NCBI/genes_NCBI_mus_All.tsv) using this
      [**Search for All Mouse DNA Items**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=%2210090%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (73343 items)
    * [genes_NCBI_mus_ProteinCoding.tsv](./NCBI/genes_NCBI_mus_ProteinCoding.tsv) using this
      [**Search for Mouse Protein-Coding Genes**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=genetype+protein+coding%5BProperties%5D+AND+%2210090%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (29414 items)
    * [genes_NCBI_mus_microRNA.tsv](./NCBI/genes_NCBI_mus_microRNA.tsv) using this
      [**Search for Mouse microRNA**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=10090%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D+AND+genetype+ncRNA%5BProperties%5D+AND+microRNA%5BTI%5D)
      (1202 items)
  * **Drosophila melanogaster (fruit fly)**: Taxonomy ID 7227
* **GENCODE lncRNA** [v23 Downloaded](ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_23/) Oct 26, 2015
  * extracted for all lines where feature=gene from gencode.v23.long_noncoding_RNAs.gtf 
    (Release 23 (GRCh38.p3) 2.4MB 7/16/15 4:10:00 PM):
    [genes_GENCODE_lncRNA.tsv](./GENCODE/genes_GENCODE_lncRNA.tsv)

## Downloads translated to Python format
* **UniProt** Downloaded August 13, 2015
  * UniProt Accession numbers to Entrez GeneIDs (and vice versa) for Homo sapiens:    
  ```import pydvkbiology.dnld.uniprot_sprot_AC_GeneID_hsa```

# Biodownloads Details

## <a name="cytoBandIdeo"></a>cytoBandIdeo.txt

The *Ideo* file underlies the graphic display of the cytoband data in the small ideogram graphic above the main UCSC Browser display. Items in the last column (e.g. gneg, gpos, gvar, stalk, acen, etc.) are the names of the band in accordance with the standards defined by the ISCN 1995 manual and are used to the coloring seen in the UCSC Browser graphic.

* **gneg**: is a light stain
* **gpos**: is a dark stain ([dark] gpos25, gpos50, gpos75, and gpos100 [darkest])
* **acen**: short for acrocentric; bands adjacent to centromere.
* **gvar**: variable heterochromatic regions; either pericentric or telomeric
* **stalk**: regions on the short arms of the acrocentric chromosomes ch13, 14, 15, 21, 22 that have a "stalk-like" appearance.

