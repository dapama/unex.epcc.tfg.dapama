
import os
from postgresql_configuration import database_configuration
from postgresql_operations import operations

def init():
   
   print( "Welcome to the PostgreSQL Application Main Menu!\n" )

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
      cur = database_configuration( )

      operations( op, cur )
      
   print( "Bye!\n" )

   
init()