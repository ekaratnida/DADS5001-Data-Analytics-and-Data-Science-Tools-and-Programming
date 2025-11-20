Example of mongodb shell
1. mongosh
2. https://www.geeksforgeeks.org/mongodb/mongodb-shell/

Run the commands below inside mongosh for creating db and table.

use mydb

db.mycollection.insertMany([{"name" : "Mary", "pet": "dog"}, {"name" : "John", "pet": "cat"}, {"name" : "Robert", "pet": "bird"}])
