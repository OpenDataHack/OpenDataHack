def calc_humidity(temp, dewpoint):
    '''
    calculates the humidity via the formula from weatherwise.org
    return the relative humidity
    '''

    t = fahrenheit_to_celsius(temp)
    td = fahrenheit_to_celsius(dewpoint)

    num = 112 - (0.1 * t) + td
    denom = 112 + (0.9 * t)

    rh = math.pow((num / denom), 8)
    
    return rh

def kelvin_to_fahrenheit(k):
    'Degrees Kelvin (K) to degrees Fahrenheit (F)'
    return (k - 255.37) * 1.8

def fahrenheit_to_celsius(f):
    'Degrees Fahrenheit (F) to degrees Celsius (C)'
    return (f - 32.0) * 0.555556


import math
import netCDF4 as nc
import numpy as np

infile = nc.Dataset('/home/rsgadmin/Downloads/humtest_comp.nc')

outfile = nc.Dataset('/home/rsgadmin/jan_rel_humid.nc','r+')

dew = infile.variables['d2m'][:]
t = infile.variables['t2m'][:]
time = infile.variables['time'][:]

print infile.dimensions.keys()

outVar = outfile.createVariable("RH", infile.variables['d2m'].datatype, ("time", "latitude", "longitude"))

# Copy variable attributes

print dew.shape
print t.shape

outarr = np.empty(dew.shape)

for a in range(dew.shape[0]):
    for x in range(dew.shape[1]):
        for y in range(dew.shape[2]):
            outarr[a,x,y] = 100*calc_humidity(kelvin_to_fahrenheit(t[a,x,y]),kelvin_to_fahrenheit(dew[a,x,y]))

outVar[:]=outarr[:]

outfile.close()

