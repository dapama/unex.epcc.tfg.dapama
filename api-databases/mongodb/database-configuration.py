
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions

def database_configuration( port, client_name ):

    client = MongoClient( 'localhost', 27017 )
    db = client[ 'nfcdata' ]

    return db
