
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
sys.path.insert(0, '../utils')
import data_type_selection
import time
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

    cnt = 0
    cnt_i = 0
    start_time = time.time()

    if not db.hasCollection( name  = 'netcdf_data' ):
        collection = db.createCollection( className = 'Collection', name = 'netcdf_data' )
        collection.ensureGeoIndex( [ 'loc' ] )
        print ('GEOSPATIAL INDEX')
    else:
        collection = db[ 'netcdf_data' ]

    f = open("arango_doc.txt", "w")

    for json_file in json_files_path_list:

        print 'JSON FILE: ', json_file

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
                    cnt = cnt + 1
                    if cnt == 100000:
                        cnt_i = cnt_i + 1
                        # f.write( "%i ' - ' %f\r\n" % ( cnt * cnt_i, time.time() - start_time ))
                        print( "%i ' - ' %f\r\n" % ( cnt * cnt_i, time.time() - start_time ))
                        cnt = 0
                else:
                    line = fp.readline().strip()
    f.close()


def spatial_querying( db ):

    collection = db[ 'netcdf_data' ]
    
    for docs in collection.fetchAll():
        print ( docs )

    # start_time = time.time()

    # for current_collection in retrieve_collections( db ):
    #     collection = db.collection( current_collection['name'] )
        
    #     print( 'RETRIEVED DOCS: ', len(
    #         collection.find_in_box( -77.49, -89.30, 0.00, 0.00, 0, 0, collection.indexes( )[1]['id'] )
    #     ), 'TIME: ', ( time.time() - start_time ))
        

def temporal_querying( db ):
    
    start_time = time.time()

    for current_collection in retrieve_collections( db ):
        collection = db.collection( current_collection['name'] )

        print( 'RETRIEVED DOCS: ', len(
            collection.find({ 'time': 2017365 })
        ), 'TIME: ', ( time.time() - start_time ))

        
def temporal_spatial_querying( db ):

    start_time = time.time()

    for current_collection in retrieve_collections( db ):
        collection = db.collection( current_collection['name'] )

        print( 'RETRIEVED DOCS: ', len(
            collection.find_in_box( -77.49, -89.30, 0.00, 0.00, 0, 0, collection.indexes( )[1]['id'] )
            # .find({ 'time': 2017365 })
        ), 'TIME: ', ( time.time() - start_time ))
