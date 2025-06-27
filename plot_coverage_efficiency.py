# Aman Pruthi 20FEB2024
# Plot coverage graphs from Clonal pipeline output
# Input - HS Metrics after UMI grouping text files
# Output - Coverage Efficiency for all the samples
# Usage - python3 plot_coverage_efficiency.py txt Coverage_efficiency.png

import os
import sys
import matplotlib.pyplot as plt

def plot_data(file_path, extension):
    # Read data from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extracting data from each line
    column1 = [line.split()[0] for line in lines]
    column2 = [float(line.split()[1]) for line in lines]

    # Plotting the data
    plt.plot(column1, column2, label=os.path.basename(file_path).replace(extension, "").replace('_coverage-info.', ''))

# Check if the correct number of arguments is provided
if len(sys.argv) < 3:
    print("Usage: python3 script.py txt output_graph.png")
    sys.exit(1)

# Iterate over all files in the working directory with the specified extension
extension = sys.argv[1]
for filename in os.listdir():
    if filename.endswith(extension):
        plot_data(filename, extension)

# Customize the plot
plt.xlabel('Depth of coverage')
plt.ylabel('Percentage of bases')
plt.title('Coverage Efficiency')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(False)

# Save the plot to the specified output file
output_file = sys.argv[2]
plt.savefig(output_file, bbox_inches='tight')

plt.show()
