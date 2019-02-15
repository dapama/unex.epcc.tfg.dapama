
def create_json_from_l3_data():
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