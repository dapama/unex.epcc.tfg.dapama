import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
sys.path.insert(0, '../utils')
import data_type_selection


def operations( op, cur ):

    if op == 1:
        # Retrieve all Data
        create_table( cur )
    elif op == 3:
        # Insert Data
        insert_data( cur )


def create_table( cur ):
    cur.execute('''CREATE TABLE IF NOT EXISTS NETCDFDATA  
    (DOCUMENT_ID     SERIAL    PRIMARY KEY);''')


def insert_data( cur ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()

    for json_file in json_files_path_list:

        json_docs = json.load( open( json_file ) )
        for doc in json_docs[ 'data' ]:
            print ( doc )

