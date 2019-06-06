import psycopg2


def database_configuration( ):

    conn_string = "host='localhost' dbname='postgres' user='postgres' password='secretpassword' port='5432'"

    connection = psycopg2.connect( conn_string )
    cursor = connection.cursor()
    return cursor, connection
