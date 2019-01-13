
from pymongo import MongoClient, GEOSPHERE, GEO2D

import os, sys, json
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
        collection.ensure_index([( "time", GEO2D )])
        with open( json_file ) as f:
            file_data = json.load(f)

        collection.insert( file_data )

# collection = db['quikscat-l2b12-001']
# cursor = collection.find({})
# for document in cursor:
#     print(document)

# collection = db['quikscat-l2b12-001']

# -- DROP COLLECTIONS --
collection_list = db.collection_names()
for collection in collection_list:
    db.drop_collection(collection)

# -- PRINT COLLECTIONS --
print( db.collection_names() )

# -- CHECK COLLECTION INDEXES --
# collection_list = db.collection_names()
# for collection in collection_list:
#     print ( collection.getIndexes() )

# -- INDEXES --
for index in db.system.indexes.find():
    print( index )

