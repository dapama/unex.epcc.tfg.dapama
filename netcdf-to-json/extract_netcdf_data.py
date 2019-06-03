import datetime, gzip, os, shutil
from functools import reduce
from read_nc import read_vars
from netCDF4 import Dataset
from l3_data_to_json import create_json_from_l3_data, create_geojson_from_l3_data
from l2_data_to_json import create_json_from_l2_data, create_geojson_from_l2_data
from l2b12_data_to_json import create_json_from_l2b12_data, create_geojson_from_l2b12_data

format_type = 'NETCDF3_CLASSIC'


def extract_data( files_list, type_of_file, is_geojson_file ):
    for file_i in files_list:
        with gzip.open( file_i, 'rb' ) as f_in:
            with open( file_i[:-3], 'wb' ) as f_out:
                shutil.copyfileobj( f_in, f_out )
                net_cdf_to_json( file_i[:-3], type_of_file, is_geojson_file )
                
        f_in.close()
        os.remove( file_i[:-3] )

def net_cdf_to_json( file_nc, type_of_file, is_geojson_file ):
    try:
        nc = Dataset( file_nc, 'r' )
        if nc.file_format == format_type:
            var_data_list = read_vars( nc )

            attr1, attr2, attr3, attr4, attr5, attr6 = read_net_cdf_data( var_data_list, type_of_file )

            if type_of_file == 'L3':
                if is_geojson_file == False:
                    create_json_from_l3_data( attr1, attr2, attr3, attr4, attr5, attr6, file_nc )
                elif is_geojson_file == True:
                    create_geojson_from_l3_data( attr1, attr2, attr3, attr4, attr5, attr6, file_nc )

            elif type_of_file == 'L2B12':
                if is_geojson_file == False:
                    create_json_from_l2b12_data( attr1, attr2, attr3, attr4, attr5, attr6, file_nc )
                elif is_geojson_file == True:
                    create_geojson_from_l2b12_data( attr1, attr2, attr3, attr4, attr5, attr6, file_nc )
            
            elif type_of_file == 'L2':
                if is_geojson_file == False:
                    create_json_from_l2_data( attr1, attr2, attr3, attr4, attr5, attr6, file_nc )
                elif is_geojson_file == True:
                    create_geojson_from_l2_data( attr1, attr2, attr3, attr4, attr5, attr6, file_nc )
                
        nc.close()
    except IOError:
        print( 'not a valid netCDF file' )


def read_net_cdf_data ( data, type_of_file ):
    
    if type_of_file == 'L3':
        # times, latitudes, longitudes, wind_speed, rain_rate, sea_surface_temperature
        return data[2], data[0], data[1], data[8], data[5], data[3]

    elif  type_of_file == 'L2B12':
        # times, latitudes, longitudes, wind_speed, wind_dir, rain_rate
        return data[0], data[1], data[2], data[3], data[4], data[5]
         
    elif  type_of_file == 'L2':
        # times, latitudes, longitudes, wind_speed, wind_dir, ice_prob
        return data[0], data[1], data[2], data[9], data[10], data[6]

