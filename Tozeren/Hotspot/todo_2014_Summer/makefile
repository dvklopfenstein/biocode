# DIRECTORIES
SCR  := ../../../PyBiocode/hotspot/
DG   := ../../../../DiseaseGenes/
TODO := $(DG)/todo_2014_Summer/
DAT  := $(DG)/data/

DIS := $(DAT)/genes_ManyDiseases_NCBI_sorted.txt

item2: item2_mktxt item2_pltscr item2_mkplt item2_mv

item2_mktxt:
	$(SCR)/clu_NCBI_genes.py $(DIS)  20000
	$(SCR)/clu_NCBI_genes.py $(DIS)  50000
	$(SCR)/clu_NCBI_genes.py $(DIS) 100000

item2_pltscr:
	$(SCR)/plt_NCBI_genes.py $(DAT)/genes_ManyDiseases_NCBI_sorted_distLT20000.txt
	$(SCR)/plt_NCBI_genes.py $(DAT)/genes_ManyDiseases_NCBI_sorted_distLT50000.txt
	$(SCR)/plt_NCBI_genes.py $(DAT)/genes_ManyDiseases_NCBI_sorted_distLT100000.txt

item2_mkplt:
	plot_genes_ManyDiseasesdistLT20000.py  noshow
	plot_genes_ManyDiseasesdistLT50000.py  noshow
	plot_genes_ManyDiseasesdistLT100000.py noshow

item2_mv:
	mv plot_genes_ManyDiseasesdistLT20000.png  $(TODO)
	mv plot_genes_ManyDiseasesdistLT50000.png  $(TODO)
	mv plot_genes_ManyDiseasesdistLT100000.png $(TODO)

clean:
	rm -f plot_genes_ManyDiseasesdist*
