let initializer = require("./initializer");

initializer.cleardb();
initializer.db("./database/static/users.json", "usersdb");
initializer.db("./database/static/orderitem.json", "productsdb");