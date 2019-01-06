const MongoClient = require('mongodb').MongoClient;
const test = require('assert');

const url = require('./config/database').url;
const dbName = 'test';

MongoClient.connect ( url, function( err, client ) {

    const db = client.db( dbName );

    // Use the admin database for the operation
    const adminDb = db.admin();
    
    // List all the available databases
    adminDb.listDatabases( function( err, dbs ) {
      test.equal( null, err );
      test.ok( dbs.databases.length > 0 );
      client.close();
    });
  });

// MongoClient.connect( url, function( err, client ) {
   
//     const db = client.db( dbName );
//     client.close();
// });