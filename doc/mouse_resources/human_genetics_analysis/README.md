# Human Genetics Analysis

## [1000 Genomes Project](http://www.1000genomes.org/)
[Tutorial](http://www.1000genomes.org/using-1000-genomes-data)

You’ve been working with Oprm1 knockout mice and notice they don’t display the normal rewarding effects of morphine administration. You wonder if humans with low levels of OPRM1 expression are
protected against opioid addiction, so you begin to do background research on the gene.

Where is the human OPRM1 gene located?
What gene is directly upstream of OPRM1? Which gene is directly downstream?
How many missense variants have been identified in the gene?
During your research, you find that there is a non-synonymous variant that is frequently studied: rs1799971 or A118G. Previous studies have indicated that mRNA containing the G allele is expressed at
lower levels than mRNA containing the A allele. It seems like a good potential SNP for you to study, but you need more information about frequency of the minor allele and the haplotype structure of
the region. 

  4. What is the minor allele frequency of rs1799971 in the European-American (CEU) population? What about the African-American (ASW) population?

  5. How many SNPs are in perfect linkage disequilibrium with rs1799971 in European-Americans? In African-Americans?

 Bonus question: What’s the most likely reason for the differences between African-Americans and European-Americans in question 5?

You realize that most of the DNA samples from your opioid dependence study come from African-Americans, so you decide to not study rs1799971. Instead you want to download all of the African-American
OPRM1 genetic variation data and look for potential polymorphisms to study.

  6. Generate a VCF file containing all of the genetic variation in OPRM1 for the African-American population (don’t download the file).

[Answers PDF](Answers_for_Database_Problems_1000_Genomes.pdf)

## NHLBI Exome Variant Server
Knock-in mice have been created so that they express a cocaine-insensitive form of the dopamine transporter (DAT). Cocaine reward is abolished in these mice. The human DAT is encoded by the SLC6A3 gene.
You hypothesize that some coding genetic variants in SLC6A3 may result in DAT proteins that are less sensitive to cocaine and that individuals carrying those variants may have reduced susceptibility
to cocaine dependence.

 Are there any common coding non-synonymous polymorphisms in either the African-American or European-American populations (minor allele frequency > 5%)?
Which coding SNP has the highest frequency in the African-American population?
 Bonus question: Based on your answers, do you think it’s worth doing an association analysis of any SLC6A3 polymorphisms in cocaine addicts and controls?
[Answers PDF](Answers_for_Database_Problems_NHLBI.pdf)

## [Haploview](https://www.broadinstitute.org/scientific-community/science/programs/medical-and-population-genetics/haploview/haploview)
[Tutorial](https://www.broadinstitute.org/scientific-community/science/programs/medical-and-population-genetics/haploview/tutorial)

## [PLINK](http://pngu.mgh.harvard.edu/~purcell/plink/gplink.shtml)
[Tutorial](https://www.broadinstitute.org/scientific-community/science/programs/medical-and-population-genetics/haploview/tutorial)

## [GWAS Catalog](https://www.ebi.ac.uk/gwas/home)
Excited by Thorgeir's presentation on the first nicotine GWAS, you go to the GWAS Catalog to find what other studies have been done on nicotine addiction and smoking.

 How many GWAS have been performed with “nicotine dependence” as the studied phenotype?
How many of those studies found significant associations?
What SNP has the most significant association with nicotine dependence?
 Click on the SNP ID and it will search the GWAS Catalog for all significant associations involving that SNP. You notice that the SNP was found in studies that analyzed phenotypes closely related to
nicotine dependence, including smoking behavior and lung adenocarcinoma.

  4. If you search the catalog for the term “smoking”, how many studies appear?
  5. How many studies would you have missed if you only searched for “nicotine dependence”?
[Answers PDF](Answers_for_Database_Problems_GWAS.pdf)

## [dbGAP](http://www.ncbi.nlm.nih.gov/gap)
[Tutorial](http://www.ncbi.nlm.nih.gov/projects/gap/tutorial/dbGaP_demo_1.htm)

The large number of studies that you’ve seen in the GWAS Catalog has given you the idea to do a meta-analysis of smoking behavior. That means you have to find studies whose data has been made
available through services like dbGAP.

 How many nicotine dependence studies have data available on dbGAP?
Based on the data available in the search results, what potential problems would arise when combining studies for a meta-analysis?
 You notice that “The Genetic Architecture of Smoking and Smoking Cessation” has passed embargo and the associated data are available for investigators. Click on the link to the study.

  3. What is the primary variable being analyzed in this study?
  4. Many smoking studies use cigarettes per day as a measurement of dependence. Did this study collect that data from participants?
  5. Are ethnicity data available for this study?
[Answers PDF](Answers_for_Database_Problems_dbgap.pdf)

## [dbSNP](http://www.ncbi.nlm.nih.gov/SNP/)
[Handbook](http://www.ncbi.nlm.nih.gov/books/NBK21093/?report=reader)

## [eQTL Browser](http://www.ncbi.nlm.nih.gov/projects/gap/eqtl/index.cgi)
Two of the studies in your recent search through the GWAS Catalog found associations between nicotine dependence and SNPs near the genes encoding the nicotinic receptors (the CHRNA3/CHRNA5/CHRNB4
locus and CHRNB3). You suspect that the significant SNPs from the GWAS may alter expression of those genes, affecting response to nicotine use.

  1. Are either of those two SNPs associated with expression of the nicotinic receptor genes?

You are also interested in identifying other SNPs that are associated with nicotinic receptor expression, since they may also be relevant to nicotine addiction susceptibility. A search through the
eQTL Browser shows that there is one SNP associated with CHRNA3 expression.

  2. What is the ID of that SNP?
  3. What tissue was used for that analysis?

You notice that the SNP is on a completely separate chromosome from CHRNA3. You click on the SNP ID, which brings you to that SNP’s page on the dbSNP website and lets you get more information.

  4. What gene is the SNP locating within?
  5. What is the minor allele frequency in the HapMap sub-Saharan African population (“YRI”)? What about in the Japanese population (“JPT”)?

Bonus question: The answers in question 5 are a warning to be careful when comparing minor allele frequencies across populations. What’s the problem when comparing those two populations?
[Answers PDF](Answers_for_Database_Problems_eQTL.pdf)

## [GTEx](Portal)
You're suspicious that the eQTL Browser didn't cover all of the CHRNA3 eQTLs, so you look for a second opinion at GTEx Portal.  

1. It looks like there are a lot more eQTLs for CHRNA3 in the GTEx database.  What are some reasons why this might be the case?

2.  What SNP is the most significant eQTL for CHRNA3 in a region of the brain?

3. Click on "eQTL box plot" for that SNP.  Is expression higher for the reference allele or the alternate allele?

GTEx Portal can also be used to examine expression data for genes of interest in the tissue library.  You want to know if there are non-brain tissues that you should potentially be studying in your
research on nicotinic receptors.  

4. What tissue has the highest expression of CHRNA3? What brain region has the highest expression?

5. There is only one eQTL for CHRNA3 between those two tissues.  Why would an eQTL be tissue specific?



