
from pymongo import MongoClient
import os, sys, json
sys.path.insert(0, '../utils') 
import path_functions 


client = MongoClient('localhost', 27017)
db = client['nfcdata']

# json_files_path_list = path_functions.get_json_files('../../ftp-data/json-files/quikscat-l2b12')

# for json_file in json_files_path_list:
#     collection = db['quikscat-l2b12-' + path_functions.get_file_name( json_file )]
#     with open( json_file ) as f:
#         file_data = json.load(f)

#     # print('FILE: ', f, '\n - ', json.load(f)['data'])
#     collection.insert( file_data )

print(db.collection_names())        #Return a list of collections in 'testdb1'

collection = db['quikscat-l2b12-001']
cursor = collection.find({})
# print ( type( cursor ) )
for document in cursor:
    print(document)

