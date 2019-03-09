import os


def group_json_files_by_days( files_list, path ):
    
    new_json_files = reduce( lambda x, y: x + [y] if not y in x else x,
                        map( lambda file_i: os.path.basename( os.path.dirname( file_i[:-2] + 'json' ) ), files_list ), [] )

    for json_file in new_json_files:
        with open( path + "/" + json_file + '.json', 'w' ) as outfile:
            outfile.write( "{\n\t" + '"'"data"'"' + " : [\n" )
            
            files_by_day = filter( lambda json_d: '/' + json_file + '/' in json_d, 
                            map( lambda file_i: file_i[:-2] + 'json', files_list ) )

            for file_by_day in files_by_day:
                with open( file_by_day, 'r' ) as infile:
                    for line in infile:
                        if line.startswith( "\t\t{" ):
                            outfile.write( line )
                            
                outfile.seek( -1, os.SEEK_END )
                outfile.write( ",\n" )
                os.remove( file_by_day )

            outfile.seek( -2, os.SEEK_END )
            outfile.truncate()

            outfile.write( "\n\t]\n}" )
