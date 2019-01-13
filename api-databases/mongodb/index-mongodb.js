const MongoClient = require('mongodb').MongoClient
const config = require('./config/database');

var jsonData = require('../../ftp-data/json-files/quikscat-l2b12/001.json');

var data = JSON.stringify(jsonData);
console.log(data)

( async function() {
  const client = await MongoClient.connect( config.url, { useNewUrlParser: true } );
  const db = client.db('unex_epcc_tfg');
  console.log('Connected to MongoDB');
  const collection = db.collection('l2b12_data');
  
  collection.insertMany(data);

})();