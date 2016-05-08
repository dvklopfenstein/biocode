# [Whole-genome CNV analysis: advances in computational approaches](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4394692/)
from 2015 Apr paper by Mehdi Pirooznia, Fernando S. Goes, and Peter P. Zandi    

*Accumulating evidence indicates that DNA copy number variation (CNV) 
is likely to make a significant contribution to **human diversity** 
and also play an important role in **disease susceptibility**.*

## *widely used [CNV detection tools](http://omictools.com/cnv-detection3-category)*
*with specific focus on whole genome sequencing data*

### *There are four main methods for detecting CNVs with NGS data*: 
* Read Pair (RP)
* Split-Read (SR)
* Read Depth (RD) 
* Assembly based (AS) methods

#### Read Pair (RP)
**Minus**:  Low sensitivity for detecting variation in repeating regions (Medvedev et al., 2009)   

* [PEMer ](http://sv.gersteinlab.org/pemer/)
* Hydra
* [Ulysses](http://www.lcqb.upmc.fr/ulysses/) and [github](https://github.com/gillet/ulysses)
* [BreakDancer](http://gmt.genome.wustl.edu/packages/breakdancer/)


#### Split Read (SR)
**Plus**: Can do single-base-pair resolution    
**Minus**: Extremely dependent on read length. Not as reliable in repetitive regions.    
(Bellos et al., 2012

* [Pindel](http://gmt.genome.wustl.edu/packages/pindel/)
* [Gustaf](https://www.seqan.de/apps/gustaf/)
* [SVseq2](http://www.engr.uconn.edu/~jiz08001/svseq2.html)
* [Prism](http://compbio.cs.toronto.edu/prism/)


#### Read Depth (RD)
**Plus**: Good at detecting absolute copy number (Alkan et al., 2009   
**Minus**: Poor efficiency for determining small CNVs (Bellos et al., 2012)   

* CNV-seq (Xie and Tammi, 2009)
* BIC-seq (Xi et al., 2011)
* Cm.MOPS (Klambauer et al., 2012)
* CNVnator (Abyzov et al., 2011)
* ERDS (Zhu et al., 2012)
* RDXplorer (Yoon et al., 2009)
* ReadDepth (Miller et al., 2011)
* SeqSeq (Chiang et al., 2009)
* CNVrd2 (Nguyen et al., 2014)


#### Assembly (AS)
**Plus**: Does not require a reference genome.    
**Minus**: 
Requires large computational resources. 
Performs  poorly on repeats.    

* Magnolya


#### Combined Approac (CA)
* **SVDetect** (Zeitouni et al., 2010)
* **cnvHiTSeq** (Bellos et al., 2012)
* **Clever-sv** (Marschall et al., 2013)
* **CNVer** (Medvedev et al., 2010)
* **DELLY** (Rausch et al., 2012)
* **GenomeSTRiP** (Haraksingh and Snyder, 2013)
* **Gindel** (Chu et al., 2014)
* **GASVPro** (Sindi et al., 2012)
* **Hydra-Multi** (Lindberg et al., 2014)
* **LUMPY** (Layer et al., 2014)
* **PSCC** (Li et al., 2014)
* **SoftSearch** (Hart et al., 2013)

