
from couchbase.cluster import Cluster
from couchbase.n1ql import N1QLQuery
import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
import data_type_selection
import time


def operations( op, cb ):
    if op == 1:
        # Print Document from an specific Bucket
        print_bucket_documents( cb )
    elif op == 2:
        # Insert data (JSON or GEOJSON) into any Bucket
        insert_data( cb )


def print_bucket_documents( cb ):
    print( cb.get( 'u:NetCDF_data' ).value )


def insert_data( cb ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()

    cnt = 0
    cnt_i = 0

    for json_file in json_files_path_list:

        start_time = time.time()

        with open( json_file ) as fp:  
            line = fp.readline().strip()
            while line:
                if line != '[' and line != ']':
                    if ( line.endswith(',') ):
                        line = line[:-1]
                    doc = json.loads( line )

                    index = str( doc['time'] ) + '_' + str( doc['loc'][0] ) + str( doc['loc'][1] )
                    cb.insert( index, doc )
                    # print (doc)

                    line = fp.readline().strip()
                    cnt = cnt + 1
                    if cnt == 10000:
                        cnt_i = cnt_i + 1
                        print( 'INSERTED DOCS: ', ( cnt * cnt_i ), 'TIME: ', ( time.time() - start_time ))
                        cnt = 0
                else:
                    line = fp.readline().strip()      

