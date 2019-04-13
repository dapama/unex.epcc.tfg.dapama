
import os
from couchbase_configuration import database_configuration
from couchbase_operations import operations

def init():
    print( "Welcome to the CouchDB Application Main Menu!\n" )
    print( "What process do you want to execute?\n" )
    print( "\t1. Print Document from an specific Bucket\n"
           "\t2. Insert data (JSON or GEOJSON) into any Bucket\n"
           "\t3. Create N1QL index into a Bucket\n"
           # "\t4. Spatial Querying using 2D Index\n"
           # "\t5. Temporal Querying using 2D Index\n"
           # "\t6. Temporal-Spatial Querying using 2D Index\n"
           # "\t7. Spatial Querying using 2D Sphere Index\n"
           # "\t8. Temporal Querying using 2D Sphere Index\n"
           # "\t9. Temporal-Spatial Querying using 2D Sphere Index\n"
           "\t0. Exit\n" )

    op = input()
    cb = database_configuration( )

    operations( op, cb )

init()