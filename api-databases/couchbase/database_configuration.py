
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator

cluster = Cluster('couchbase://localhost:8091')
authenticator = PasswordAuthenticator('admin', 'Bgt56yhn$')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('netcdf')
