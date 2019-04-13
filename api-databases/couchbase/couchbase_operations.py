
from couchbase.cluster import Cluster
from couchbase.n1ql import N1QLQuery
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions


def operations( op, cb ):
    if op == 1:
        # Print Document from an specific Bucket
        print_bucket_documents( cb )
    elif op == 2:
        # Insert data (JSON or GEOJSON) into any Bucket
        insert_data( cb )


def print_bucket_documents( cb ):
    print( cb.get( 'u:NetCDF_data' ).value )


def insert_data( cb ):

    print( "What type of data do you want to insert?\n" )
    print( "\t1. L3 - WindSAT\n"
           "\t2. L2B12 - QuikSCAT\n"
           "\t3. L2B12 - RapidSCAT\n"
           "\t4. L2 - ASCAT\n" )

    data_type = input()

    print( "What kind of files are you want to insert?\n" )
    print( "\t1. JSON Files\n"
           "\t2. GEOJSON Files\n" )

    files_format = input()

    if files_format == 1:
        files_format = 'json-files'
    elif files_format == 2:
        files_format = 'geojson-files'
    else:
        return

    if data_type == 1:
        json_files_path_list = path_functions.get_json_files( '../../ftp-data/' + files_format + '/windsat-l3' )
        data_type = 'WINDSCAT'
    elif data_type == 2:
        json_files_path_list = path_functions.get_json_files( '../../ftp-data/' + files_format + '/quikscat-l2b12' )
        data_type = 'QUIKSCAT'
    elif data_type == 3:
        json_files_path_list = path_functions.get_json_files( '../../ftp-data/' + files_format + '/rapidscat-l2b12' )
        data_type = 'RAPIDSCAT'
    elif data_type == 4:
        json_files_path_list = path_functions.get_json_files( '../../ftp-data/' + files_format + '/ascat-l2' )
        data_type = 'ASCAT'
    else:
        return

    for json_file in json_files_path_list:
        json_docs = json.load( open( json_file ) )
        for doc in json_docs['data']:
            index = str( doc['time'] ) + '_' + str( doc['loc'][0] ) + str( doc['loc'][1] )
            rv = cb.insert( index, doc )
            print rv
        