
import os
from arangodb_configuration import database_configuration
from arangodb_operations import operations

def init():
   
   print( "Welcome to the MongoDB Application Main Menu!\n" )

   op = -1
   while op != 0:

      print( "\n\n\nWhat process do you want to execute?\n" )
      print( "\t1. Retrieve all Collections\n"
            "\t2. Drop all Collections\n"
            "\t3. Insert Data\n"
            "\t4. Spatial Querying using GEO Index\n"
            "\t5. Temporal Querying using GEO Index\n"
            "\t6. Temporal-Spatial Querying using GEO Index\n"
            "\t0. Exit\n" )

      op = input()
      db = database_configuration( 8529, 'netcdf' )
   
      operations( op, db )
   
   print( "Bye!\n" )

   
init()