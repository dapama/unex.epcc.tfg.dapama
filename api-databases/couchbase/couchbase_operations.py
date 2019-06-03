
from couchbase.cluster import Cluster
from couchbase.n1ql import N1QLQuery
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
import data_type_selection


def operations( op, cb ):
    if op == 1:
        # Print Document from an specific Bucket
        print_bucket_documents( cb )
    elif op == 2:
        # Insert data (JSON or GEOJSON) into any Bucket
        insert_data( cb )
    elif op == 3:
        # Create N1QL index into a Bucket
        create_index( cb )


def print_bucket_documents( cb ):
    print( cb.get( 'u:NetCDF_data' ).value )


def insert_data( cb ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()

    for json_file in json_files_path_list:
        json_docs = json.load( open( json_file ) )
        for doc in json_docs['data']:
            index = str( doc['time'] ) + '_' + str( doc['loc'][0] ) + str( doc['loc'][1] )
            rv = cb.insert( index, doc )
            print ( rv )
        

def create_index( cb ):
    cb.n1ql_query('CREATE PRIMARY INDEX ON TFG_NetCDF(loc)').execute()
