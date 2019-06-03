import os
from path_functions import get_files_data
from extract_netcdf_data import extract_data
from group_files import group_json_files_by_days

def transform_data( op, src_path, dst_path ):
    files_list = []
    get_files_data( src_path, files_list, ".gz" )

    if len( files_list ) > 0:        
        if op == 1:
            # Calling WindSAT Method - L3
            extract_data( files_list, 'L3', False )
            group_json_files_by_days( files_list, dst_path )
        
        elif op == 2:
            # Calling RapidSCAT / QuikSCAT Method - L2B12
            extract_data( files_list, 'L2B12', False )
            group_json_files_by_days( files_list, dst_path )
        
        elif op == 3:
            # Calling ASCAT Method - L2
            extract_data( files_list, 'L2', False )
            group_json_files_by_days(files_list, dst_path)
                
        elif op == 4:
            # Calling WindSAT Method - L3 GEOJSON
            extract_data( files_list, 'L3', True )
            group_json_files_by_days( files_list, dst_path )
                
        elif op == 5:
            # Calling RapidSCAT / QuikSCAT Method - L2B12 GEOJSON
            extract_data( files_list, 'L2B12', True )
            group_json_files_by_days( files_list, dst_path )
        
        elif op == 6:
            # Calling ASCAT Method - L2 GEOJSON
            extract_data( files_list, 'L2', True )
            group_json_files_by_days( files_list, dst_path )

    else:
        print( "There is not files in the path: " + src_path )


def get_data_path( op ):
    
    print( "Can you select the path where the data is saved? (SRC)\n" )
    src_path = '/srv/ftp-data/netcdf-files/windsat-l3'
    
    print( "Can you select the path where the data will be saved? (DST)\n" )
    dst_path = '/srv/ftp-data/json-files/windsat-l3'
    
    if os.path.isdir( src_path ) and os.path.isdir( dst_path ):
        transform_data( op, src_path, dst_path )
    else:
        print( "The Path doesn't exist." )


def init():
    print( "Welcome to the NetCDF to JSON program!\n" )
    print( "What type satellite data do you want to convert?\n" )
    print( "\t0. Exit\n"
          "\t1. L3 from WindSAT - JSON FILES\n"
          "\t2. L2B12 from RapidSCAT / QuikSCAT - JSON FILES\n"
          "\t3. L2 from ASCAT - JSON FILES\n"
          "\t4. L3 from WindSAT - GEOJSON FILES\n"
          "\t5. L2B12 from RapidSCAT / QuikSCAT - GEOJSON FILES\n"
          "\t6. L2 from ASCAT - GEOJSON FILES\n" )

    op = 1
    get_data_path( op )


init()
