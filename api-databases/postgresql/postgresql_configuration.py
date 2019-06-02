import psycopg2

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='password' host='localhost' port='5432'")
except:
    print "I am unable to connect to the database"

