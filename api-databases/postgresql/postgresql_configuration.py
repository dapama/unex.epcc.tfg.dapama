import psycopg2


def database_configuration( ):

    try:
        conn = psycopg2.connect( "dbname='postgres' user='postgres' password='password' host='localhost' port='5432'" )
        return conn.cursor()
    except:
        print ( "I am unable to connect to the database" )
        return
