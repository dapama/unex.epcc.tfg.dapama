import datetime
import gzip
import os
import shutil
from netCDF4 import Dataset
from read_nc import read_vars


format_type = "NETCDF3_CLASSIC"

# RapidSCAT / QuikSCAT
def extract_data_list_l2b12_GeoJSON( files_list ):
    for file_i in files_list:
        with gzip.open( file_i, 'rb' ) as f_in:
            with open( file_i[:-3], 'wb' ) as f_out:
                shutil.copyfileobj( f_in, f_out )
                l2b12_net_cdf_to_geojson( file_i[:-3] )
            # f_out.close()
        f_in.close()
        os.remove( file_i[:-3] )


def l2b12_net_cdf_to_geojson( file_nc ):
    try:
        nc = Dataset( file_nc, 'r' )
        if nc.file_format == format_type:
            [vars, var_attr_list, var_data_list] = read_vars( nc )

            times = var_data_list[0]
            latitudes = var_data_list[1]
            longitudes = var_data_list[2]
            wind_speed = var_data_list[3]
            wind_dir = var_data_list[4]
            rain_rate = var_data_list[5]

            with open( file_nc + '.json', 'w' ) as outfile:
                outfile.write( "{\n\t" + '"'"type"'"' + " : "'"FeatureCollection"'",\n\t" +
                '"'"features"'"'  + " : [\n" )
                for i in range( 0, len( latitudes ) ):
                    t = time_to_string(times[i])
                    for j in range( 0, len(latitudes[0] ) ):
                        lo = "{:0.2f}".format( longitudes[i][j] - 180 )
                        la = "{:0.2f}".format( latitudes[i][j] )
                        ws = string_variable( wind_speed[i][j] )
                        wd = string_variable( wind_dir[i][j] )
                        rr = string_variable( rain_rate[i][j] )

                        outfile.write( "\t\t{ "'"type"'" :  "'"Feature"'", "'"geometry"'": { " +
                                      ""'"type"'": "'"Point"'", "'"coordinates"'": [" + lo + ", " + la + "] }, " +
                                      ""'"properties"'": { "'"time"'": " + t + ", "'"wind_speed"'" : " + ws + ", "
                                      ""'"wind_dir"'": " + wd + ", "'"rain"'": " + rr + "} },\n" )

                outfile.seek( -2, os.SEEK_END )
                outfile.truncate()

                outfile.write( "\n\t]\n}" )
            outfile.close()

        nc.close()
    except IOError:
        print( 'not a valid netCDF file' )


def l2b12_group_geojson_files_by_days_GeoJSON( files_list, dst_path ):
    path = dst_path
    new_json_files = reduce(lambda x, y: x + [y] if not y in x else x,
                            map(lambda file_i: os.path.basename(os.path.dirname(file_i[:-2] + 'json')), files_list), [])

    print ( 'JSON FILES: ', new_json_files )

    for json_file in new_json_files:
        print( 'JSON NAME: ', json_file )
        with open(path + "/" + json_file + '.json', 'w') as outfile:
            outfile.write("{\n\t"'"type"'": "'"FeatureCollection"'",\n\t"'"features"'": [\n")
            # Read all the data days
            files_by_day = filter(lambda json_d: '/' + json_file + '/' in json_d, map(lambda file_i: file_i[:-2] + 'json', files_list))

            print ( 'FILES BY DAY: ', files_by_day )

            for file_by_day in files_by_day:
                # print(file_by_day)
                with open(file_by_day, 'r') as infile:
                    for line in infile:
                        if line.startswith("\t\t{"):
                            outfile.write(line)
                outfile.seek(-1, os.SEEK_END)
                outfile.write(",\n")
                # os.remove(file_by_day)

            outfile.seek(-2, os.SEEK_END)
            outfile.truncate()

            outfile.write("\n\t]\n}")


def string_variable(var):
    if str(var) == "--":
        return "0.00"
    else:
        return "{:0.2f}".format(var)


def time_to_string(time):
    time += 915145200
    year = datetime.datetime.fromtimestamp(time).strftime('%Y')
    day = datetime.datetime.fromtimestamp(time).strftime('%j')
    date = str(int(year) * 1000 + int(day))
    return date
