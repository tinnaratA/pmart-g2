var express = require("express");
var multer  = require('multer')
var bodyParser = require("body-parser");
var app = express();
var db = require("./database/nedb");

var bodyParser = require('body-parser');
var rawBodySaver = function (req, res, buf, encoding) {
  if (buf && buf.length) {
    req.rawBody = buf.toString(encoding || 'utf8');
  }
}

app.use(bodyParser.json({ verify: rawBodySaver , limit: '50mb'}));
app.use(bodyParser.urlencoded({ verify: rawBodySaver, extended: true , limit: '50mb'}));
app.use(bodyParser.raw({ verify: rawBodySaver, type: function () { return true }, limit: '50mb' }));
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.use(express.static('./static'))



// ===============================================================================
// Old and Original Code 
// ===============================================================================
  
order_no = 1
order = []

users = [
    {"password": "password", "email": "Punika@horozont.in.th", "name":"Punika Puengnoo", "nickname": "คุณแขก", "type": "FINANCE" },
    {"password": "password", "email": "Patteera@horizont.in.th","name":"Patteera intra","nickname": "คุณเหมี่ยว", "type":"CUSTOMER"},
    {"password": "password", "email": "Supaporn@horizont.in.th","name":"Supaporn Klinhom","nickname":"คุณหนึ่ง", "type":"VENDER"},

    {"password": "", "email": "customer", "name":"ร้านบะหมี่ต้มยำ", "nickname": "ร้านบะหมี่ต้มยำ", "type": "CUSTOMER" },
    {"password": "", "email": "vendor", "name":"Vendor001", "nickname": "", "type": "VENDOR" },
    {"password": "", "email": "finance", "name":"Finance", "nickname": "", "type": "FINANCE" }
]

app.post('/reg', function (req, res) {
    if(users.filter(u => u.email == req.body.email ).length > 0){
        res.send("ERR01")
    }
    else{
        users.push(req.body)
        res.send("OK");
    }
});

app.get('/allusers', function (req, res) {
    res.send(users)
});

app.get('/orders', function (req, res) {
    res.send(order);
});

Number.prototype.pad = function(size) {
    var s = String(this);
    while (s.length < (size || 2)) {s = "0" + s;}
    return s;
}
  
app.post('/orders', function (req, res) {
    req.body.id = "ORD"+order_no.pad(10);
    order_no++;
    order.push(req.body);
    res.send("OK");
});

app.post('/order_all', function (req, res) {
    order = req.body;
    res.send("OK");
});

app.get('/refresh', function (req, res) {
    order_no = 1;
    order = [];

    res.send("OK");
});



// ===============================================================================
// New and shiny backend
// ===============================================================================

// Users APIs
user_apis = require("./apis/users");
app.post('/users/register', user_apis.register);
app.post('/users/login', user_apis.login);
app.post('/users/logout', user_apis.logout);

// Products APIs
product_apis = require("./apis/products");
app.get('/products/list', product_apis.productList);
app.get('/products/:product_id', product_apis.getProduct);
app.post('/products/create', product_apis.createProduct);
app.get('/products/image/:product_id', product_apis.productImage);
app.post('/products/image/:product_id', product_apis.productImage);

// Orders APIs
order_apis = require("./apis/orders");
app.get('/orders/list', order_apis.orderList);
app.post('/orders/create', order_apis.createOrder);
app.get('/orders/:order_id', order_apis.getOrder);
app.put('/orders/edit', order_apis.editOrders);
app.put('/orders/edit/:order_id', order_apis.editOrder);

// Customers APIs
customer_apis = require("./apis/customers");
app.get('/customers/list', customer_apis.customerList);

app.listen(2001, () => console.log('Application listening on port 2001!'));