import os, sys, json, pprint
sys.path.insert(0, '../utils')
import path_functions
sys.path.insert(0, '../utils')
import data_type_selection


def operations( op, cur ):

    if op == 1:
        # Create simple table
        create_table( cur )
    elif op == 2:
        # Drop table
        drop_table( cur )
    elif op == 3:
        # Insert data
        insert_data( cur )
    # elif op == 4:
    #     # Retrieve data
    #     retrieve_data( session )


def create_table( cur ):
    
    cur.execute("""
        CREATE TABLE netcdf_data (
            loc VARCHAR(255),
            time INTEGER NOT NULL,
            wind_speed REAL NOT NULL,
            rain_rate REAL NOT NULL,
            sea_surface_temperature REAL NOT NULL,
            PRIMARY KEY (loc , time)
        );"""
    )


def drop_table( cur ):

    cur.execute('''
        DROP TABLE IF EXISTS netcdf_data;
        '''
    )


def insert_data( cur ):

    json_files_path_list, data_type = data_type_selection.data_type_selection()
    cnt = 1

    for json_file in json_files_path_list:

        with open( json_file ) as fp:  
            line = fp.readline().strip()
            while line:
                if line != '[' and line != ']':
                    if ( line.endswith(',') ):
                        line = line[:-1]
                    doc = json.loads( line )

                    postgres_insert_query = """ 
                    INSERT INTO netcdf_data (loc, time, wind_speed, rain_rate, sea_surface_temperature) 
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    record_to_insert = (str(doc['loc'][0]) + str(doc['loc'][1]), doc['time'], 
                    doc['wind_speed'], doc['rain_rate'], doc['surface_temperature'])
                    cur.execute( postgres_insert_query, record_to_insert )

                    line = fp.readline().strip()
                    cnt += 1
                    if cnt == 10000:
                        break
                else:
                    line = fp.readline().strip()

