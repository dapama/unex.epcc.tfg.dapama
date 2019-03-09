
import datetime, gzip, os, shutil


def create_json_from_l2_data( times, latitudes, longitudes, wind_speed, wind_dir, ice_prob, file_nc ):
    
    with open( file_nc + '.json', 'w' ) as outfile:
        outfile.write( "{\n\t" + '"'"data"'"' + " : [\n" )
        
        # for i in range(0, 10):
        for i in range( 0, len( latitudes ) ):
            
            # for j in range(0, 10):
            for j in range( 0, len( latitudes[0] ) ):
                t = time_to_string( times[i][j] )
                la = "{:0.2f}".format( latitudes[i][j] )
                lo = "{:0.2f}".format( longitudes[i][j] )
                ws = string_variable( wind_speed[i][j] )
                wd = string_variable( wind_dir[i][j] )
                ip = string_variable( ice_prob[i][j] )

                 outfile.write( "\t\t{"'"loc"'": [" + lo + ", " + la + "], " +
                                  ""'"time"'": " + t + ", "'"wind_speed"'": " + ws +
                                  ", "'"wind_speed"'": " + ws + ", "'"wind_dir"'": " + wd +
                                  ", " + '"'"ice_prob"'"' ": " + ip + "},\n" )

        outfile.seek( -2, os.SEEK_END )
        outfile.truncate()

        outfile.write( "\n\t]\n}" )
    outfile.close()


def string_variable( var ):
    if str( var ) == "--":
        return "0.00"
    else:
        return "{:0.2f}".format( var )


def time_to_string( time ):
    time += 631148401
    year = datetime.datetime.fromtimestamp( time ).strftime( '%Y' )
    day = datetime.datetime.fromtimestamp( time ).strftime( '%j' )
    date = str( int( year ) * 1000 + int( day ) )
    return date