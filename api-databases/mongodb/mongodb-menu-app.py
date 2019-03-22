
import os

def init():
    print( "Welcome to the MongoDB Application Main Menu!\n" )
    print( "What process do you want to execute?\n" )
    print( "\t1. Print Collections\n"
           "\t2. Drop Collections\n"
           "\t3. Insert Data\n"
           "\t4. Spatial Querying using 2D Index\n"
           "\t5. Temporal Querying using 2D Index\n"
           "\t6. Temporal-Spatial Querying using 2D Index\n"
           "\t0. Exit\n" )

    op = input()
    print( os.environ[ 'HOME' ] )

    # database_configuration( port, client_name )

init()