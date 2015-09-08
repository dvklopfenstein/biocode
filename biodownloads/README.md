# Biodownloads Summary

## Downloads in original source format
* **UCSC**
  * <a name="top"></a>[cytoBandIdeo.txt] (./UCSC/hg38/cytoBandIdeo.txt) from **UCSC**'s 
    [Human Genome](http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/) released 
    [Dec 2013 hg38, GRCh38] (http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/cytoBandIdeo.txt.gz)
  * <a name="top"></a>[cytoBandIdeo.txt] (./UCSC/mm10/cytoBandIdeo.txt) from **UCSC**'s 
    [Mouse Genome](http://hgdownload.soe.ucsc.edu/goldenPath/mm10/database/) released 
    [Dec 2011 mm10](http://hgdownload.soe.ucsc.edu/goldenPath/mm10/database/cytoBandIdeo.txt.gz)
* **NCBI Gene** Downloaded **September 8, 2015**
  * Homo sapiens
    * [genes_NCBI_All_Homo_sapiens.tsv](./NCBI/genes_NCBI_All_Homo_sapiens.tsv) using this
      [**Search for All DNA Items**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=%229606%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (56409 items downloaded)
    * [genes_NCBI_ProteinCoding.tsv](./NCBI/genes_NCBI_ProteinCoding.tsv) using this
      [**Search for Protein-Coding Genes**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=genetype+protein+coding%5BProperties%5D+AND+%229606%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (20930 items downloaded)
  * Mus musculus (house mouse)
    * [genes_NCBI_All_Homo_sapiens.tsv](./NCBI/genes_NCBI_All_Homo_sapiens.tsv) using this
      [**Search for All DNA Items**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=%2210090%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (56409 items downloaded)
    * [genes_NCBI_ProteinCoding.tsv](./NCBI/genes_NCBI_ProteinCoding.tsv) using this
      [**Search for Protein-Coding Genes**]
      (http://www.ncbi.nlm.nih.gov/gene/?term=genetype+protein+coding%5BProperties%5D+AND+%2210090%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (20930 items downloaded)
* **GENCODE lncRNA** [v22 Downloaded](ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_22/) July 6, 2015 [GRCh38](http://www.gencodegenes.org/releases/)
  * tsv extracted for all lines where feature=gene from gencode.v22.long_noncoding_RNAs.gtf:
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

