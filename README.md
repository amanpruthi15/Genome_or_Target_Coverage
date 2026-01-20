# Plot target coverage
Calculate and plot target coverage using HS Metrics obtained using GATK CollectHSMetrics on BAM files.

**Steps:**
1. Coverage – Calculate HSMetrics using GATK tools on BAM/SAM files
2. A sample info file containing sample ID in the first column. 
3. Make sure the working directory has the output files from HSmetrics in a directory labelled 'hs-metrics'
4. Calculate coverage at each using the target bed file using bedtools.
