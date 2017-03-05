import netCDF4 as nc


def get_computed_dataset():
    uri = 'datastore/output_index_comp_Jan2016.nc'
    return {
        'computed_values': nc.Dataset(uri).variables['index'][:],
        'latitudes': nc.Dataset(uri).variables['Lat'][:],
        'longitudes': nc.Dataset(uri).variables['Long'][:],
    }


