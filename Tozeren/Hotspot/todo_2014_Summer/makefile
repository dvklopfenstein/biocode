SCR := ../../../PyBiocode/hotspot/
DAT := ../data/
DIS := $(DAT)/genes_ManyDiseases_NCBI_sorted.txt

item2: item2_pltscr item2_chmod item2_plt

item2_pltscr:
	$(SCR)/clu_NCBI_genes.py $(DIS)  20000
	$(SCR)/clu_NCBI_genes.py $(DIS)  50000
	$(SCR)/clu_NCBI_genes.py $(DIS) 100000

item2_chmod:
	chmod 755 $(DAT)/genes_ManyDiseases_NCBI_sorted_distLT20000.txt
	chmod 755 $(DAT)/genes_ManyDiseases_NCBI_sorted_distLT50000.txt
	chmod 755 $(DAT)/genes_ManyDiseases_NCBI_sorted_distLT100000.txt

item2_plt:
	$(DAT)/genes_ManyDiseases_NCBI_sorted_distLT20000.txt
	$(DAT)/genes_ManyDiseases_NCBI_sorted_distLT50000.txt
	$(DAT)/genes_ManyDiseases_NCBI_sorted_distLT100000.txt
