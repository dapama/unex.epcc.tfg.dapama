import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
sys.path.insert(0, '../utils')
import data_type_selection
import time


def operations( op, cur, conn ):

    if op == 1:
        # Create simple table
        create_table( cur, conn )
    elif op == 2:
        # Drop table
        drop_table( cur, conn )
    elif op == 3:
        # Insert data
        insert_data( cur, conn )
    elif op == 4:
        # Retrieve data
        retrieve_data_spatial_query( cur )
    elif op == 5:
        # Retrieve data
        retrieve_data_temporal_query( cur )
    elif op == 6:
        # Retrieve data
        retrieve_data_spatial_temporal_query( cur )


def create_table( cur, conn ):
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS netcdf_data (
            doc_id BIGSERIAL PRIMARY KEY,
            loc GEOMETRY(Point,312),
            time INTEGER NOT NULL,
            wind_speed REAL NOT NULL,
            rain_rate REAL NOT NULL,
            sea_surface_temperature REAL NOT NULL
        );"""
    )

    conn.commit()

def drop_table( cur, conn ):

    cur.execute('''
        DROP TABLE IF EXISTS netcdf_data;
        '''
    )

    conn.commit()


def insert_data( cur, conn ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()
    
    start_time = time.time()
    cnt = 0
    cnt_i = 0

    for json_file in json_files_path_list:
        
        print 'JSON FILE: ', json_file

        with open( json_file ) as fp:  
            line = fp.readline().strip()
            while line:
                if line != '[' and line != ']':
                    if ( line.endswith(',') ):
                        line = line[:-1]
                    doc = json.loads( line )

                    postgres_insert_query = """ 
                    INSERT INTO netcdf_data (loc, time, wind_speed, rain_rate, sea_surface_temperature) 
                    VALUES (ST_GeomFromText(%s,312), %s, %s, %s, %s)
                    """

                    record_to_insert = 'POINT( {0} {1} )'.format( str(doc['loc'][1]), str(doc['loc'][0]) ), str(doc['time']), str(doc['wind_speed']), str(doc['rain_rate']), str(doc['surface_temperature'])

                    cur.execute( postgres_insert_query, record_to_insert )

                    line = fp.readline().strip()
                    cnt = cnt + 1
                    if cnt == 100000:
                        cnt_i = cnt_i + 1
                        print( 'INSERTED DOCS: ', ( cnt * cnt_i ), 'TIME: ', ( time.time() - start_time ))
                        cnt = 0
                        conn.commit()
                else:
                    line = fp.readline().strip()


def retrieve_data_spatial_query( cur ):

    start_time = time.time()

    cur.execute("""
        SELECT ST_Y(loc) AS latitude, ST_X(loc) as longitude FROM netcdf_data 
        WHERE loc && ST_MakeEnvelope( -5.49, -10.30, 0.00, 0.00, 4326 );
        """
    ) 

    print( 'RETRIEVED DOCS: ', len(cur.fetchall()), 'TIME: ', ( time.time() - start_time ))
    
    # docs_retrieved = cur.fetchall() 
    # print docs_retrieved


def retrieve_data_temporal_query( cur ):

    start_time = time.time()

    cur.execute("""
        SELECT ST_Y(loc) AS latitude, ST_X(loc) as longitude FROM netcdf_data 
        WHERE time = 2017365;
        """
    ) 

    print( 'RETRIEVED DOCS: ', len(cur.fetchall()), 'TIME: ', ( time.time() - start_time ))
    
    # docs_retrieved = cur.fetchall() 
    # print docs_retrieved


def retrieve_data_spatial_temporal_query( cur ):

    start_time = time.time()

    cur.execute("""
        SELECT ST_Y(loc) AS latitude, ST_X(loc) as longitude FROM netcdf_data 
        WHERE loc && ST_MakeEnvelope( -5.49, -10.30, 0.00, 0.00, 4326 ) AND time = 2017365;
        """
    ) 

    print( 'RETRIEVED DOCS: ', len(cur.fetchall()), 'TIME: ', ( time.time() - start_time ))
    
    # docs_retrieved = cur.fetchall() 
    # print docs_retrieved