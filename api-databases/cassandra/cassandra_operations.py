
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
sys.path.insert(0, '../utils')
import data_type_selection
from cassandra.cluster import Cluster


TABLE_NAME = 'netcdf_data'


def operations( op, session ):

    if op == 1:
        # Create simple table
        create_table( session )
    elif op == 2:
        # Drop table
        drop_table( session )
    elif op == 3:
        # Insert data (JSON or GEOJSON) into Collections
        insert_data( session )
    # elif op == 4:
    #     # Spatial Querying using GEO Index
    #     spatial_querying( db )
    # elif op == 5:
    #     # Temporal Querying using GEO Index
    #     temporal_querying( db )
    # elif op == 6:
    #     # Temporal-Spatial Querying using GEO Index
    #     temporal_spatial_querying( db )


def create_table( session ):
    
    session.execute("""
        CREATE TABLE IF NOT EXISTS %s (
            thekey text,
            col1 text,
            col2 text,
            PRIMARY KEY (thekey, col1)
        )
        """ % TABLE_NAME )


def drop_table( session ):
    


def insert_data( session ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()

    for json_file in json_files_path_list:
        # current_collection = data_type + '_' + path_functions.get_file_name( json_file )

        json_docs = json.load( open( json_file ) )
        for doc in json_docs[ 'data' ]:

            session.execute( """CREATE INDEX latlong on University.netcdfdata(loc);""" )


        # session.execute(
        #     """
        #     INSERT INTO users (name, credits)
        #     VALUES (%(name)s, %(credits)s)
        #     """,
        #     {'name': "John O'Reilly", 'credits': 42 }
        # )

        # json_docs = json.load( open( json_file ) )
        # for doc in json_docs[ 'data' ]:
        #     collection.insert( doc )

