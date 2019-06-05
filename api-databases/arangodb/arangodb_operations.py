
from couchbase.cluster import Cluster
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
sys.path.insert(0, '../utils')
import data_type_selection
import time


def operations( op, db ):

    if op == 1:
        # Retrieve all Collection
        print_all_collections( db )
    elif op == 2:
        # Drop All Collections
        drop_collections( db )
    elif op == 3:
        # Insert data (JSON or GEOJSON) into Collections
        insert_data( db )
    elif op == 4:
        # Spatial Querying using GEO Index
        spatial_querying( db )
    elif op == 5:
        # Temporal Querying using GEO Index
        temporal_querying( db )
    elif op == 6:
        # Temporal-Spatial Querying using GEO Index
        temporal_spatial_querying( db )


def retrieve_collections( db ):
    return list( filter ( lambda collection: collection['name'][0] != "_", db.collections() ) )


def print_all_collections( db ):
    print 'Collection List: \n'
    for collection in retrieve_collections( db ):
        print collection['name']


def drop_collections( db ):
    collection_list = retrieve_collections( db )

    if not collection_list:
        print 'Currently no collections exist.'
    else:
        for current_collection in collection_list:
            db.delete_collection( current_collection['name'] )
        print 'All collections deleted.'



def insert_data( db ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()

    cnt = 0
    cnt_i = 0

    for json_file in json_files_path_list:
        current_collection = data_type + '_' + path_functions.get_file_name( json_file )

        if db.has_collection( current_collection ):
            collection = db.collection( current_collection )
        else:
            collection = db.create_collection( current_collection )
            collection.add_geo_index( fields = [ 'loc' ] )
            collection.add_hash_index( fields = [ 'time' ] )

        start_time = time.time()

        with open( json_file ) as fp:  
            line = fp.readline().strip()
            while line:
                if line != '[' and line != ']':
                    if ( line.endswith(',') ):
                        line = line[:-1]
                    doc = json.loads( line )

                    collection.insert( doc )

                    line = fp.readline().strip()
                    cnt += 1
                    if cnt == 10000:
                        cnt = 0
                        cnt_i = cnt_i + 1
                        print( 'INSERTED DOCS: ', ( cnt * cnt_i ), 'TIME: ', ( time.time() - start_time ))
                else:
                    line = fp.readline().strip()


def spatial_querying( db ):
   for current_collection in retrieve_collections( db ):
        collection = db.collection( current_collection['name'] )
           
        for doc in collection.find_in_box( -77.49, -89.30, 0.00, 0.00, 0, 0, collection.indexes( )[1]['id'] ):
            pprint.pprint( doc )
        

def temporal_querying( db ):
    for current_collection in retrieve_collections( db ):
        collection = db.collection( current_collection['name'] )

        for doc in collection.find({ 'time': 2008366 }):
            pprint.pprint( doc )

        
def temporal_spatial_querying( db ):
    for current_collection in retrieve_collections( db ):
        collection = db.collection( current_collection['name'] )

        for doc in collection.find_in_box( -77.49, -89.30, 0.00, 0.00, 0, 0, collection.indexes( )[1]['id'] ):
            if doc['time'] == 2008366:
                pprint.pprint( doc )