
import os
from cassandra_configuration import database_configuration
from cassandra_operations import operations

def init():
   
   print( "Welcome to the ArangoDB Application Main Menu!\n" )

   op = -1
   while op != 0:

      print( "\n\n\nWhat process do you want to execute?\n" )
      print( "\t1. Create Table\n"
            "\t2. Drop all Collections\n"
            "\t3. Insert Data\n"
            "\t4. Spatial Querying using GEO Index\n"
            "\t5. Temporal Querying using GEO Index\n"
            "\t6. Temporal-Spatial Querying using GEO Index\n"
            "\t0. Exit\n" )

      op = input()
      session = database_configuration( )
   
      operations( op, session )
   
   print( "Bye!\n" )

   
init()