def load_netCDF4_compdata(filenamestr, varnamecomp, varlet, varformat):
# Load netCDF4 data of aggregated monthly values
   ncdata = nc.Dataset(filenamestr,varlet,format=varformat);
   latitudes = ncdata.variables['Lat'][:];      # Extracts latitudes
   longitudes = ncdata.variables['Long'][:];    # Extracts longitudes
   times = ncdata.variables['ansi'][:];         # Exracts times (UNIX timestaps)
   data = ncdata.variables[varnamecomp][:];     # Extracts latitudes
   return ncdata, data, latitudes, longitudes, times
   
def variable2D_over_threshold(variable2D,threshold):
# Finds where 2D array exceeds set threshold values and stores
# results in an output 2D array
   # Define output array and set it to 0
   variable2Dthr = np.zeros_like(variable2D)
   # Where variable2D > threshold set output array to 1
   variable2Dthr[ np.where( variable2D > threshold ) ] = 1
   return variable2Dthr
   

# Load required libraries
import netCDF4 as nc
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import font_manager as ftm
from mpl_toolkits.basemap import Basemap
import time
import datetime

# Load aggregated UK PM10 data
filenamestrPM10comp = "./output_pm10_comp.nc";   # Filename
varnamePM10comp = "PM10";                        # Variable name
varlet =  "a";
varformat = "NETCDF4";
ncdataPM10comp, dataPM10comp, latitudesPM10comp, longitudesPM10comp, timesPM10comp = load_netCDF4_compdata(filenamestrPM10comp, varnamePM10comp, varlet, varformat);
dataPM10 = dataPM10comp[0,:,:]                   # Store to 2D array
# Convert time to date from UNIX timestamp
ddaydataPM10 = datetime.date.fromtimestamp(int(timesPM10comp))
#
dataPM10median = np.median(dataPM10)             # Find median
# Find where values exceed median
dataPM10thr = variable2D_over_threshold(dataPM10,dataPM10median)

# Load aggregated UK PM25 data
filenamestrPM25comp = "./output_pm25_comp.nc";   # Filename
varnamePM25comp = "PM25";                        # Variable name
ncdataPM25comp, dataPM25comp, latitudesPM25comp, longitudesPM25comp, timesPM25comp = load_netCDF4_compdata(filenamestrPM25comp, varnamePM25comp, varlet, varformat);
dataPM25 = dataPM25comp[0,:,:]                   # Store to 2D array
# Convert time to date from UNIX timestamp
ddaydataPM25 = datetime.date.fromtimestamp(int(timesPM25comp))
dataPM25median = np.median(dataPM25)             # Find median
# Find where values exceed median
dataPM25thr = variable2D_over_threshold(dataPM25,dataPM25median)

# Load aggregated UK NO2 data
filenamestrNO2comp = "./output_no2_comp.nc";   # Filename
varnameNO2comp = "NO2";                        # Variable name
ncdataNO2comp, dataNO2comp, latitudesNO2comp, longitudesNO2comp, timesNO2comp = load_netCDF4_compdata(filenamestrNO2comp, varnameNO2comp, varlet, varformat);
#dataNO2 = ncdataNO2comp.variables['NO2'][1,:,:]
dataNO2 = dataNO2comp[0,:,:]                   # Store to 2D array
# Convert time to date from UNIX timestamp
ddaydataNO2 = datetime.date.fromtimestamp(int(timesNO2comp))
dataNO2median = np.median(dataNO2)             # Find median
# Find where values exceed median
dataNO2thr = variable2D_over_threshold(dataNO2,dataNO2median)

# ------------------------------------- Plot data --------------------------------------
# Define plot parameters
# Set the font dictionaries (for plot title and axis titles)
ftsb = 14
ftname = 'Bitstream Vera Sans'   #Default
##ftname = 'Helvetica'
axis_font   = ftm.FontProperties(family=ftname, size=ftsb, weight='normal')
title_font  = ftm.FontProperties(family=ftname, size=ftsb+4, weight='bold')
labels_font = ftm.FontProperties(family=ftname, size=ftsb+2, weight = 'bold')
legend_font = ftm.FontProperties(family=ftname, size=ftsb, weight='bold')

# Define grid of X (logitudes) and Y (latitudes) - same for all input data
X, Y = np.meshgrid(longitudesPM10comp, latitudesPM10comp);

# Plot PM10 data
fig1, ax1 = plt.subplots()
p1 = ax1.pcolor(X,Y,dataPM10)
cb1 = fig1.colorbar(p1, ax = ax1)
ax1.get_xaxis().set_tick_params(which='both', direction='out')
ax1.get_yaxis().set_tick_params(which='both', direction='out')
for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
    label.set_fontproperties(axis_font)
plt.xlabel('Lon', fontproperties = labels_font)
plt.ylabel('Lat', fontproperties = labels_font)
title_str = "PM10, " + str(ddaydataPM10)
plt.title(title_str, fontproperties = title_font)
plt.show()

# Plot PM25 data
fig2, ax2 = plt.subplots()
p2 = ax2.pcolor(X,Y,dataPM25)
cb2 = fig2.colorbar(p2, ax = ax2)
ax2.get_xaxis().set_tick_params(which='both', direction='out')
ax2.get_yaxis().set_tick_params(which='both', direction='out')
for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
    label.set_fontproperties(axis_font)
plt.xlabel('Lon', fontproperties = labels_font)
plt.ylabel('Lat', fontproperties = labels_font)
title_str = "PM25, " + str(ddaydataPM25)
plt.title(title_str, fontproperties = title_font)
plt.show()

# Plot NO2 data
fig3, ax3 = plt.subplots()
p3 = ax3.pcolor(X,Y,dataNO2)
cb3 = fig3.colorbar(p3, ax = ax3)
ax3.get_xaxis().set_tick_params(which='both', direction='out')
ax3.get_yaxis().set_tick_params(which='both', direction='out')
for label in (ax3.get_xticklabels() + ax3.get_yticklabels()):
    label.set_fontproperties(axis_font)
plt.xlabel('Lon', fontproperties = labels_font)
plt.ylabel('Lat', fontproperties = labels_font)
title_str = "NO2, " + str(ddaydataNO2)
plt.title(title_str, fontproperties = title_font)
plt.show()