##############################################################
# R code to analyze data from a morphine study.
#
# R can be downloaded from The Comprehensive R Archive Network
# (CRAN, http://cran.r-project.org/). This
# script is adapted from one developed by Elissa Chesler to generate the results in Kest et al, Mapping of a quantitative trait locus for morphine withdrawal severity. Mamm Genome 2004 Aug 15(8):610-7 
#
# Documented by Sue McClatchy | susan.mcclatchy@jax.org
# The Center for Genome Dynamics | The Jackson Laboratory
#
# 14 August 2013
##############################################################

# Set the working directory. In this case the data are 
# in the Downloads directory. Alternatively, change the 
# working directory using the Misc menu in the R 
# graphical user interface.
getwd()
setwd("Downloads/")

# Load R/qtl library. This can be downloaded from CRAN.
# http://cran.r-project.org/web/packages
install.packages("qtl")
library(qtl)

# Read in the data.
bxa <- read.cross(format="csv", file="tolerance4.csv")
?read.cross
ls()
summary(bxa)

# Have a peek at the phenotypes.
head(bxa$pheno)
##########################################################
# Genome scans
##########################################################
# Set up for scanning by calculating genotype probabilities.
bxa <- calc.genoprob(bxa, step=1, stepwidth="fixed", map.function="c-f", err=0.002)

# One dimensional genome scan 
bxa.scan1a <- scanone(bxa, pheno.col="X.sqrdep", method="hk")

# Run permutations.
bxa.perm1a <-scanone(bxa, pheno.col="X.sqrdep", method="hk", n.perm=100, perm.Xsp=TRUE)
# Plot the genome scan.
quartz()
plot(bxa.scan1a)
add.threshold(bxa.scan1a, perms=bxa.perm1a, alpha=0.05,lty="dashed",lwd=2,col="red")
add.threshold(bxa.scan1a, perms=bxa.perm1a, alpha=0.63,lty="dashed",lwd=2,col="green")

# Tabular summary options	
summary(bxa.scan1a)
summary(bxa.scan1a, perms=bxa.perm1a, alpha=0.10)
summary(bxa.scan1a, perms=bxa.perm1a, alpha=0.10, format="tabByCol",ci.function="lodint")

# Find the nearest marker to the chromosome 1 peak.
find.marker(bxa, 1, 53)

# Two dimensional genome scan 
bxa.scan2a <- scantwo(bxa, pheno.col="X.sqrdep", method="hk")

# Plot.
plot(bxa.scan2a)

# Report.
summary(bxa.scan2a, what="best", thresholds=c(9.1, 7.1, 6.3, 6.3, 3.3))

##########################################################
# Multiple QTL mapping
##########################################################

# Impute genotypes.
bxa <- sim.geno(bxa, step=2, n.draws=128, err=0.001)

# Create a QTL object by pulling out imputed genotypes at selected loci.
qtl <- makeqtl(bxa, chr=c(1, 5, 10), pos=c(56, 23, 42))
qtl
plot(qtl)

# Fit a model with selected QTL loci.
out.fq <- fitqtl(bxa, qtl=qtl, formula = y ~ Q1 + Q2 + Q3)
summary(out.fq)
