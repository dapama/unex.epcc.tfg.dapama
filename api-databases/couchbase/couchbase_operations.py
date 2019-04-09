
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


def insert_data( db ):

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
        json_files_path_list = path_functions.get_json_files( '../../ftp-data/' + files_format-files + '/windsat-l3' )
        data_type = 'WINDSCAT'
    elif data_type == 2:
        json_files_path_list = path_functions.get_json_files( '../../ftp-data/json-files/quikscat-l2b12' )
        data_type = 'QUIKSCAT'
    elif data_type == 3:
        json_files_path_list = path_functions.get_json_files( '../../ftp-data/json-files/rapidscat-l2b12' )
        data_type = 'RAPIDSCAT'
    elif data_type == 4:
        json_files_path_list = path_functions.get_json_files( '../../ftp-data/json-files/ascat-l2' )
        data_type = 'ASCAT'
    else:
        return

    for json_file in json_files_path_list:
        current_collection = data_type + '_' + path_functions.get_file_name( json_file )
        collection_list = db.collection_names()

        if current_collection not in collection_list:
            collection = db[ current_collection ]
            collection.create_index([( "loc", GEO2D )])

            json_docs = json.load( open( json_file ) )
            for doc in json_docs['data']:
                collection.insert( doc )