
from cassandra.cluster import Cluster

KEYSPACE = "tfg"


def database_configuration( ):

    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect( )

    session.execute( """
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE )

    session.set_keyspace( KEYSPACE )

    return session