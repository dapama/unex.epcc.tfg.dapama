
import os, sys, json, pprint
from path_functions import get_json_files

def data_type_selection( ):
    
    print( "What type of data do you want to insert?\n" )
    print( "\t1. L3 - WindSAT\n"
           "\t2. L2B12 - QuikSCAT\n"
           "\t3. L2B12 - RapidSCAT\n"
           "\t4. L2 - ASCAT\n" )

    data_type = input()

    print( "What kind of files do you want to insert?\n" )
    print( "\t1. JSON Files - 2D index\n"
           "\t2. GEOJSON Files - 2d Sphere index\n" )

    files_format = input()

    if files_format == 1:
        files_format = 'json-files'
    elif files_format == 2:
        files_format = 'geojson-files'
    else:
        return

    if data_type == 1:
        json_files_path_list = get_json_files( '../../ftp-data/' + files_format + '/windsat-l3' )
        data_type = 'WINDSCAT'
    elif data_type == 2:
        json_files_path_list = get_json_files( '../../ftp-data/' + files_format + '/quikscat-l2b12' )
        data_type = 'QUIKSCAT'
    elif data_type == 3:
        json_files_path_list = get_json_files( '../../ftp-data/' + files_format + '/rapidscat-l2b12' )
        data_type = 'RAPIDSCAT'
    elif data_type == 4:
        json_files_path_list = get_json_files( '../../ftp-data/' + files_format + '/ascat-l2' )
        data_type = 'ASCAT'
    else:
        return

    return json_files_path_list, data_type