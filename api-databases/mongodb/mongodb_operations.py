
from pymongo import MongoClient, GEOSPHERE, GEO2D
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions

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


def spatial_querying( db ):
    collection_list = db.collection_names()
    for current_collection in collection_list:
        collection = db[current_collection]
        for doc in collection.find({"loc": {"$geoWithin": {"$box": [[-77.49, -89.70], [30.00, 0.00]]}}}).limit(3):
            pprint.pprint( doc )


def temporal_querying( db ):
    collection_list = db.collection_names()
    for current_collection in collection_list:
        collection = db[current_collection]
        for doc in collection.find({"time": 2009001}).limit(3):
            pprint.pprint( doc )


def temporal_spatial_querying( db ):
    for current_collection in collection_list:
        collection = db[current_collection]
        for doc in collection.find(
                {"loc": {"$geoWithin": {"$box": [[-77.49, -89.70], [30.00, 0.00]]}}, "time": 2009001} ).limit(3):
            pprint.pprint( doc )


def spatial_querying_2d_sphere( db ):
    collection_list = db.collection_names()
    for current_collection in collection_list:
        collection = db[ current_collection ]
        for doc in collection.find(
                {"geometry": {
                    "$geoWithin": {
                        "$geometry": {
                            "type": "Polygon",
                            "coordinates": [ [ [-77.49, -89.70], [0.00, 0.00], [10.00, 10.00], [-77.49, -89.70] ] ]
                        }}}}):
            pprint.pprint( doc )


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