# P1 - Importing a data file using pandas DataFrame 
# Ethan Smith 
# 10 March 2025 

# Import the pandas package 
import pandas as pd 

# Import the file 
nitpicker_data = pd.read_csv(r'\\wsl.localhost\Ubuntu\home\ethan\SMTETH005_SCDM2025\SMTETH005-SCDM2025\P1_Reading_and_improving_flat_files_SMTETH005\nitpicker_20081129_0652_CTD.dat', delimiter='\t', header = 0)

# Print the data frame 
print(nitpicker_data)