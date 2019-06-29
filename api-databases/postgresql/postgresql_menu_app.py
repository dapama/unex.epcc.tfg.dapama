
import os
from postgresql_configuration import database_configuration
from postgresql_operations import operations

def init():
   
   print( "Welcome to the PostgreSQL Application Main Menu!\n" )
   
   cur, conn = database_configuration( )

   op = -1
   while op != 0:

      print( """\n\n\nWhat process do you want to execute?\n
               \t1. Create Table\n
               \t2. Drop Table\n
               \t3. Insert Data\n
               \t4. Retrieve Data - Spatial Query\n
               \t5. Retrieve Data - Temporal Query\n
               \t6. Retrieve Data - Spatial-Temporal Query\n
               \t0. Exit\n""" )

      op = input()

      operations( op, cur, conn )
      
   print( """Bye!\n""" )

   
init()