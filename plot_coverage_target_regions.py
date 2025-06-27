# Aman Pruthi 20FEB2024
# Plot coverage graphs from Clonal pipeline output
# Input - Meancoverage.bedgraph files
# Output - Coverage plot for each sample
# Usage - python3 plot_coverage_target_regions.py <input_file> <output_file>

import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_coverage(input_file, output_file):
    # Read the specified columns from the input file
    data = pd.read_table(input_file, usecols=["chrom", "start", "end", "mean_coverage"])
    
    # Round off the mean_coverage to the closest integer
    data["mean_coverage"] = data["mean_coverage"].round().astype(int)
    
    plt.figure(figsize=(10, 6))

    # Calculate the total number of genomic regions
    total_regions = len(data)

    # Plot histogram with modified parameters
    plt.hist(data["mean_coverage"], bins=1000, range=(0, 5000), alpha=1, linewidth=1.5, histtype='step', label=None)
    plt.xlabel("Coverage")
    plt.ylabel("Number of Genomic Regions")
    plt.title("Coverage Distribution")
    # Set the y-axis ticks
    plt.gca().set_yticks(plt.gca().get_yticks())

    # Convert y-axis ticks to percentages
    plt.gca().set_yticklabels([f'{(v / total_regions * 100):.2f}%' for v in plt.gca().get_yticks()])

    plt.xlim(0, 5000)
    plt.ylim(0, max(plt.gca().get_yticks()))

    plt.savefig(output_file)
    plt.show()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 plot_coverage_target_regions.py <input_file> <output_file>")

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    plot_coverage(input_file, output_file)
