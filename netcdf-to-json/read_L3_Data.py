import datetime, gzip, os, shutil
from functools import reduce
from read_nc import read_vars
from netCDF4 import Dataset

format_type = 'NETCDF3_CLASSIC'

# WindSAT
def extract_data_list_l3( files_list ):
    for file_i in files_list:
        with gzip.open( file_i, 'rb' ) as f_in:
            with open( file_i[:-3], 'wb' ) as f_out:
                shutil.copyfileobj( f_in, f_out )
                l3_net_cdf_to_json( file_i[:-3] )
        f_in.close()
        os.remove( file_i[:-3] )


def l3_net_cdf_to_json( file_nc ):
    try:
        nc = Dataset( file_nc, 'r' )
        if nc.file_format == format_type:
            [vars, var_attr_list, var_data_list] = read_vars( nc )

            times = var_data_list[2]
            latitudes = var_data_list[0]
            longitudes = var_data_list[1]
            wind_speed = var_data_list[8]
            # rain_rate = var_data_list[5]
            sea_surface_temperature = var_data_list[3]

            # flag = True


        nc.close()
    except IOError:
        print('not a valid netCDF file')


def l3_group_json_files_by_days(files_list, dst_path):
    path = dst_path
    new_json_files = reduce(lambda x, y: x + [y] if not y in x else x,
                            map(lambda file_i: os.path.basename(os.path.dirname(file_i[:-2] + 'json')), files_list), [])

    for json_file in new_json_files:
        with open(path + "\\" + json_file + '.json', 'w') as outfile:
            outfile.write("{\n\t" + '"'"data"'"' + " : [\n")
            # Read all the data days
            files_by_day = filter(lambda json_d: json_file in json_d,
                                  map(lambda file_i: file_i[:-2] + 'json', files_list))

            for file_by_day in files_by_day:
                # print(file_by_day)
                with open(file_by_day, 'r') as infile:
                    for line in infile:
                        if line.startswith("\t\t{"):
                            outfile.write(line)
                outfile.seek(-2, os.SEEK_END)
                outfile.write(",\n")
                os.remove(file_by_day)

            outfile.seek(-3, os.SEEK_END)
            outfile.truncate()

            outfile.write("\n\t]\n}")


def string_variable(var):
    if str(var) == "--":
        return "0.00"
    else:
        return "{:0.2f}".format(var)


def time_to_string(time):
    time += 347151601
    year = datetime.datetime.fromtimestamp(time).strftime('%Y')
    day = datetime.datetime.fromtimestamp(time).strftime('%j')
    date = str(int(year) * 1000 + int(day))
    return date


def retrieve_l3_data( var_data_list ):
    print 'asd'
