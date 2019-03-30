
from pymongo import MongoClient, GEOSPHERE, GEO2D


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
        temporal_spatial_querying(db)
    elif op == 7:
        # Spatial Querying using 2D Sphere Index
        spatial_querying_2d_sphere(db)
    elif op == 8:
        # Temporal Querying using 2D Sphere Index
        temporal_querying_2d_sphere(db)
    elif op == 9:
        # Temporal-Spatial Querying using 2D Sphere Index
        temporal_spatial_querying_2d_sphere(db)


def print_collections( db ):
    print( db.collection_names() )


def drop_collections( db ):
    for collection in db.collection_names():
        db.drop_collection( collection )


def insert_data( db ):
    # path_functions.get_json_files( '../../ftp-data/json-files/*' )
    json_files_path_list = input()

    for json_file in json_files_path_list:
        current_collection = 'quikscat-l2b12-' + path_functions.get_file_name( json_file )
        collection_list = db.collection_names()

        if current_collection not in collection_list:
            collection = db[current_collection]
            collection.create_index([("loc", GEO2D)])

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
                {"loc": {"$geoWithin": {"$box": [[-77.49, -89.70], [30.00, 0.00]]}}, "time": 2009001}).limit(3):
            pprint.pprint(doc)


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
            pprint.pprint(doc)


def temporal_querying_2d_sphere( db ):
    collection_list = db.collection_names()
    for current_collection in collection_list:
        collection = db[current_collection]
        for doc in collection.find({"properties.time": 2009002}).limit(3):
            pprint.pprint(doc)


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
                        }}}, "properties.time": 2009003}):
            pprint.pprint(doc)