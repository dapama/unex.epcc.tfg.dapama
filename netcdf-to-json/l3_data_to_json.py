
import datetime, gzip, os, shutil


def create_json_from_l3_data( times, latitudes, longitudes, wind_speed, rain_rate, sea_surface_temperature, file_nc ):
    with open( file_nc + '.json', 'w' ) as outfile:
        outfile.write( "{\n\t" + '"'"data"'"' + " : [\n" )
        # for i in range(0, len(latitudes)):

        for i in range(0, len(times)):
            t = time_to_string(times[i])

            for j in range( 0, len( latitudes ) ):
                la = "{:0.2f}".format( latitudes[j] )
                for k in range( 0, len( longitudes ) ):
                    lo = "{:0.2f}".format( longitudes[k] )
                    ws = string_variable( wind_speed[i][j][k] )
                    # rr = string_variable( rain_rate[i][j][k] )
                    sst = string_variable( sea_surface_temperature[i][j][k] )

                    outfile.write( "\t\t{" + '"'"time"'"' + ": " + t + ", " '"'"lat"'"' + ": " + la +
                                  ", " '"'"lon"'"' + ": " + lo + ", " + '"'"wind_speed"'"' ": " + ws +
                                  ", " + '"'"surface_temperature"'"' ": " + sst + "},\n" )

        outfile.seek( -3, os.SEEK_END )
        outfile.truncate()

        outfile.write( "\n\t]\n}" )
    outfile.close()


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