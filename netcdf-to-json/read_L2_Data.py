import datetime
import gzip
import os
import shutil
from netCDF4 import Dataset
from read_nc import read_vars


format_type = "NETCDF3_CLASSIC"

# ASCAT
def extract_data_list_l2(files_list):
    for file_i in files_list:
        with gzip.open(file_i, 'rb') as f_in:
            with open(file_i[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                l2_net_cdf_to_json(file_i[:-3])
            # f_out.close()
        f_in.close()
        os.remove(file_i[:-3])


def l2_net_cdf_to_json(file_nc):
    try:
        nc = Dataset(file_nc, 'r')
        if nc.file_format == format_type:
            [vars, var_attr_list, var_data_list] = read_vars(nc)

            times = var_data_list[0]
            latitudes = var_data_list[1]
            longitudes = var_data_list[2]
            wind_speed = var_data_list[9]
            wind_dir = var_data_list[10]
            ice_prob = var_data_list[6]

            with open(file_nc + '.json', 'w') as outfile:
                outfile.write("{\n\t" + '"'"data"'"' + " : [\n")
                # for i in range(0, len(latitudes)):
                for i in range(0, 10):
                    # for j in range(0, len(latitudes[0])):
                    for j in range(0, 10):
                        t = time_to_string(times[i][j])
                        la = "{:0.2f}".format(latitudes[i][j])
                        lo = "{:0.2f}".format(longitudes[i][j])
                        ws = string_variable(wind_speed[i][j])
                        wd = string_variable(wind_dir[i][j])
                        ip = string_variable(ice_prob[i][j])

                        outfile.write("\t\t{" + '"'"time"'"' + ": " + t + ", " '"'"lat"'"' + ": " + la +
                                      ", " '"'"lon"'"' + ": " + lo + ", " + '"'"wind_speed"'"' ": " + ws +
                                      ", " + '"'"wind_dir"'"' ": " + wd + ", " + '"'"ice_prob"'"' ": " + ip + "},\n")

                outfile.seek(-3, os.SEEK_END)
                outfile.truncate()

                outfile.write("\n\t]\n}")
            outfile.close()

        nc.close()
    except IOError:
        print('not a valid netCDF file')


def l2_group_json_files_by_days(files_list, dst_path):
    path = dst_path
    new_json_files = reduce(lambda x, y: x + [y] if not y in x else x,
                            map(lambda file_i: os.path.basename(os.path.dirname(file_i[:-2] + 'json')), files_list), [])

    # [004 003 002 001]
    print(new_json_files)
    new_json_files.sort()
    print(new_json_files)

    for json_file in new_json_files:
        with open(path + json_file + '.json', 'w') as outfile:
            outfile.write("{\n\t" + '"'"data"'"' + " : [\n")
            # Read all the data days
            files_by_day = filter(lambda json_d: '/'+json_file+'/' in json_d,
                                  map(lambda file_i: file_i[:-2] + 'json', files_list))

            files_by_day.sort()
            print(files_by_day)
            for file_by_day in files_by_day:
                print(file_by_day)
                with open(file_by_day, 'r') as infile:
                    for line in infile:
                        if line.startswith("\t\t{"):
                            outfile.write(line)
                outfile.seek(-2, os.SEEK_END)
                outfile.write("},\n")
                os.remove(file_by_day)

            print('------------')

            outfile.seek(-3, os.SEEK_END)
            outfile.truncate()

            outfile.write("}\n\t]\n}")


def string_variable(var):
    if str(var) == "--":
        return "0.00"
    else:
        return "{:0.2f}".format(var)


def time_to_string(time):
    time += 631148401
    year = datetime.datetime.fromtimestamp(time).strftime('%Y')
    day = datetime.datetime.fromtimestamp(time).strftime('%j')
    date = str(int(year) * 1000 + int(day))
    return date
