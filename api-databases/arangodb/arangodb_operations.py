
import os, sys, json, pprint, time
sys.path.insert(0, '../utils')
import data_type_selection, path_functions, query_parameters_selection
from arangodb_configuration import database_configuration


def operations( op, db ):

    if op == 1:
        # Retrieve all Collection
        print_all_collections( db )
    elif op == 2:
        # Drop All Collections
        drop_collections( db )
    elif op == 3:
        # Insert data (JSON or GEOJSON) into Collections
        insert_data( db )
    elif op == 4:
        # Spatial Querying using GEO Index
        spatial_querying( db )
    elif op == 5:
        # Temporal Querying using GEO Index
        temporal_querying( db )
    elif op == 6:
        # Temporal-Spatial Querying using GEO Index
        temporal_spatial_querying( db )


def retrieve_collections( db ):
    return list( filter ( lambda collection: collection['name'][0] != "_", db.collections() ) )


def print_all_collections( db ):
    print 'Collection List: \n'
    for collection in retrieve_collections( db ):
        print collection['name']


def drop_collections( db ):
    db.dropAllCollections()


def insert_data( db ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()

    cnt, cnt_i = 0, 0
    start_time = time.time()

    if not db.has_collection( name  = 'netcdf_data' ):
        collection = db.create_collection( className = 'Collection', name = 'netcdf_data' )
        index = collection.add_geo_index(fields=['loc'])
    else:
        collection = db.collection( 'netcdf_data' )

    with open( '_arangodb_.txt', 'a' ) as outfile:

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
                        
                        arango_doc = collection.createDocument()
                        arango_doc['loc'] = doc['loc']
                        arango_doc['time'] = doc['time']
                        arango_doc['wind_speed'] = doc['wind_speed']
                        arango_doc['rain_rate'] = doc['rain_rate']
                        arango_doc['surface_temperature'] = doc['surface_temperature']
                        arango_doc.save()

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

    collection = db[ 'netcdf_data' ]

    with open( '_arangodb_.txt', 'a' ) as outfile:

        outfile.write( """\n ---------------- \nSPATIAL QUERY: [ [""" + lat1 + """, """ + long1 + """] [""" + lat2 + """, """ + long2 + """] ]""")

        cursor_docs = collection.find_in_box( float( lat1 ), float( long1 ), float( lat2 ), float( long2 ), 0, 0, collection.indexes( )[1]['id'] )
        query_time = str( ( time.time() - start_time ) )

        # print( """\n\tRetrieved Docs: """ + retrieved_docs + """ // Time: """ + query_time + """\n""" )
        outfile.write(  """\n\tRetrieved Docs: """ + str( cursor_docs.count() ) + """ // Time: """ + query_time + """\n""" )

    outfile.close()
        

def temporal_querying( db ):

    start_time = time.time()

    collection = db[ 'netcdf_data' ]

    with open( '_arangodb_.txt', 'a' ) as outfile:

        outfile.write( """\n ---------------- \nTEMPORAL QUERY: """)

        """ To custom this query you must to introduce the range by writting it on the line below """
        cursor_docs = collection.find_in_range( "time", 2017365, 2018006 )
        query_time = str( ( time.time() - start_time ) )

        # print( """\n\tRetrieved Docs: """ + str( cursor_docs.count() ) + """ // Time: """ + query_time + """\n""" )
        outfile.write(  """\n\tRetrieved Docs: """ + str( cursor_docs.count() ) + """ // Time: """ + query_time + """\n""" )

    outfile.close()

        
def temporal_spatial_querying( db ):

    start_time = time.time()

    """ This query cannot be created because Arango doesn't allow query concatenations """

    # for current_collection in retrieve_collections( db ):
    #     collection = db.collection( current_collection['name'] )
    #     collection.find_in_box( -5.49, -10.40, 0.00, 0.00, 0, 0, collection.indexes( )[1]['id'] )
        
    print( 'TIME: ', ( time.time() - start_time ))
