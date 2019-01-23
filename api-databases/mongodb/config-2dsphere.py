
from pymongo import MongoClient, GEOSPHERE, GEO2D

import os, sys, json, pprint
sys.path.insert(0, '../utils') 
import path_functions 


client = MongoClient( 'localhost', 27017 )
db = client[ 'nfcdata' ]

json_files_path_list = path_functions.get_json_files('../../ftp-data/geojson-files/quikscat-l2b12')

for json_file in json_files_path_list:
    
    current_collection = 'GeoJSON-quikscat-l2b12-' + path_functions.get_file_name( json_file )
    print(current_collection)
    collection_list = db.collection_names()

    if current_collection not in collection_list:
        collection = db[current_collection]
        collection.create_index([( "geometry", GEOSPHERE )])

        json_docs = json.load( open( json_file ) )
        for doc in json_docs['features']:
            collection.insert( doc )


# -- DROP COLLECTIONS --
# collection_list = db.collection_names()
# for collection in collection_list:
#     db.drop_collection(collection)

# -- PRINT COLLECTIONS --
print( db.collection_names() )

# # -- PRINT INDEXES --
# collection_list = db.collection_names()
# for current_collection in collection_list:
#     collection = db[current_collection]
#     print( 'Index: ', sorted( list( collection.index_information() ) ) )

# -- PRINT DATA --
# collection = db['quikscat-l2b12-006']
# cursor = collection.find({})
# for document in cursor:
#     print('\n - - - - - - - DOCUMENTO - - - - - - - \n')
#     print(document)   

# -- SPATIAL QUERYING USING 2D INDEX
collection_list = db.collection_names()
for current_collection in collection_list:
    collection = db[current_collection]
#     for doc in collection.find( { "geometry":{ "$geoWithin": { "$box": [ [ -180 , -180 ], [ 180 , 180 ] ] } } } ).limit(1):
    for doc in collection.find( { "geometry": { "$geoWithin" : { "$geometry" : { type : "Polygon" , "coordinates" : [ [
                                          [ 0 , 0 ] ,
                                          [ 3 , 6 ] ,
                                          [ 6 , 1 ] ,
                                          [ 0 , 0 ]
                                        ] ] } } } } ).limit(1):
        pprint.pprint(doc)

# -- SPATIAL QUERYING USING 2D INDEX
# collection_list = db.collection_names()
# for current_collection in collection_list:
#     collection = db[current_collection]
#     for doc in collection.find( { "properties.time": 2009002 } ).limit(3):
#         pprint.pprint(doc)

# collection = db['quikscat-l2b12-001']
# cursor = collection.find({})
# for document in cursor:
#     pprint.pprint( document )
