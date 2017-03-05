### ================================================================================= ###   
### ================================== Functions ==================================== ### 
### ================================================================================= ###  

### ---------- Load netCDF4 data
def load_netCDF4_compdata(filenamestr, varnamecomp, varlet, varformat):
# Load netCDF4 data of aggregated monthly values
   ncdata = nc.Dataset(filenamestr,varlet,format=varformat);
   latitudes = ncdata.variables['Lat'][:];      # Extracts latitudes
   longitudes = ncdata.variables['Long'][:];    # Extracts longitudes
   times = ncdata.variables['ansi'][:];         # Exracts times (UNIX timestaps)
   data = ncdata.variables[varnamecomp][:];     # Extracts latitudes
   return ncdata, data, latitudes, longitudes, times

### ---------- Find 2D variables over threshold  
def variable2D_over_threshold(variable2D,threshold):
# Finds where 2D array exceeds set threshold values and stores
# results in an output 2D array
   # Define output array and set it to 0
   variable2Dthr = np.zeros_like(variable2D)
   # Where variable2D > threshold set output array to 1
   variable2Dthr[ np.where( variable2D > threshold ) ] = 1
   return variable2Dthr

### ---------- Interpolate 2D variables to lower resolution grid
def interpolate2Darray(latin,longin,data2Din,latinterp,longinterp,methodin):
# Interpolates arrays from higher resolution grid to lower resolution grid
   # Flip y (latitudes) of T and RH data upside down
   latinterpin = np.flipud(latinterp); 
   # Create grids
   LongInterp, LatInterp = np.meshgrid(longinterp,latinterpin);   
   LongIn, LatIn = np.meshgrid(longin,latin);
   # Reshape arrays
   xinterp = np.reshape(LongInterp,-1)
   yinterp = np.reshape(LatInterp,-1)
   xin = np.reshape(LongIn,-1)
   yin = np.reshape(LatIn,-1)
   datain = np.reshape(data2Din,-1)
   # Interpolate data
   data2Dinterp = interpolate.griddata((xin, yin), datain, (xinterp, yinterp), method = methodin)   
   data2Dinterp = np.flipud(np.reshape(data2Dinterp,LatInterp.shape))
   return data2Dinterp  

### ---------- Find risk indices   
def find_risk_index(PM10thresh,PM25thresh,NO2thresh,RHthresh,Tthresh):
# Assigns risk categories based on combinations of thresholds of Particulates (10 and 2.5,
# NO2, relative humidity and temperature thresholds
# results in an output 2D array
   # Make a crude sum for now
   riskindex = PM10thresh + PM25thresh + NO2thresh + RHthresh + Tthresh
   return riskindex  

### ---------- Make 2D plots   
def make2Dplot(lat,long,data2D,varname,datestr):
# Makes 2D plots of selected variables in x = long and y = lat coordinates
   # Define plot parameters
   # Set the font dictionaries (for plot title and axis titles)
   ftsb = 14
   ftname = 'Bitstream Vera Sans'   #Default
   axis_font   = ftm.FontProperties(family=ftname, size=ftsb, weight='normal')
   title_font  = ftm.FontProperties(family=ftname, size=ftsb+4, weight='bold')
   labels_font = ftm.FontProperties(family=ftname, size=ftsb+2, weight = 'bold')
   legend_font = ftm.FontProperties(family=ftname, size=ftsb, weight='bold')
   # Define grid of X (longitudes) and Y (latitudes)
   X, Y = np.meshgrid(long, lat);
   # Plot data
   fig, ax = plt.subplots()
   p = ax.pcolormesh(X,Y,data2D)
   cb = fig.colorbar(p, ax = ax)
   # Set axes limits and aspects
   xpltmin = math.floor(np.min(long));    xpltmax = math.ceil(np.max(long)); 
   ypltmin = math.floor(np.min(lat));     ypltmax = math.ceil(np.max(lat));
   plt.xlim(xpltmin,xpltmax);             plt.ylim(ypltmin,ypltmax);
   ax.set_aspect('equal','datalim')
   ax.get_xaxis().set_tick_params(which='both', direction='out')
   ax.get_yaxis().set_tick_params(which='both', direction='out')
   for label in (ax.get_xticklabels() + ax.get_yticklabels()):
       label.set_fontproperties(axis_font)
   plt.xlabel('Lon', fontproperties = labels_font)
   plt.ylabel('Lat', fontproperties = labels_font)
   title_str = varname + ", " + datestr
   plt.title(title_str, fontproperties = title_font)
   plt.show()
   
### ---------- Make 2D plots on the UK map   
def make2DplotMap(lat,long,data2D,varname,datestr):
# Makes 2D plots of selected variables in x = long and y = lat coordinates on the UK map
   # Define plot parameters
   # Set the font dictionaries (for plot title and axis titles)
   ftsb = 14
   ftname = 'Bitstream Vera Sans'   #Default
   axis_font   = ftm.FontProperties(family=ftname, size=ftsb, weight='normal')
   title_font  = ftm.FontProperties(family=ftname, size=ftsb+4, weight='bold')
   labels_font = ftm.FontProperties(family=ftname, size=ftsb+2, weight = 'bold')
   legend_font = ftm.FontProperties(family=ftname, size=ftsb, weight='bold')
   # Define grid of X (longitudes) and Y (latitudes)
   X, Y = np.meshgrid(long, lat);
   # Plot data
   fig, ax = plt.subplots()
   # Calculate map center and corner
   xpltmin = np.min(long);           xpltmax = np.max(long); 
   ypltmin = np.min(lat);            ypltmax = np.max(lat);
   llon0 = 0.5*(xpltmin + xpltmax)
   llat0 = 0.5*(ypltmin + ypltmax)
   # Create map object and draw coastlines
   map = Basemap(resolution='h',lat_0=llat0,lon_0=llon0,llcrnrlon=xpltmin,llcrnrlat=ypltmin,urcrnrlon=xpltmax,urcrnrlat=ypltmax)
   map.drawcoastlines()   
   # Draw parallels
   parmin = 50;  parmax = 60;  parstep = 2;
   parallels = np.arange(parmin,parmax,parstep)
   map.drawparallels(parallels,labels=[1,0,0,0],fontsize=ftsb)
   # Draw meridians
   mermin = -10;  mermax = 2;  merstep = 2;
   meridians = np.arange(mermin,mermax,merstep)
   map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=ftsb)
   # Map data
   cs = map.pcolormesh(X,Y,data2D) 
   # add colorbar.
   cbar = map.colorbar(cs,location='right',pad="5%")
   # Edit axes fonts 
   ax.get_xaxis().set_tick_params(which='both', direction='out')
   ax.get_yaxis().set_tick_params(which='both', direction='out')
   for label in (ax.get_xticklabels() + ax.get_yticklabels()):
       label.set_fontproperties(axis_font)   
   plt.xlabel('Lon', fontproperties = labels_font)
   plt.ylabel('Lat', fontproperties = labels_font)
   title_str = varname + ", " + datestr
   plt.title(title_str, fontproperties = title_font)   
   # Show map
   plt.show()     
   
### ================================================================================= ###   
### ===================================== Main -===================================== ### 
### ================================================================================= ###  

# Load required libraries
import netCDF4 as nc
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import font_manager as ftm
from mpl_toolkits.basemap import Basemap
import time
import datetime
import math
from scipy import interpolate
import matplotlib.mlab as ml
import pickle

### ----- Load netCDF4 data ----- ###
# Define required filenames
fprep = "./output_";
mth = "Jan";  yyy = "2016";  ext = ".nc";
fapp = "_comp_" + mth + yyy + ext;
filenamePM10 = fprep + "pm10" + fapp;      # PM 10
filenamePM25 = fprep + "pm25" + fapp;      # PM 2.5 
filenameNO2 =  fprep + "no2" + fapp;       # NO2
filenameRH =  fprep + "humidity" + fapp;   # Relative Humidity
filenameT = fprep + "temp" + fapp;         # Temperature

# Define variable names
varnamePM10 = "PM10";   
varnamePM25 = "PM25";  
varnameNO2  = "NO2";
varnameRH  = "RH";
varnameT  = "t2m";

# Define extract formats for netCDF4 data (same for all variables)
varlet =  "a";
varformat = "NETCDF4";

# Load aggregated UK PM10 data
filenamestrPM10 = filenamePM10;                                # Filename
varnamePM10 = varnamePM10;                                     # Variable name
ncdataPM10, dataPM10, latitudesPM10, longitudesPM10, timesPM10 = load_netCDF4_compdata(filenamestrPM10, varnamePM10, varlet, varformat);
dataPM10 = dataPM10[0,:,:]                                     # Store to 2D array
ddaydataPM10 = datetime.date.fromtimestamp(int(timesPM10))     # Convert time to date from UNIX timestamp

# Load aggregated UK PM25 data
filenamestrPM25 = filenamePM25;                                # Filename
varnamePM25 = varnamePM25;                                     # Variable name
ncdataPM25, dataPM25, latitudesPM25, longitudesPM25, timesPM25 = load_netCDF4_compdata(filenamestrPM25, varnamePM25, varlet, varformat);
dataPM25 = dataPM25[0,:,:]                                     # Store to 2D array
ddaydataPM25 = datetime.date.fromtimestamp(int(timesPM25))     # Convert time to date from UNIX timestamp

# Load aggregated UK NO2 data
filenamestrNO2 = filenameNO2;                                  # Filename
varnameNO2 = varnameNO2;                                       # Variable name
ncdataNO2, dataNO2, latitudesNO2, longitudesNO2, timesNO2 = load_netCDF4_compdata(filenamestrNO2, varnameNO2, varlet, varformat);
dataNO2 = dataNO2[0,:,:]                                       # Store to 2D array
ddaydataNO2 = datetime.date.fromtimestamp(int(timesNO2))       # Convert time to date from UNIX timestamp

# Load aggregated UK Relative Humidity data
filenamestrRH = filenameRH;                                    # Filename
varnameRH = varnameRH;                                         # Variable name
ncdataRH, dataRH, latitudesRH, longitudesRH, timesRH = load_netCDF4_compdata(filenamestrRH, varnameRH, varlet, varformat);
dataRH = dataRH[0,:,:]                                         # Store to 2D array
ddaydataRH = datetime.date.fromtimestamp(int(timesRH))         # Convert time to date from UNIX timestamp

# Load aggregated UK Temperature data
filenamestrT = filenameT;                                      # Filename
varnameT = varnameT;                                           # Variable name
ncdataT, dataT, latitudesT, longitudesT, timesT = load_netCDF4_compdata(filenamestrT, varnameT, varlet, varformat);
dataT = dataT[0,:,:]  - 273.15;                                # Store to 2D array and convert from K to °C
ddaydataT = datetime.date.fromtimestamp(int(timesT))           # Convert time to date from UNIX timestamp

### ----- Define thresholds for data and interpolate higher resolution data (PM10, PM25 and NO2) 
### ----- to lower resolution Relative Humidity and Temperature 2m data
method = 'linear';
# Find where PM10 values exceed threshold
dataPM10median = np.median(dataPM10)             # Set threshold for PM10 (median of original data for now)
valthr = dataPM10median
dataPM10interp = np.zeros_like(dataT)            # Set interpolated and threshold values to 0
dataPM10thr = np.zeros_like(dataT) 
data2D = dataPM10
dataPM10interp = interpolate2Darray(latitudesPM10,longitudesPM10,data2D,latitudesT,longitudesT,method)   # Interpolate
dataPM10thr = variable2D_over_threshold(dataPM10interp,valthr)

# Find where PM25 values exceed threshold
dataPM25median = np.median(dataPM25)             # Set threshold for PM25 (median of original data for now)
valthr = dataPM25median
dataPM25interp = np.zeros_like(dataT)            # Set interpolated and threshold values to 0
dataPM25thr = np.zeros_like(dataT) 
data2D = dataPM25
dataPM25interp = interpolate2Darray(latitudesPM25,longitudesPM25,data2D,latitudesT,longitudesT,method)   # Interpolate
dataPM25thr = variable2D_over_threshold(dataPM25interp,valthr)

# Find where NO2 values exceed threshold
dataNO2median = np.median(dataNO2)              # Set threshold for NO2 (median of original data for now)
valthr = dataNO2median
dataNO2interp = np.zeros_like(dataT)            # Set interpolated and threshold values to 0
dataNO25thr = np.zeros_like(dataT) 
data2D = dataNO2
dataNO2interp = interpolate2Darray(latitudesNO2,longitudesNO2,data2D,latitudesT,longitudesT,method)     # Interpolate
dataNO2thr = variable2D_over_threshold(dataNO2interp,valthr)

# Find where Relative Humidity values exceed threshold
valthr = 80;                                    # Set threshold to 80% relative humidity
dataRHthr = variable2D_over_threshold(dataRH,valthr)

# Find where Temperature 2m values exceed threshold (UNDER the certain value, not over)
dataTmedian = np.median(dataT)                  # Set threshold for T2m (median of original data for now)
valthr = dataTmedian;
dataTthr = np.zeros_like(dataT)
dataTthr[ np.where( dataT < valthr ) ] = 1

### ----- Find Risk Indices 
RiskIndices = find_risk_index(dataPM10thr,dataPM25thr,dataNO2thr,dataRHthr,dataTthr)

### ----- Save Risk Indices Data
Lat = latitudesT;     
Long = longitudesT;
XLongGrid, YLatGrid = np.meshgrid(Long, Lat);
GridRiskIndices = [Long, Lat, XLongGrid, YLatGrid, RiskIndices];
foutputname = 'RiskIndicesOut';
pickle.dump(GridRiskIndices, open(foutputname, 'w'));

# ------------------------------------- Plot data --------------------------------------

# Define date (Month and Year) for plots
mmmyyy = mth + " " + yyy;

# Working plots, need to figure out how to do in on a map
# Plot PM10 data
latt = latitudesPM10;   long = longitudesPM10;   datain = dataPM10;   varname = varnamePM10; 
make2Dplot(latt,long,datain,varname,mmmyyy)
# Plot PM25 data
latt = latitudesPM25;   long = longitudesPM25;   datain = dataPM25;   varname = varnamePM25;
make2Dplot(latt,long,datain,varname,mmmyyy)
# Plot NO2 data
latt = latitudesNO2;    long = longitudesNO2;    datain = dataNO2;    varname = varnameNO2;
make2Dplot(latt,long,datain,varname,mmmyyy)
# Plot Relative Humidities
latt = latitudesRH;     long = longitudesRH;    datain = dataRH;      varname = varnameRH;
make2Dplot(latt,long,datain,varname,mmmyyy)
# Plot Temperatures
latt = latitudesT;      long = longitudesT;     datain = dataT;       varname = varnameT;
make2Dplot(latt,long,datain,varname,mmmyyy)
# Plot Risk Indices
latt = latitudesT;   longg = longitudesT;   datain = RiskIndices;
make2DplotMap(latt,longg,datain,"Risk Indices (1-5)",mmmyyy)