# Biodownloads Summary

## Downloads in original source format
* [**UCSC Sequence and Annotation Downloads**](http://hgdownload.cse.ucsc.edu/downloads.html) for 
  [cytoBandIdeo.txt file](#cytobandideotxt) and human/mouse/fly genomic sequence in 2bit files from
  [The Genome Reference Consortium](http://www.ncbi.nlm.nih.gov/projects/genome/assembly/grc/)
  * <a name="top"></a>
    [Human Genome](http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/) released 
    [Dec 2013 (hg38, GRCh38)] (http://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/cytoBandIdeo.txt.gz)
    * [cytoBandIdeo.txt](./UCSC/hg38/cytoBandIdeo.txt),
      [hg38.2bit](http://hgdownload.cse.ucsc.edu/goldenPath/hg38/bigZips/)
  * <a name="top"></a>
    [Mouse Genome](http://hgdownload.soe.ucsc.edu/goldenPath/mm10/database/) released 
    [Dec 2011 (mm10)](http://hgdownload.soe.ucsc.edu/goldenPath/mm10/database/cytoBandIdeo.txt.gz)
    * [cytoBandIdeo.txt](./UCSC/mm10/cytoBandIdeo.txt), 
      [mm10.2bit](http://hgdownload.cse.ucsc.edu/goldenPath/mm10/bigZips/)
  * <a name="top"></a>
    [Fly Genome](http://hgdownload.soe.ucsc.edu/goldenPath/dm6/database/) released 
    [Aug 2014 (dm6, BDGP Release 6 + ISO1 MT)](http://hgdownload.soe.ucsc.edu/goldenPath/dm6/database/cytoBandIdeo.txt.gz)
    * [cytoBandIdeo.txt](./UCSC/dm6/cytoBandIdeo.txt),
      [dm6.2bit](http://hgdownload.cse.ucsc.edu/goldenPath/dm6/bigZips/)

* [**NCBI Gene**](http://www.ncbi.nlm.nih.gov/gene/) Downloaded **Apr 22, 2018**
  * **Homo sapiens (human)**: Taxonomy ID [9606](
    http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=9606&lvl=3&lin=f&keep=1&srchmode=1&unlock)
    * [genes_NCBI_hsa_All.tsv](./NCBI/genes_NCBI_hsa_All.tsv) using this
      [**Search for All Human DNA Items**](http://www.ncbi.nlm.nih.gov/gene/?term=%229606%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (60196 items)
    * [genes_NCBI_hsa_ProteinCoding.tsv](./NCBI/genes_NCBI_hsa_ProteinCoding.tsv) using this
      [**Search for Human Protein-Coding Genes**](http://www.ncbi.nlm.nih.gov/gene/?term=genetype+protein+coding%5BProperties%5D+AND+%229606%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (20395 items) 
    * [genes_NCBI_hsa_microRNA.tsv](./NCBI/genes_NCBI_hsa_microRNA.tsv) using this
      [**Search for All Human microRNA**](http://www.ncbi.nlm.nih.gov/gene/?term=9606%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D+AND+genetype+ncRNA%5BProperties%5D+AND+microRNA%5BTI%5D)
      (1859 items) 
  * **Mus musculus (house mouse)**: Taxonomy ID [10090](http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=10090&lvl=3&lin=f&keep=1&srchmode=1&unlock)
    * [genes_NCBI_mus_All.tsv](./NCBI/genes_NCBI_mus_All.tsv) using this
      [**Search for All Mouse DNA Items**](http://www.ncbi.nlm.nih.gov/gene/?term=%2210090%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (68747 items) 
    * [genes_NCBI_mus_ProteinCoding.tsv](./NCBI/genes_NCBI_mus_ProteinCoding.tsv) using this
      [**Search for Mouse Protein-Coding Genes**](http://www.ncbi.nlm.nih.gov/gene/?term=genetype+protein+coding%5BProperties%5D+AND+%2210090%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (27548 items) 
    * [genes_NCBI_mus_microRNA.tsv](./NCBI/genes_NCBI_mus_microRNA.tsv) using this
      [**Search for Mouse microRNA**](http://www.ncbi.nlm.nih.gov/gene/?term=10090%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D+AND+genetype+ncRNA%5BProperties%5D+AND+microRNA%5BTI%5D)
      (1199 items) 
  * **Drosophila melanogaster (fruit fly)**: Taxonomy ID [7227](http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=7227&lvl=3&lin=f&keep=1&srchmode=1&unlock)
    * [genes_NCBI_dme_All.tsv](./NCBI/genes_NCBI_dme_All.tsv) using this
      [**Search for All Fruit fly DNA Items**](http://www.ncbi.nlm.nih.gov/gene/?term=%227227%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (25040 items) 
    * [genes_NCBI_dme_ProteinCoding.tsv](./NCBI/genes_NCBI_dme_ProteinCoding.tsv) using this
      [**Search for Fruit fly Protein-Coding Genes**](http://www.ncbi.nlm.nih.gov/gene/?term=genetype+protein+coding%5BProperties%5D+AND+%227227%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (13929 items) 
    * [genes_NCBI_dme_noncoding.tsv](./NCBI/genes_NCBI_dme_noncoding.tsv) using this
      [**Search for Fruit fly Non-coding DNA items**](http://www.ncbi.nlm.nih.gov/gene/?term=7227%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D+AND+((%22genetype+miscrna%22%5BProperties%5D+OR+%22genetype+ncrna%22%5BProperties%5D+OR+%22genetype+rrna%22%5BProperties%5D+OR+%22genetype+trna%22%5BProperties%5D+OR+%22genetype+scrna%22%5BProperties%5D+OR+%22genetype+snrna%22%5BProperties%5D+OR+%22genetype+snorna%22%5BProperties%5D)+NOT+%22genetype+protein+coding%22%5BProperties%5D))
      (3533 items) 
  * **Arabidopsis thaliana (thale cress)**: Taxonomy ID [3702](http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=3702&lvl=3&lin=f&keep=1&srchmode=1&unlock)
    * [genes_NCBI_ath_All.tsv](./NCBI/genes_NCBI_ath_All.tsv) using this
      [**Search for All thale cress DNA Items**](http://www.ncbi.nlm.nih.gov/gene/?term=%223702%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (38094 items) 
    * [genes_NCBI_ath_ProteinCoding.tsv](./NCBI/genes_NCBI_ath_ProteinCoding.tsv) using this
      [**Search for thale cress Protein-Coding Genes**](http://www.ncbi.nlm.nih.gov/gene/?term=genetype+protein+coding%5BProperties%5D+AND+%223702%22%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D)
      (27562 items) 
    * [genes_NCBI_ath_noncoding.tsv](./NCBI/genes_NCBI_ath_noncoding.tsv) using this
      [**Search for thale cress Non-coding DNA items**](http://www.ncbi.nlm.nih.gov/gene/?term=3702%5BTaxonomy+ID%5D+AND+alive%5Bproperty%5D+AND+((%22genetype+miscrna%22%5BProperties%5D+OR+%22genetype+ncrna%22%5BProperties%5D+OR+%22genetype+rrna%22%5BProperties%5D+OR+%22genetype+trna%22%5BProperties%5D+OR+%22genetype+scrna%22%5BProperties%5D+OR+%22genetype+snrna%22%5BProperties%5D+OR+%22genetype+snorna%22%5BProperties%5D)+NOT+%22genetype+protein+coding%22%5BProperties%5D))
      (6607 items) 

* **GENCODE lncRNA** [v23 Downloaded](ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_23/) Oct 26, 2015
  * extracted for all lines where feature=gene from gencode.v23.long_noncoding_RNAs.gtf 
    (Release 23 (GRCh38.p3) 2.4MB 7/16/15 4:10:00 PM):
    [genes_GENCODE_lncRNA.tsv](./GENCODE/genes_GENCODE_lncRNA.tsv)

* [**SNPs**](http://learn.genetics.utah.edu/content/pharma/snips/) downloaded Feb 12, 2016   
  * NCBI dbSNP [Search for All Human SNPs](http://www.ncbi.nlm.nih.gov/snp/?term=%22Homo+sapiens%22%5BOrganism%5D+AND+snp%5BSnp_Class%5D) 
   (144702459 items)
  * NCBI dbSNP [Search for OMIM Human SNPs](http://www.ncbi.nlm.nih.gov/snp/?term=%22Homo+sapiens%22%5BOrganism%5D+AND+snp%5BSnp_Class%5D+AND+AND+snp_omim%5BFilter%5D) 
   (16498 items)

## Downloads translated to Python format
* **UniProt** Downloaded December 26, 2015
  * 86,556 UniProt Accession numbers to 19,048 Entrez GeneIDs (and vice versa) for Homo sapiens:    
  ```
     import pydvkbiology.dnld.uniprot_sprot_hsa_AC2nt
     import pydvkbiology.dnld.uniprot_sprot_hsa_GeneID2ACs
  ```

# Biodownloads Details

## <a name="cytoBandIdeo"></a>cytoBandIdeo.txt

The *Ideo* file underlies the graphic display of the cytoband data in the small ideogram graphic above the main UCSC Browser display. Items in the last column (e.g. gneg, gpos, gvar, stalk, acen, etc.) are the names of the band in accordance with the standards defined by the ISCN 1995 manual and are used to the coloring seen in the UCSC Browser graphic.

* **gneg**: is a light stain
* **gpos**: is a dark stain ([dark] gpos25, gpos50, gpos75, and gpos100 [darkest])
* **acen**: short for acrocentric; bands adjacent to centromere.
* **gvar**: variable heterochromatic regions; either pericentric or telomeric
* **stalk**: regions on the short arms of the acrocentric chromosomes ch13, 14, 15, 21, 22 that have a "stalk-like" appearance.

