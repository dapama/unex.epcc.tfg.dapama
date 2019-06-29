
from os import listdir
from os.path import isdir, join, isfile, basename, normpath, splitext

def get_json_files( files_path ):
    return [ files_path + '/' + pos_json for pos_json in listdir( files_path ) if pos_json.endswith( '.json' ) ]


def get_file_name( file_path ):
    filename, file_extension = splitext( basename( normpath( file_path ) ) )
    return filename