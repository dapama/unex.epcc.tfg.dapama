
from pymongo import MongoClient, GEOSPHERE, GEO2D

import os, sys, json, pprint
sys.path.insert(0, '../utils') 
import path_functions 


client = MongoClient( 'localhost', 27017 )
db = client[ 'nfcdata' ]

json_files_path_list = path_functions.get_json_files('../../ftp-data/json-files/quikscat-l2b12')

for json_file in json_files_path_list:
    
    current_collection = 'quikscat-l2b12-' + path_functions.get_file_name( json_file )
    collection_list = db.collection_names()

    if current_collection not in collection_list:
        collection = db[current_collection]
        collection.create_index([( "loc", GEO2D )])

        json_docs = json.load( open( json_file ) )
        for doc in json_docs['data']:
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
    for doc in collection.find( { "loc": { "$geoWithin": { "$box": [ [-77.49, -89.70], [0.00, 0.00] ] } } } ).limit(3):
        pprint.pprint(doc)

# -- TEMPORAL QUERYING USING 2D INDEX
# collection_list = db.collection_names()
# for current_collection in collection_list:
#     collection = db[current_collection]
#     for doc in collection.find( { "time": 2009001 } ).limit(3):
#         pprint.pprint(doc)

# -- TEMPORAL-SPATIAL QUERYING USING 2D INDEX


# collection = db['quikscat-l2b12-001']
# cursor = collection.find({})
# for document in cursor:
#     pprint.pprint( document )
