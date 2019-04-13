
from couchbase.cluster import Cluster
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
sys.path.insert(0, '../utils')
import data_type_selection


def operations( op, db ):
    if op == 1:
        # Print Document from an specific Collection
        print_collection_documents( db )
    elif op == 2:
        # Insert data (JSON or GEOJSON) into Collections
        insert_data( db )


def print_bucket_documents( db ):
    print( db.get() )


def insert_data( db ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()

    for json_file in json_files_path_list:
        print 'JSON FILE: ', json_file
        current_collection = data_type + '_' + path_functions.get_file_name( json_file )

        if db.has_collection( current_collection ):
            collection = db.collection( current_collection )
        else:
            collection = db.create_collection( current_collection )
            collection.add_geo_index( fields = [ 'loc' ] )

        json_docs = json.load( open( json_file ) )
        for doc in json_docs[ 'data' ]:
            collection.insert( doc )
        
