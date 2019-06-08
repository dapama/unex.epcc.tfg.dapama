
from pymongo import MongoClient

def database_configuration( port, client_name ):

    client = MongoClient( 'localhost', port )
    db = client[ client_name ]

    return db
