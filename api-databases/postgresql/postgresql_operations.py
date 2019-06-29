import os, sys, json, pprint, time
sys.path.insert(0, '../utils')
import path_functions, data_type_selection, query_parameters_selection


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
    cnt, cnt_i = 0, 0

    with open( '_postgresql_.txt', 'a' ) as outfile:

        outfile.write( """\n ---------------- \nINSERTION PROCESS: \n""")

        for json_file in json_files_path_list:
            
            # print 'JSON FILE: ', json_file
            outfile.write( """\t-> Json file: """ + json_file + """\n""" )

            with open( json_file ) as fp:  
                line = fp.readline().strip()
                while line:
                    if line != '[' and line != ']':
                        if ( line.endswith(',') ):
                            line = line[:-1]
                        doc = json.loads( line )

                        # postgres_insert_query = """ 
                        # INSERT INTO netcdf_data ( loc, time, wind_speed, rain_rate, sea_surface_temperature ) 
                        # VALUES ( ST_GeomFromText( %s,312 ), %s, %s, %s, %s )
                        # """

                        # record_to_insert = 'POINT( {0} {1} )'.format( str(doc['loc'][1]), str(doc['loc'][0]) ), 
                        # str(doc['time']), str(doc['wind_speed']), str(doc['rain_rate']), str(doc['surface_temperature'])

                        # cur.execute( postgres_insert_query, record_to_insert )

                        line = fp.readline().strip()
                        cnt += 1
                        
                        if cnt == 100000:
                            cnt_i += 1
                            # print( 'INSERTED DOCS: ', ( cnt * cnt_i ), 'TIME: ', ( time.time() - start_time ))
                            outfile.write( """\tInserted Docs: """ + str(( cnt * cnt_i )) + 
                                           """ time: """ + str(( time.time() - start_time )) + """\n""" )
                            cnt = 0
                            conn.commit()
                    else:
                        line = fp.readline().strip()
    f.close()


def retrieve_data_spatial_query( cur ):

    lat1, long1, lat2, long2 = query_parameters_selection.ask_for_a_query_box()
    
    start_time = time.time()

    with open( '_postgresql_.txt', 'a' ) as outfile:

        outfile.write( """\n ---------------- \nSPATIAL QUERY: [ [""" + lat1 + """, """ + long1 + """] [""" + lat2 + """, """ + long2 + """] ]""")

        cur.execute("""
            SELECT ST_Y( loc ) AS latitude, ST_X( loc ) as longitude FROM netcdf_data 
            WHERE loc && ST_MakeEnvelope( %s, %s, %s, %s, 4326 );
            """, ( lat1, long1, lat2, long2, )
        )

        retrieved_docs = str( len( cur.fetchall() ) )
        query_time = str( ( time.time() - start_time ) )

        # print( """\n\tRetrieved Docs: """ + retrieved_docs + """ // TIME: """ + time + """\n""" )
        outfile.write(  """\n\tRetrieved Docs: """ + retrieved_docs + """ // TIME: """ + query_time + """\n""" )

    outfile.close()


def retrieve_data_temporal_query( cur ):
    
    dates = query_parameters_selection.ask_for_a_query_date()

    start_time = time.time()

    with open( '_postgresql_.txt', 'a' ) as outfile:

        outfile.write( """\n ---------------- \nTEMPORAL QUERY: [ """ + ', '.join( str(d) for d in dates ) + """ ]""")

        cur.execute("""
            SELECT ST_Y( loc ) AS latitude, ST_X( loc ) as longitude FROM netcdf_data 
            WHERE ( time = ANY( %s ) );
            """, ( dates, )
        ) 

        retrieved_docs = str( len( cur.fetchall() ) )
        query_time = str( ( time.time() - start_time ) )

        # print( """\n\tRetrieved Docs: """ + retrieved_docs + """ // TIME: """ + time + """\n""" )
        outfile.write(  """\n\tRetrieved Docs: """ + retrieved_docs + """ // TIME: """ + query_time + """\n""" )
    
    outfile.close()


def retrieve_data_spatial_temporal_query( cur ):

    lat1, long1, lat2, long2 = query_parameters_selection.ask_for_a_query_box()
    dates = query_parameters_selection.ask_for_a_query_date()

    start_time = time.time()

    with open( '_postgresql_.txt', 'a' ) as outfile:

        outfile.write( """\n ---------------- \nSPATIAL-TEMPORAL QUERY: [ [""" +
                       lat1 + """, """ + long1 + """] [""" + lat2 + """, """ + long2 + """] ]""" +
                       """ && [ """ + ', '.join( str(d) for d in dates ) + """ ]""")

        cur.execute("""
            SELECT ST_Y( loc ) AS latitude, ST_X( loc ) as longitude FROM netcdf_data 
            WHERE loc && ST_MakeEnvelope( %s, %s, %s, %s, 4326 ) AND ( time = ANY( %s ) );
            """, ( lat1, long1, lat2, long2, dates, )
        ) 

        retrieved_docs = str( len( cur.fetchall() ) )
        query_time = str( ( time.time() - start_time ) )

        # print( """\n\tRetrieved Docs: """ + retrieved_docs + """ // TIME: """ + time + """\n""" )
        outfile.write(  """\n\tRetrieved Docs: """ + retrieved_docs + """ // TIME: """ + query_time + """\n""" )

    outfile.close()
