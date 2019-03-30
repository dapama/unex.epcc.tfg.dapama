
from os import listdir
from os.path import isdir, join, isfile


def get_files_data( path, files_list, extension ):
        if isdir( path ):
            for f in listdir( path ):
                get_files_data( join( path, f ), files_list, extension )
        else:
            if path.endswith( extension ) and isfile( path ):
                files_list.append( path )
