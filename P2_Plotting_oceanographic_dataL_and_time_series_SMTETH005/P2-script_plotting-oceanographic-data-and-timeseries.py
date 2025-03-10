# P2 - Creating plots using CTD data 
# Ethan Smith 
# 10 March 2025 

# Import the necessary packages
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from scipy.stats import iqr

    # Part 1 - Profiles ---------------------------------------------------------------------------------------------------

# Import the file 
nitpicker_data = pd.read_csv(r'\\wsl.localhost\Ubuntu\home\ethan\SMTETH005_SCDM2025\SMTETH005-SCDM2025\P1_Reading_and_improving_flat_files_SMTETH005\nitpicker_20081129_0652_CTD.dat', delimiter='\t', header = 0)

# Create a figure and axes to work on 
fig, ax = plt.subplots(1,2, sharey = True) # Creates two subplots, one next to the other. They share the y-axis

# Create the plots
ax[0].plot(nitpicker_data['Temperature (C)'], nitpicker_data['Depth (m)'], color = 'r')
ax[1].plot(nitpicker_data['Salinity (PSU)'], nitpicker_data['Depth (m)'], color = 'blue')

# Add more x-ticks to the temperature plot
temperature_ticks = np.arange(0, 31, 5)  # From 0 to 30 in increments of 5
ax[0].set_xticks(temperature_ticks)  # Set the x-ticks for temperature

# Add x-axis labels
ax[0].set_xlabel('Temperature (Degrees Celsius)')  
ax[1].set_xlabel('Salinity (PSU)')  

# Add y-axis labels 
ax[0].set_ylabel('Depth (m)') # Can set for either because sharey = True

# Reverse the shared y-axis 
ax[0].invert_yaxis()  # you can reverse either subplot's axis becuase they are shared 

# Check the plot  
plt.show()

# Save the plot
fig.savefig('Temperature-and-Salinity-side-by-side-lineplot_P2-part1.jpg', dpi=400)

    # Part 2 - Time series ----------------------------------------------------------------------------------------------

# Import the file with the index column set as the date (TIME_SERVER)
SO_winter_cruise_data_2017 = pd.read_csv(r"\\wsl.localhost\Ubuntu\home\ethan\SMTETH005_SCDM2025\SMTETH005-SCDM2025\P2_Plotting_oceanographic_dataL_and_time_series_SMTETH005\SAA2_WC_2017_metocean_10min_avg.csv", parse_dates = ['TIME_SERVER'], index_col = 'TIME_SERVER')

# Select data from the start of the cruise (2017-06-28) until the ship reached the southern most point (2017-07-04)
data = SO_winter_cruise_data_2017['2017-06-28':'2017-07-04']

        # Plot the time series of temperature using the grayscale style

plt.style.use('grayscale')
fig, ax = plt.subplots()
ax.plot(data.index, data['TSG_TEMP'])
ax.set_xlabel('Date')
ax.set_ylabel('Temperature (degrees Celsius)')

# Set x-ticks with only 10 evenly spaced ticks
ax.set_xticks(data.index[::len(data) // 10])  
ax.set_xticklabels(data.index[::len(data) // 10].strftime('%Y-%m-%d'), rotation=90)  # Format as 'YYYY-MM-DD' and rotate the tick labels

# Check the plot 
plt.show() 

# Adjust layout to fit x-tick labels properly
plt.tight_layout()

# Save the figure without cutting off labels
fig.savefig('Temperature-timeseries-grayscale_P2-part2.jpg', dpi=400, bbox_inches='tight')

        # Plot a histogram of the salinity distribution using bins of 0.5 psu between 30 and 35.

# Define bin edges from 30 to 35 with 0.5 PSU bin width
bins = np.arange(30, 35.5, 0.5)  # From 30 to 35 in 0.5 increments

# Create histogram plot
fig, ax = plt.subplots()
ax.hist(data['TSG_SALINITY'], bins=bins, label='Salinity', linewidth=2)

# Set axis labels
ax.set_xlabel('Salinity (PSU)')
ax.set_ylabel('# of Observations')

# Check the plot
plt.show()

# Save the plot
fig.savefig('Salinity-histogram_P2-part2.jpg', dpi=400)

       # Calculate the mean, standard deviation and the interquartile range for temperature and salinity and present the            results in a table

# Create variables containing the statistcs
# For temperature
temp_mean = data['TSG_TEMP'].mean()
temp_std = data['TSG_TEMP'].std()
temp_iqr = iqr(data['TSG_TEMP'].dropna())  # Remove NaN values becasue iqr does not work with them 

# For salinity 
saln_mean = data['TSG_SALINITY'].mean()
saln_std = data['TSG_SALINITY'].std()
saln_iqr = iqr(data['TSG_SALINITY'].dropna())  # Remove NaN values becasue iqr does not work with them 

# Create and print out a table containing the statistics
# Create a dictionary with the statistics
stats_dict = {
    'Statistic': ['Mean', 'Standard Deviation', 'Interquartile Range'],
    'Temperature (°C)': [temp_mean, temp_std, temp_iqr],
    'Salinity (PSU)': [saln_mean, saln_std, saln_iqr]
}

# Convert to DataFrame, round to 3 decimals
df = pd.DataFrame(stats_dict).round(3)

# Plot the table 
fig, ax = plt.subplots(figsize=(4, 2))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, loc='center')

# Save the table as an image
fig.savefig('Salinity-Temperature-statistics-table_P2-part2.jpg', bbox_inches='tight', pad_inches=0.05, dpi=400)

        # Create a scatter plot of wind speed and air temperature, encoding the latitude information in color. Wind speed is in meters per second and air temperature in degrees C
        
# Function to convert degrees and minutes (ddmm) to decimal degrees (dd)
def ddmm2dd(ddmm):     
    """     
    Converts a position input from degrees and minutes to degrees and decimals.     
    Input is ddmm.cccc and output is dd.cccc.     
    Note, it does not check if positive or negative.     
    """     
    thedeg = np.floor(ddmm / 100.)  # Extract the degrees part
    themin = (ddmm - thedeg * 100.) / 60.  # Convert the minutes to decimals
    return -(thedeg + themin)  # Return the decimal degrees (here they are negative because the data are from the souhtern hemisphere)

# Assuming 'LATITUDE' is in ddmm format, convert it to decimal degrees
data.loc[:, 'LATITUDE'] = data['LATITUDE'].apply(ddmm2dd)      

# Create the plot
plt.style.use('default')
fig, ax = plt.subplots()
scatter = ax.scatter(data['WIND_SPEED_TRUE'], data['AIR_TEMPERATURE'], c = data['LATITUDE'], cmap='cividis')
ax.set_xlabel('Wind speed (m/s)')
ax.set_ylabel('Air temperature (C)')
plt.colorbar(scatter, ax=ax, label='Latitude') # add a colourbar to show latitude

# Check the plot 
plt.show()

# Save the plot (300 DPI)       
fig.savefig('Air-temp-wind-speed-latitude_scatter_P2-part2.png', dpi=300) 