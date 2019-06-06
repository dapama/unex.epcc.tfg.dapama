
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.admin import Admin

"""
First to all, it's necessary to create an user-admin from your local browser into VagrantIP:CouchBasePORT 
                                                                                    (192.168.10.95:8091)
     and a new bucket in which to keep save the documents. Of course the input configuration in this python 
     file must be the same. When you configure the Cluster properties, you could disable analytics options 
     to save some memory.

     If you want to add a geospatial index, you need to create it inside the Couchbase console.
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
