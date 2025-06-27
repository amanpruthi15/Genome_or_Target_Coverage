import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
from itertools import cycle
import numpy as np

def plot_coverage(extension, output_file):
    input_files = [file for file in os.listdir() if file.endswith(extension)]

    if not input_files:
        sys.exit(f"No files with the extension {extension} found in the current directory.")

    # Increase the figure width to accommodate the legend
    plt.figure(figsize=(14, 6))

    legend_lines = []  # to store legend lines

    total_regions = 0  # total number of genomic regions
    
    line_styles = cycle(['-', '--', ':', '-.'])

    for i, input_file in enumerate(input_files):
        # Explicitly define column types to avoid dtype warnings
        dtypes = {
            "chr": str, "start": int, "end": int, "length": int, "name": str,
            "%gc": float, "mean_coverage": float, "normalized_coverage": float,
            "min_normalized_coverage": float, "max_normalized_coverage": float,
            "min_coverage": int, "max_coverage": int, "pct_0x": float, "read_count": int
        }
        data = pd.read_table(input_file, dtype=dtypes)

        # Handle non-finite values in 'mean_coverage'
        data["mean_coverage"] = pd.to_numeric(data["mean_coverage"], errors='coerce')  # Convert to numeric, coercing errors to NaN
        data["mean_coverage"] = data["mean_coverage"].fillna(0)  # Replace NaN with 0
        # Replace inf and -inf with 0
        data["mean_coverage"] = data["mean_coverage"].replace([np.inf, -np.inf], 0)
        data["mean_coverage"] = data["mean_coverage"].round().astype(int)
        
        # Use a different color for each file
        colors = ['blue', 'green', 'orange', 'red', 'purple', 'brown', 'pink', 'gray']
        color = colors[i % len(colors)]
        legend_label = os.path.basename(input_file).replace('_per_target_coverage.txt', '')

        # Calculate the total number of genomic regions
        total_regions += len(data)
        
        # Plot histogram for each file
        hist, bins, _ = plt.hist(data["mean_coverage"], bins=1000, range=(0, 5000), alpha=1, edgecolor=color, linewidth=1.5, histtype='step', linestyle=next(line_styles), label=None)

        # Create a legend line
        legend_lines.append(plt.Line2D([0], [0], color=color, linewidth=1, linestyle=next(line_styles)))

    # Set the y-axis ticks
    plt.gca().set_yticks(plt.gca().get_yticks())

    # Convert y-axis ticks to percentages
    plt.gca().set_yticklabels([f'{(v / total_regions * 100):.2f}%' for v in plt.gca().get_yticks()])

    # Add legend with custom lines, positioned to the right of the plot
    plt.legend(legend_lines, [os.path.basename(input_file).replace('_per_target_coverage.txt', '') for input_file in input_files], loc='center left', bbox_to_anchor=(1, 0.5))

    plt.xlabel("Coverage")
    plt.ylabel("Percentage of Genomic Regions")
    plt.title("Coverage Distribution")
    plt.xlim(0, 5000)
    plt.ylim(0, max(plt.gca().get_yticks()))  # Adjust y-axis limit to show all percentages

    # Save the figure in a supported format, e.g., 'png'
    plt.savefig(output_file, format='png', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 script.py <extension> <output_file>")

    extension = sys.argv[1]
    output_file = sys.argv[2]

    plot_coverage(extension, output_file)
