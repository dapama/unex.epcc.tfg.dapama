
from pymongo import MongoClient
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions

def database_configuration( port, client_name ):

    client = MongoClient( 'localhost', port )
    db = client[ client_name ]

    return db
