
from pymongo import MongoClient, GEOSPHERE, GEO2D
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
import time
import data_type_selection


def operations( op, db ):
    if op == 1:
        # Print Collections
        print_collections( db )
    elif op == 2:
        # Drop Collections
        drop_collections( db )
    elif op == 3:
        # Insert Data
        insert_data( db )
    elif op == 4:
        # Spatial Querying using 2D Index
        spatial_querying( db )
    elif op == 5:
        # Temporal Querying using 2D Index
        temporal_querying( db )
    elif op == 6:
        # Temporal-Spatial Querying using 2D Index
        temporal_spatial_querying( db )
    elif op == 7:
        # Spatial Querying using 2D Sphere Index
        spatial_querying_2d_sphere( db )
    elif op == 8:
        # Temporal Querying using 2D Sphere Index
        temporal_querying_2d_sphere( db )
    elif op == 9:
        # Temporal-Spatial Querying using 2D Sphere Index
        temporal_spatial_querying_2d_sphere( db )


def print_collections( db ):
    print( db.collection_names() )


def drop_collections( db ):
    for collection in db.collection_names():
        db.drop_collection( collection )


def insert_data( db ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()

    cnt = 0
    cnt_i = 0

    for json_file in json_files_path_list:
        current_collection = data_type + '_' + path_functions.get_file_name( json_file )
        collection_list = db.collection_names()

        if current_collection not in collection_list:
            collection = db[ current_collection ]
            collection.create_index([( "loc", GEO2D )])

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
                    cnt = cnt + 1
                    if cnt == 10000:
                        cnt_i = cnt_i + 1
                        print( 'INSERTED DOCS: ', ( cnt * cnt_i ), 'TIME: ', ( time.time() - start_time ))
                        cnt = 0
                else:
                    line = fp.readline().strip()


def spatial_querying( db ):
    collection_list = db.collection_names()
    for current_collection in collection_list:
        collection = db[current_collection]

        print( 'RETRIEVED DOCS: ', len(
            collection.find({"loc": {"$geoWithin": {"$box": [[-77.49, -89.70], [30.00, 0.00]]}}})
        ), 'TIME: ', ( time.time() - start_time ))


def temporal_querying( db ):
    collection_list = db.collection_names()
    for current_collection in collection_list:
        collection = db[current_collection]

        print( 'RETRIEVED DOCS: ', len(
            collection.find({"time": 2009001})
        ), 'TIME: ', ( time.time() - start_time ))


def temporal_spatial_querying( db ):
    for current_collection in collection_list:
        collection = db[current_collection]

        print( 'RETRIEVED DOCS: ', len(
            collection.find({"loc": {"$geoWithin": {"$box": [[-77.49, -89.70], [30.00, 0.00]]}}, "time": 2009001} )
        ), 'TIME: ', ( time.time() - start_time ))


def spatial_querying_2d_sphere( db ):
    collection_list = db.collection_names()
    for current_collection in collection_list:
        collection = db[ current_collection ]

        docs = collection.find(
                {"geometry": {
                    "$geoWithin": {
                        "$geometry": {
                            "type": "Polygon",
                            "coordinates": [ [ [-77.49, -89.70], [0.00, 0.00], [10.00, 10.00], [-77.49, -89.70] ] ]
                        }}}})
            # pprint.pprint( doc )

        print( 'RETRIEVED DOCS: ', len(docs), 'TIME: ', ( time.time() - start_time ))


def temporal_querying_2d_sphere( db ):
    collection_list = db.collection_names()
    for current_collection in collection_list:
        collection = db[current_collection]
        for doc in collection.find( {"properties.time": 2009002} ).limit(3):
            pprint.pprint( doc )


def temporal_spatial_querying_2d_sphere( db ):
    collection_list = db.collection_names()
    for current_collection in collection_list:
        collection = db[current_collection]

        for doc in collection.find(
                {"geometry": {
                    "$geoWithin": {
                        "$geometry": {
                            "type": "Polygon",
                            "coordinates": [ [ [-77.49, -89.70], [0.00, 0.00], [10.00, 10.00], [-77.49, -89.70] ] ]
                        }}}, "properties.time": 2009003} ):
            pprint.pprint( doc )
