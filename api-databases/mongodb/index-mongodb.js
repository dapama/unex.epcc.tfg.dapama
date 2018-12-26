const MongoClient = require('mongodb').MongoClient;

const url = 'mongodb://localhost:27017';
const dbName = 'test';

// MongoClient.connect ( url, function( err, client ) {

//     // Use the admin database for the operation
//     const adminDb = client.db( dbName ).admin();
    
//     // List all the available databases
//     adminDb.listDatabases( function( err, dbs ) {
//       test.equal( null, err );
//       test.ok( dbs.databases.length > 0 );
//       client.close();
//     });
//   });

MongoClient.connect( url, function( err, client ) {
   
    const db = client.db( dbName );
    client.close();
});