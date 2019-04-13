
from arango import ArangoClient

"""
https://buildmedia.readthedocs.org/media/pdf/python-driver-for-arangodb/3.12.1/python-driver-for-arangodb.pdf

"""

def database_configuration( port, database_name ):

    # Initialize the ArangoDB client.
     client = ArangoClient( protocol = 'http', host = 'localhost', port = port )

     # Connect to "_system" database as root user.
     # This returns an API wrapper for "_system" database.
     sys_db = client.db( '_system' )

     # Create a new database named "netcdf" if it does not exist.
     if not sys_db.has_database( database_name ):
          sys_db.create_database( database_name )

     return client.db( database_name )