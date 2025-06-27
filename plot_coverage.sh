#!/bin/bash
# Aman Pruthi 20FEB2024
# Plot coverage graphs from Clonal pipeline output
# Input1 - per_target_coverage.txt 
# Input2 - HS Metrics after UMI grouping text files
# Input3 - Sample Info file
# Output1 - Coverage plot for each sample
# Output2 - Coverage Efficiency for all the samples
# Output3 - Coverage plot for all the samples
# Usage - bash plot_coverage.sh Sample_Info_File

# Check if sample info file argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: bash plot_coverage.sh Sample_Info_File"
    exit 1
fi

SAMPLE_INFO_FILE=$1

mkdir -p ${PWD}/coverage_plots
cp -a ${PWD}/*_per_target_coverage.txt ${PWD}/coverage_plots
mkdir -p ${PWD}/coverage_plots/tumor ${PWD}/coverage_plots/normal

while read -r line; do
    sample=$(echo $line | awk '{print $1}')
    mv ${PWD}/coverage_plots/${sample}_per_target_coverage.txt ${PWD}/coverage_plots/tumor/
done < <(grep -E '(^|\s)Tumor($|\s)' ${PWD}/${SAMPLE_INFO_FILE})

while read -r line; do
    sample=$(echo $line | awk '{print $1}')
    mv ${PWD}/coverage_plots/${sample}_per_target_coverage.txt ${PWD}/coverage_plots/normal/
done < <(grep -E '(^|\s)NAT($|\s)' ${PWD}/${SAMPLE_INFO_FILE})

cd ${PWD}/coverage_plots

for i in ../hs-metrics/*hs*after*txt; do
    id=$(echo $i | sed 's/.*\///g' | sed 's/_.*//g')
    sed -n 7,8p $i | datamash --no-strict transpose | grep 'PCT_TARGET' | head -11 | sed 's/PCT_TARGET_BASES_//g' | awk '{print $1, $2*100, log($2)/log(2)}' OFS='\t' > ${PWD}/${id}_coverage-info.tsv
done

while read -r line; do
    sample=$(echo $line | awk '{print $1}')
    mv ${PWD}/${sample}_coverage-info.tsv ${PWD}/tumor/
done < <(grep -E '(^|\s)Tumor($|\s)' ../${SAMPLE_INFO_FILE})

while read -r line; do
    sample=$(echo $line | awk '{print $1}')
    mv ${PWD}/${sample}_coverage-info.tsv ${PWD}/normal/
done < <(grep -E '(^|\s)NAT($|\s)' ../${SAMPLE_INFO_FILE})

#################################################################
## Plotting efficiency and coverage distribution for tumor samples.

cd tumor

for file in *per_target_coverage.txt; do
    id=$(echo $file | sed 's/_.*//g')
    python3 /home/act/general-scripts//plot_coverage/plot_coverage_target_regions.py $file ${id}_coverage_tumor.png
done
echo 'Generated target region coverage for each tumor sample.'

python3 /home/act/general-scripts//plot_coverage/plot_coverage_efficiency.py tsv Coverage_efficiency_tumor.png
echo 'Generated Coverage_efficiency_tumor.png'

python3 /home/act/general-scripts//plot_coverage/plot_coverage_target_regions_combined.py txt Coverage_distribution_tumor.png
echo 'Generated Coverage_distribution_tumor.png'

rm *per_target_coverage.txt *_coverage-info.tsv
mv Coverage*png ../

#################################################################
## Plotting efficiency and coverage distribution for normal samples.

cd ../normal

for file in *per_target_coverage.txt; do
    id=$(echo $file | sed 's/_.*//g')
    python3 /home/act/general-scripts//plot_coverage/plot_coverage_target_regions.py $file ${id}_coverage_normal.png
done
echo 'Generated target region coverage for each normal sample.'

python3 /home/act/general-scripts//plot_coverage/plot_coverage_efficiency.py tsv Coverage_efficiency_normal.png
echo 'Generated Coverage_efficiency_normal.png'

python3 /home/act/general-scripts//plot_coverage/plot_coverage_target_regions_combined.py txt Coverage_distribution_normal.png
echo 'Generated Coverage_distribution_normal.png'

rm *per_target_coverage.txt *_coverage-info.tsv
mv Coverage*png ../

echo "Complete!"
