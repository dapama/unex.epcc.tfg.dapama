import datetime, gzip, os, shutil
from functools import reduce
from read_nc import read_vars
from netCDF4 import Dataset
from l3_data_to_json import create_json_from_l3_data

format_type = 'NETCDF3_CLASSIC'


def extract_data( files_list, type_of_file ):
    for file_i in files_list:
        with gzip.open( file_i, 'rb' ) as f_in:
            with open( file_i[:-3], 'wb' ) as f_out:
                shutil.copyfileobj( f_in, f_out )
                net_cdf_to_json( file_i[:-3], type_of_file )
        f_in.close()
        os.remove( file_i[:-3] )


def net_cdf_to_json( file_nc, type_of_file ):
    try:
        nc = Dataset(file_nc, 'r')
        if nc.file_format == format_type:
            var_data_list = read_vars(nc)

            times, latitudes, longitudes, wind_speed, rain_rate, sea_surface_temperature = \
                read_net_cdf_data ( var_data_list, type_of_file )

            create_json_from_l3_data\
                ( times, latitudes, longitudes, wind_speed, rain_rate, sea_surface_temperature, file_nc )

        nc.close()
    except IOError:
        print('not a valid netCDF file')


def read_net_cdf_data ( data, type_of_file ):
    if type_of_file == 'L3':
        # times, latitudes, longitudes, wind_speed, rain_rate, sea_surface_temperature
        return data[2], data[0], data[1], data[8], data[5], data[3]

