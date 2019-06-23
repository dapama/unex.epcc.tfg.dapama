
from pyArango.connection import *


def database_configuration( port, database_name ):

     conn = Connection( )
     # Initialize the ArangoDB client.
     # client = ArangoClient( protocol = 'http', host = 'localhost', port = port )

     # Connect to "_system" database as root user.
     # This returns an API wrapper for "_system" database.
     # sys_db = client.db( '_system' )

     # Create a new database named "netcdf" if it does not exist.
     if not conn.hasDatabase( database_name ):
          db = conn.createDatabase( database_name )
          print ( 'Database created' )

     else: 
          db = conn[ database_name ]

     print ( 'Database: ', db )
     return db
     # return conn.createDatabase( name="netcdf" )