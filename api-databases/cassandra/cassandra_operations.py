
import os, sys, json, pprint
import pandas as pd
import ijson
sys.path.insert(0, '../utils')
import path_functions
sys.path.insert(0, '../utils')
import data_type_selection
from cassandra.cluster import Cluster
import time


TABLE_NAME = 'netcdf_data'
QUERY_WHERE = '-5.49-10.30'


def operations( op, session ):

    if op == 1:
        # Create simple table
        create_table( session )
    elif op == 2:
        # Drop table
        drop_table( session )
    elif op == 3:
        # Insert data
        insert_data( session )
    elif op == 4:
        # Retrieve data
        retrieve_data( session )


def create_table( session ):
    
    session.execute("""
        CREATE TABLE IF NOT EXISTS %s (
            loc text,
            time int,
            wind_speed float,
            rain_rate float,
            sea_surface_temperature float,
            PRIMARY KEY ( loc, time )
        )
        """ % TABLE_NAME )

    # session.execute( """CREATE INDEX IF NOT EXISTS latlong_index ON netcdf_data(loc);""" )


def drop_table( session ):

    session.execute("""
        DROP TABLE %s
        """ % TABLE_NAME )


def insert_data( session ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()
    
    cnt = 0
    cnt_i = 0
    start_time = time.time()

    for json_file in json_files_path_list:

        print 'JSON FILE: ', json_file

        with open( json_file ) as fp:  
            line = fp.readline().strip()
            while line:
                if line != '[' and line != ']':
                    if ( line.endswith(',') ):
                        line = line[:-1]
                    doc = json.loads( line )

                    session.execute(
                        """
                        INSERT INTO netcdf_data (loc, time, wind_speed, rain_rate, sea_surface_temperature)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        ( str(doc['loc'][0]) + str(doc['loc'][1]), doc['time'], doc['wind_speed'], 
                            doc['rain_rate'], doc['surface_temperature'] 
                        )
                    )

                    line = fp.readline().strip()
                    cnt = cnt + 1
                    if cnt == 100000:
                        cnt_i = cnt_i + 1
                        print( 'INSERTED DOCS: ', ( cnt * cnt_i ), 'TIME: ', ( time.time() - start_time ))
                        cnt = 0
                else:
                    line = fp.readline().strip()

    
def retrieve_data( session ):

    query = session.prepare( """SELECT * FROM netcdf_data""" )
    # rows = session.execute( query, (2017365,) )
    rows = session.execute( query, )
    for row in rows:
        print ( row[0], row[1], row[2], row[3] )

    """
    https://dzone.com/articles/apache-cassandra-and-allow-filtering
    """


        

