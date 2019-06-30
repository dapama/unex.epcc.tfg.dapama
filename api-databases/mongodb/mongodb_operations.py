
from pymongo import MongoClient, GEOSPHERE, GEO2D
import os, sys, json, pprint, time
sys.path.insert(0, '../utils')
import path_functions, data_type_selection, query_parameters_selection


def operations( op, db ):
    if op == 1:
        # Print Collections
        create_collection( db )
    elif op == 2:
        # Drop Collections
        drop_collections( db )
    elif op == 3:
        # Insert Data
        insert_data( db )
    elif op == 4:
        # Spatial Querying using 2D Index
        spatial_querying( db )
    elif op == 5:
        # Temporal Querying using 2D Index
        temporal_querying( db )
    elif op == 6:
        # Temporal-Spatial Querying using 2D Index
        temporal_spatial_querying( db )


def create_collection( db ):
    
    if 'netcdf_Data' not in db.collection_names():
        collection = db[ 'netcdf_Data' ]
        collection.create_index([( "loc", GEO2D )])
        # collection.create_index([( "loc", SPHERE2D )])


def drop_collections( db ):
    for collection in db.collection_names():
        db.drop_collection( collection )


def insert_data( db ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()

    cnt, cnt_i = 0, 0
    start_time = time.time()

    collection = db[ 'netcdf_Data' ]

    with open( '_mongodb_.txt', 'a' ) as outfile:

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
                        
                        collection.insert( doc )

                        line = fp.readline().strip()
                        cnt += 1
                        if cnt == 100000:
                            cnt_i += 1

                            inserted_docs = str( cnt * cnt_i )
                            query_time = str( time.time() - start_time )

                            # print( """\tInserted Docs: """ + inserted_docs + """ // Time: """ + query_time + """\n""" )
                            outfile.write( """\tInserted Docs: """ + inserted_docs + """ // Time: """ + query_time + """\n""" )
                            cnt = 0
                    else:
                        line = fp.readline().strip()
    f.close()


def spatial_querying( db ):

    lat1, long1, lat2, long2 = query_parameters_selection.ask_for_a_query_box()
    
    start_time = time.time()

    collection = db[ 'netcdf_Data' ]

    with open( '_mongodb_.txt', 'a' ) as outfile:

        outfile.write( """\n ---------------- \nSPATIAL QUERY: [ [""" + lat1 + """, """ + long1 + """] [""" + lat2 + """, """ + long2 + """] ]""")

        retrieved_docs = str( collection.count_documents({"loc": {"$geoWithin": {"$box": [[float( lat1 ), float( long1 )], [float( lat2 ), float( long2 )]] }}}) )
        query_time = str( ( time.time() - start_time ) )

        # print( """\n\tRetrieved Docs: """ + retrieved_docs + """ // Time: """ + query_time + """\n""" )
        outfile.write(  """\n\tRetrieved Docs: """ + retrieved_docs + """ // Time: """ + query_time + """\n""" )

    outfile.close()


def temporal_querying( db ):

    dates = query_parameters_selection.ask_for_a_query_date()

    start_time = time.time()

    collection = db[ 'netcdf_Data' ]

    with open( '_mongodb_.txt', 'a' ) as outfile:

        outfile.write( """\n ---------------- \nTEMPORAL QUERY: [ """ + ', '.join( str(d) for d in dates ) + """ ]""")

        retrieved_docs = str( collection.count_documents( {"time": { "$in": dates }} ) )
        query_time = str( ( time.time() - start_time ) )

        # print( """\n\tRetrieved Docs: """ + retrieved_docs + """ // Time: """ + query_time + """\n""" )
        outfile.write(  """\n\tRetrieved Docs: """ + retrieved_docs + """ // Time: """ + query_time + """\n""" )

    outfile.close()


def temporal_spatial_querying( db ):

    lat1, long1, lat2, long2 = query_parameters_selection.ask_for_a_query_box()
    dates = query_parameters_selection.ask_for_a_query_date()

    start_time = time.time()
    
    collection = db[ 'netcdf_Data' ]
    with open( '_mongodb_.txt', 'a' ) as outfile:

        outfile.write( """\n ---------------- \nSPATIAL-TEMPORAL QUERY: [ [""" +
                       lat1 + """, """ + long1 + """] [""" + lat2 + """, """ + long2 + """] ]""" +
                       """ && [ """ + ', '.join( str(d) for d in dates ) + """ ]""")

        retrieved_docs = str( collection.count_documents( {
            "loc": {"$geoWithin": {"$box": [[float( lat1 ), float( long1 )], [float( lat2 ), float( long2 )]] }}, 
            "time": { "$in": dates }}
            ) )
        query_time = str( time.time() - start_time )

        # print( """\n\tRetrieved Docs: """ + retrieved_docs + """ // Time: """ + query_time + """\n""" )
        outfile.write(  """\n\tRetrieved Docs: """ + retrieved_docs + """ // Time: """ + query_time + """\n""" )

    outfile.close()
