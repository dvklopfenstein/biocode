## ------------------------------------------------------------------------
library(DOQTL)
library(AnnotationHub)
library(VariantAnnotation)

## ------------------------------------------------------------------------
load(file = "/data/logan_phenotypes.Rdata")
load(file = "/data/logan_haploprobs.Rdata")
ls()

## ------------------------------------------------------------------------
head(pheno)

## ------------------------------------------------------------------------
par(plt = c(0.18, 0.99, 0.1, 0.95))
image(1:100, 1:8, t(probs[2,,1:100]), ann = F, yaxt = "n",
      breaks = c(-0.25, 0.25, 0.75, 1.25), col = c("white", "grey50", "black"))
axis(side = 2, at = 1:8, labels = do.colors[,2], las = 1)
box()
abline(h = 2:8 - 0.5, col = "grey80")

## ------------------------------------------------------------------------
round(probs[2,,1:5], digits = 1)

## ------------------------------------------------------------------------
rownames(pheno) = paste0("EJC", pheno$animal_id)

## ------------------------------------------------------------------------
all(rownames(pheno) %in% rownames(probs))

## ------------------------------------------------------------------------
hist(pheno$measured_value, breaks = 20)

## ------------------------------------------------------------------------
hist(pheno$animal_zscore, breaks = 20)

## ------------------------------------------------------------------------
covar = matrix((pheno$sex == "m") * 1, ncol = 1, dimnames =
        list(rownames(pheno), "sex"))

## ------------------------------------------------------------------------
load(url("ftp://ftp.jax.org/MUGA/muga_snps.Rdata"))
markers = muga_snps
rm(muga_snps)

## ------------------------------------------------------------------------
K = kinship.probs(probs = probs, snps = markers, bychr = TRUE)

## ---- fig.width=8, fig.height=8------------------------------------------
image(1:nrow(K[[1]]), 1:ncol(K[[1]]), K[[1]], xlab = "Sample Index",
      ylab = "Sample Index", las = 1, breaks = 0:10/10, col = grey(10:1/10))
legend("bottomright", legend = 0:10/10, fill = grey(10:0/10), y.intersp = 0.6)

## ------------------------------------------------------------------------
qtl = scanone(pheno = pheno, pheno.col = "animal_zscore", probs = probs,
      K = K, addcovar = covar, snps = markers)
plot(qtl, main = "Tail Climbing")

## ---- cache=TRUE---------------------------------------------------------
perms = scanone.perm(pheno = pheno, pheno.col = "animal_zscore", probs = probs,
        addcovar = covar, snps = markers, nperm = 100)

## ------------------------------------------------------------------------
plot(qtl, main = "Tail Climbing", sig.thr = quantile(perms, 0.9))

## ------------------------------------------------------------------------
coefplot(qtl, chr = 6, main = "Tail Climbing")

## ------------------------------------------------------------------------
interval = bayesint(qtl = qtl, chr = 6, expandtomarkers = TRUE)
assoc = assoc.map(pheno = pheno, pheno.col = "animal_zscore", probs = probs,
        K = K[[6]], addcovar = covar, snps = markers, chr = 6,
        start = 94, end = 105)
assoc = assoc[!is.na(assoc[,12]),]
tmp = assoc.plot(results = assoc, thr = 5, show.sdps = TRUE)

## ------------------------------------------------------------------------
tmp = assoc.plot(results = assoc, thr = 5, show.sdps = TRUE, xlim = c(96, 100))

## ------------------------------------------------------------------------
top = assoc[assoc[,12] > 5.0,]
snp.file = "/sanger/mgp.v5.merged.snps_all.dbSNP142.vcf.gz"
hdr = scanVcfHeader(snp.file)
param = ScanVcfParam(info = "CSQ", geno = c("GT", "FI"),
        samples = samples(hdr)[c(5, 2, 26, 28, 16, 30, 35)],
        which = GRanges(seqnames = top[,1], ranges = IRanges(start = top[,2],
        width = 1)))
vcf = readVcf(file = snp.file, genome = "mm10", param = param)

vcf = vcf[-grep("intergenic_variant", as.list(info(vcf)$CSQ)),]
csq = as.list(info(vcf)$CSQ)
csq = lapply(csq, strsplit, split = "\\|")
csq = lapply(csq, function(z) {
        matrix(unlist(z), nrow = length(z), byrow = TRUE)
      })

unique(unlist(sapply(csq, function(z) { unique(z[,5]) })))

## ------------------------------------------------------------------------
keep = sapply(csq, function(z) {
         gr = grep("missense|splice|stop", z[,5])
         length(gr) > 0
       })
vcf = vcf[keep]
csq = csq[keep]
unique.genes = unique(sapply(csq, function(z) { unique(z[,2]) }))
unique.genes

## ------------------------------------------------------------------------
hub = AnnotationHub()
hub = query(hub, pattern = c("ensembl", "GTF", "Mus musculus"))
ensembl = hub[[names(hub)[grep("80.gtf$", hub$title)]]]

## ------------------------------------------------------------------------
unique(ensembl$gene_name[ensembl$gene_id %in% unique.genes])

## ------------------------------------------------------------------------
load("/data/chesler_hippocampus_expr.Rdata")

## ------------------------------------------------------------------------
samples = intersect(rownames(pheno), rownames(expr))
pheno = pheno[samples,]
expr = expr[samples,]
all(rownames(pheno) == rownames(expr))

## ------------------------------------------------------------------------
ensembl = ensembl[seqnames(ensembl) == 6 & start(ensembl) > 94e6 & end(ensembl) < 105e6]

## ------------------------------------------------------------------------
ensembl = ensembl[ensembl$gene_id %in% colnames(expr)]
ensembl = ensembl[ensembl$type == "gene"]
expr = expr[,ensembl$gene_id]
all(ensembl$gene_id == colnames(expr))

## ------------------------------------------------------------------------
max.qtl = which.max(qtl$lod$A[,7])
pr = probs[samples,,max.qtl]
fit = lm(pheno$animal_zscore ~ pheno$sex + pr)
regr.fit = vector("list", length(ensembl))
names(regr.fit) = ensembl$gene_name
for(i in 1:length(ensembl)) {
  regr.fit[[i]] = lm(pheno$animal_zscore ~ pheno$sex + expr[,i] + pr)
} # for(i)
delta.bic = sapply(regr.fit, BIC) - BIC(fit)
plot(start(ensembl) * 1e-6, delta.bic, las = 1, xlab  = "Chr 6 (Mb)",
     ylab = "BIC", col = 0)
text(start(ensembl) * 1e-6, delta.bic, names(regr.fit))

