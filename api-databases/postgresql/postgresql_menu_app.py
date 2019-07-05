
import os
from postgresql_configuration import database_configuration
from postgresql_operations import operations

def init():
   
   print( "Welcome to the PostgreSQL Application Main Menu!\n" )
   
   cur, conn = database_configuration( )

   op = -1
   while op != 0:

      print( """\n\n\nWhat process do you want to execute?
               \t1. Create Table
               \t2. Drop Table
               \t3. Insert Data
               \t4. Retrieve Data - Spatial Query
               \t5. Retrieve Data - Temporal Query
               \t6. Retrieve Data - Spatial-Temporal Query
               \t0. Exit\n""" )

      op = input()

      operations( op, cur, conn )
      
   print( """Bye!\n""" )

   
init()