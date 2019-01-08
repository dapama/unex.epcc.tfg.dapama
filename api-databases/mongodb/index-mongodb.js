const MongoClient = require('mongodb').MongoClient
const config = require('./config/database');


( async function() {

  const client = await MongoClient.connect( config.url, { useNewUrlParser: true } );
  const db = client.db('unex_epcc_tfg');
  const collection = db.collection('l2b12');

  console.log('connected');

  // collection.deleteMany({})
  // .then(function() {
  //     const promises = products.map((product) => {
  //         console.log(product.name);
  //         ticketTotal += product.cost();
  //         return collection.insertOne(product);
  //     });

  //     return Promise.all(promises);
  // }).then(function(results) {
  //     for (let result of results) {
  //         console.log(result.result);
  //     }
  //     console.log("Ticket Total: " + ticketTotal);
  //     client.close();
  // });

})();