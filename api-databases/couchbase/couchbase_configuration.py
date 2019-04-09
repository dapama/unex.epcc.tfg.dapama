
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator

"""
First to all, it's necessary to create an user-admin from your local browser with VagrantIP:CouchBasePORT 
                                                                                    (192.168.10.95:8091)
     and a new bucket in which to save. Of course the input data must be the same in this python file.
     
     When you configure the Cluster properties, you could disable analytics options to save some memory.
"""

couchbase_endpoint          = 'couchbase://localhost:8091'
username                    = 'admin'
password                    = 'password'
bucket_name                 = 'TFG_NetCDF'


def database_configuration( ):

    cluster = Cluster( couchbase_endpoint )
    cluster.authenticate( PasswordAuthenticator( username, password ) )
    cb = cluster.open_bucket( bucket_name )
    return cb
