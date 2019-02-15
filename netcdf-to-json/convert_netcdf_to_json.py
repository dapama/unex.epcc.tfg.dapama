import datetime, gzip, os, shutil
from functools import reduce
from read_nc import read_vars
from netCDF4 import Dataset

format_type = 'NETCDF3_CLASSIC'


def extract_data( files_list, type_of_file ):
    for file_i in files_list:
        with gzip.open( file_i, 'rb' ) as f_in:
            with open( file_i[:-3], 'wb' ) as f_out:
                shutil.copyfileobj( f_in, f_out )
                net_cdf_to_json( file_i[:-3], type_of_file )
        f_in.close()
        os.remove( file_i[:-3] )


def read_net_cdf_data ( data, type_of_file ):
    if type_of_file == 'L3':
        # times, latitudes, longitudes, wind_speed, rain_rate, sea_surface_temperature
        return data[2], data[0], data[1], data[8], data[5], data[3]


def net_cdf_to_json( file_nc, type_of_file ):
    try:
        nc = Dataset(file_nc, 'r')
        if nc.file_format == format_type:
            var_data_list = read_vars(nc)

            times, latitudes, longitudes, wind_speed, rain_rate, sea_surface_temperature \
                = read_net_cdf_data ( var_data_list, type_of_file )

            with open( file_nc + '.json', 'w' ) as outfile:
                outfile.write( "{\n\t" + '"'"data"'"' + " : [\n" )

                # for i in range(0, len(latitudes)):
                for i in range(0, len(times)):
                    t = time_to_string(times[i])

                    for j in range(0, len(latitudes)):
                        la = "{:0.2f}".format(latitudes[j])
                        for k in range(0, len(longitudes)):
                            lo = "{:0.2f}".format(longitudes[k])
                            ws = string_variable(wind_speed[i][j][k])
                            # rr = string_variable(rain_rate[i][j][k])
                            sst = string_variable(sea_surface_temperature[i][j][k])

                            outfile.write("\t\t{" + '"'"time"'"' + ": " + t + ", " '"'"lat"'"' + ": " + la +
                                          ", " '"'"lon"'"' + ": " + lo + ", " + '"'"wind_speed"'"' ": " + ws +
                                          ", " + '"'"surface_temperature"'"' ": " + sst + "},\n")

                outfile.seek(-3, os.SEEK_END)
                outfile.truncate()

                outfile.write("\n\t]\n}")
            outfile.close()

        nc.close()
    except IOError:
        print('not a valid netCDF file')