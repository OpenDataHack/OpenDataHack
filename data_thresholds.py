### ---------------  Functions ------------------ ###
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
   
def find_risk_index(PM10thresh,PM25thresh,NO2thresh,RHthresh,Tthresh):
# Assigns risk categories based on combinations of thresholds of Particulates (10 and 2.5,
# NO2, relative humidity and temperature thresholds
# results in an output 2D array
   # Make a crude sum for now
   riskindex = PM10thresh + PM25thresh + NO2thresh + RHthresh + Tthresh
   return riskindex  

### ---------------  Main ------------------ ###   

# Load required libraries
import netCDF4 as nc
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import font_manager as ftm
from mpl_toolkits.basemap import Basemap
import time
import datetime
import math
import pandas as pd

# Define required filenames
fprep = "./output_";
mth = "Jan";  yyy = "2016";  ext = ".nc";
fapp = "_comp_" + mth + yyy + ext;
filenamePM10 = fprep + "pm10" + fapp;      # PM 10
filenamePM25 = fprep + "pm25" + fapp;      # PM 2.5 
filenameNO2 =  fprep + "no2" + fapp;       # NO2
filenameRH =  fprep + "humidity" + fapp;   # Relative Humidity
#filenameT = "./output_pm25_comp.nc";      # Temperature

# Define variable names
varnamePM10 = "PM10";   
varnamePM25 = "PM25";  
varnameNO2  = "NO2";
varnameRH  = "RH";
#varnameT  = "NO2";

# Define extract formats for netCDF4 data (same for all variables)
varlet =  "a";
varformat = "NETCDF4";

# Load aggregated UK PM10 data
filenamestrPM10comp = filenamePM10;              # Filename
varnamePM10comp = varnamePM10;                   # Variable name
ncdataPM10comp, dataPM10comp, latitudesPM10comp, longitudesPM10comp, timesPM10comp = load_netCDF4_compdata(filenamestrPM10comp, varnamePM10comp, varlet, varformat);
dataPM10 = dataPM10comp[0,:,:]                   # Store to 2D array
# Convert time to date from UNIX timestamp
ddaydataPM10 = datetime.date.fromtimestamp(int(timesPM10comp))
dataPM10median = np.median(dataPM10)             # Find median
# Find where values exceed threshold
valthr = dataPM10median
dataPM10thr = variable2D_over_threshold(dataPM10,valthr)

# Load aggregated UK PM25 data
filenamestrPM25comp = filenamePM25;              # Filename
varnamePM25comp = varnamePM25;                   # Variable name
ncdataPM25comp, dataPM25comp, latitudesPM25comp, longitudesPM25comp, timesPM25comp = load_netCDF4_compdata(filenamestrPM25comp, varnamePM25comp, varlet, varformat);
dataPM25 = dataPM25comp[0,:,:]                   # Store to 2D array
# Convert time to date from UNIX timestamp
ddaydataPM25 = datetime.date.fromtimestamp(int(timesPM25comp))
dataPM25median = np.median(dataPM25)             # Find median
# Find where values exceed threshold
valthr = dataPM25median
dataPM25thr = variable2D_over_threshold(dataPM25,valthr)

# Load aggregated UK NO2 data
filenamestrNO2comp = filenameNO2;                # Filename
varnameNO2comp = varnameNO2;                     # Variable name
ncdataNO2comp, dataNO2comp, latitudesNO2comp, longitudesNO2comp, timesNO2comp = load_netCDF4_compdata(filenamestrNO2comp, varnameNO2comp, varlet, varformat);
dataNO2 = dataNO2comp[0,:,:]                     # Store to 2D array
# Convert time to date from UNIX timestamp
ddaydataNO2 = datetime.date.fromtimestamp(int(timesNO2comp))
dataNO2median = np.median(dataNO2)               # Find median
# Find where values exceed threshold
valthr = dataNO2median
dataNO2thr = variable2D_over_threshold(dataNO2,valthr)

## Load aggregated UK Relative Humidity data
#filenamestrRHcomp = filenameRH;                # Filename
#varnameRHcomp = varnameRH;                     # Variable name
#ncdataRHcomp, dataRHcomp, latitudesRHcomp, longitudesRHcomp, timesRHcomp = load_netCDF4_compdata(filenamestrRHcomp, varnameRHcomp, varlet, varformat);
#dataRH = dataRHcomp[0,:,:]                     # Store to 2D array
## Convert time to date from UNIX timestamp
#ddaydataRH = datetime.date.fromtimestamp(int(timesRHcomp))
##dataRHmedian = np.median(dataRH)               # Find median
## Find where values exceed threshold
#valthr = 80;     # 80% relative humidity
#dataRHthr = variable2D_over_threshold(dataRH,valthr)
dataRHthr = np.zeros_like(dataNO2thr)

## Load aggregated UK Temperature data
#filenamestrTcomp = filenameT;                  # Filename
#varnameTcomp = varnameT;                       # Variable name
#ncdataTcomp, dataTcomp, latitudesTcomp, longitudesTcomp, timesTcomp = load_netCDF4_compdata(filenamestrTcomp, varnameTcomp, varlet, varformat);
#dataT = dataTcomp[0,:,:]  - 273.15;            # Store to 2D array and convert from K to °C
## Convert time to date from UNIX timestamp
#ddaydataT = datetime.date.fromtimestamp(int(timesTcomp))
#dataTmedian = np.median(dataT)                 # Find median
## Find where values exceed threshold
#valthr = dataTmedian;
#dataTthr = variable2D_over_threshold(dataT,valthr)
dataTthr = np.zeros_like(dataNO2thr)

# Find risk indices 
riskindices_all = find_risk_index(dataPM10thr,dataPM25thr,dataNO2thr,dataRHthr,dataTthr)

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

# Define Month and Year for plots
mmmyyy = mth + " " + yyy;


# Plot PM10 data on a map  - plots boundaries, parallels and meridians but not the data for some reason!!!
fig0, ax0 = plt.subplots()
x = longitudesPM10comp;     
y = latitudesPM10comp;
xoffset = 1.1;     yoffset = 0.1;
xpltmin = np.min(x);        xpltmax = np.max(x)+xoffset; 
ypltmin = np.min(y)-yoffset;    ypltmax = np.max(y);
llon0 = 0.5*(xpltmin + xpltmax)
llat0 = 0.5*(ypltmin + ypltmax)
map = Basemap(projection='tmerc',resolution='h',lat_0=llat0,lon_0=llon0,llcrnrlon=xpltmin,llcrnrlat=ypltmin,urcrnrlon=xpltmax,urcrnrlat=ypltmax)
map.drawcoastlines()
# Draw parallels
parmin = 50;  parmax = 60;  parstep = 2;
parallels = np.arange(parmin,parmax,parstep)
map.drawparallels(parallels,labels=[1,0,0,0],fontsize=ftsb)
# Draw meridians
mermin = -10;  mermax = 2;  merstep = 2;
meridians = np.arange(mermin,mermax,merstep)
map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=ftsb)
#map.drawmapboundary(fill_color='blue') # fill to edge
map.pcolor(X,Y,dataPM10)
plt.show()

# Working plots, need to figure out how to do in on a map

# Plot PM10 data
fig1, ax1 = plt.subplots()
p1 = ax1.pcolor(X,Y,dataPM10)
cb1 = fig1.colorbar(p1, ax = ax1)
# Set axes limits
xpltmin = math.floor(np.min(longitudesPM10comp));    xpltmax = math.ceil(np.max(longitudesPM10comp)); 
ypltmin = math.floor(np.min(latitudesPM10comp));     ypltmax = math.ceil(np.max(latitudesPM10comp));
plt.xlim(xpltmin,xpltmax)
plt.ylim(ypltmin,ypltmax)
ax1.set_aspect('equal','datalim')
ax1.get_xaxis().set_tick_params(which='both', direction='out')
ax1.get_yaxis().set_tick_params(which='both', direction='out')
for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
    label.set_fontproperties(axis_font)
plt.xlabel('Lon', fontproperties = labels_font)
plt.ylabel('Lat', fontproperties = labels_font)
title_str = "PM10, " + mmmyyy
plt.title(title_str, fontproperties = title_font)
plt.show()



# Plot PM25 data
fig2, ax2 = plt.subplots()
p2 = ax2.pcolor(X,Y,dataPM25)
cb2 = fig2.colorbar(p2, ax = ax2)
# Set axes limits
xpltmin = math.floor(np.min(longitudesPM25comp));    xpltmax = math.ceil(np.max(longitudesPM25comp)); 
ypltmin = math.floor(np.min(latitudesPM25comp));     ypltmax = math.ceil(np.max(latitudesPM25comp));
plt.xlim(xpltmin,xpltmax)
plt.ylim(ypltmin,ypltmax)
ax2.set_aspect('equal','datalim')
ax2.get_xaxis().set_tick_params(which='both', direction='out')
ax2.get_yaxis().set_tick_params(which='both', direction='out')
for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
    label.set_fontproperties(axis_font)
plt.xlabel('Lon', fontproperties = labels_font)
plt.ylabel('Lat', fontproperties = labels_font)
title_str = "PM25, " + mmmyyy
plt.title(title_str, fontproperties = title_font)
plt.show()

# Plot NO2 data
fig3, ax3 = plt.subplots()
p3 = ax3.pcolor(X,Y,dataNO2)
cb3 = fig3.colorbar(p3, ax = ax3)
# Set axes limits
xpltmin = math.floor(np.min(longitudesNO2comp));    xpltmax = math.ceil(np.max(longitudesNO2comp)); 
ypltmin = math.floor(np.min(latitudesNO2comp));     ypltmax = math.ceil(np.max(latitudesNO2comp));
plt.xlim(xpltmin,xpltmax)
plt.ylim(ypltmin,ypltmax)
ax3.set_aspect('equal','datalim')
ax3.get_xaxis().set_tick_params(which='both', direction='out')
ax3.get_yaxis().set_tick_params(which='both', direction='out')
for label in (ax3.get_xticklabels() + ax3.get_yticklabels()):
    label.set_fontproperties(axis_font)
plt.xlabel('Lon', fontproperties = labels_font)
plt.ylabel('Lat', fontproperties = labels_font)
title_str = "NO2, " + mmmyyy
plt.title(title_str, fontproperties = title_font)
plt.show()

# Plot Risk Indices
fig4, ax4 = plt.subplots()
p4 = ax4.pcolor(X,Y,riskindices_all)
cb4 = fig4.colorbar(p4, ax = ax4)
ax4.get_xaxis().set_tick_params(which='both', direction='out')
ax4.get_yaxis().set_tick_params(which='both', direction='out')
ax4.set_aspect('equal','datalim')
plt.xlim(xpltmin,xpltmax)
plt.ylim(ypltmin,ypltmax)
for label in (ax4.get_xticklabels() + ax4.get_yticklabels()):
    label.set_fontproperties(axis_font)
plt.xlabel('Lon', fontproperties = labels_font)
plt.ylabel('Lat', fontproperties = labels_font)
title_str = "Risk Indices (1-5), " + mmmyyy
plt.title(title_str, fontproperties = title_font)
plt.show()