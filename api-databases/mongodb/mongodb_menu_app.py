
import os
from database_configuration import database_configuration
from mongodb_operations import operations

def init():
    print( "Welcome to the MongoDB Application Main Menu!\n" )
    print( "What process do you want to execute?\n" )
    print( "\t1. Print Collections\n"
           "\t2. Drop Collections\n"
           "\t3. Insert Data\n"
           "\t4. Spatial Querying using 2D Index\n"
           "\t5. Temporal Querying using 2D Index\n"
           "\t6. Temporal-Spatial Querying using 2D Index\n"
           "\t7. Spatial Querying using 2D Sphere Index\n"
           "\t8. Temporal Querying using 2D Sphere Index\n"
           "\t9. Temporal-Spatial Querying using 2D Sphere Index\n"
           "\t0. Exit\n" )

    op = input()
    db = database_configuration( 27017, 'netcdf_data' )

    operations( op, db )

init()