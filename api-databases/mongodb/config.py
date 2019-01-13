
from pymongo import MongoClient
import os, sys, json
sys.path.insert(0, '../utils')
import path_functions 


client = MongoClient('localhost', 27017)
db = client['nfcdata']

print(db.collection_names())        #Return a list of collections in 'testdb1'


# json_files_path_list = path_functions.get_json_files('../../ftp-data/json-files/quikscat-l2b12')

# for json_file in json_files_path_list:
#     collection = db['quikscat-l2b12-' + path_functions.get_file_name( json_file )]
    # with open(json_files) as f:
        # print('FILE: ', f, '\n - ', json.load(f)['data'])
        # collection.insert_one(json.load(f))