var db = require("../database/nedb");
var permissions = require("../utils/permissions");
var time_utils = require("../utils/time");

var user_namespace = "usersdb";
var product_namespace = "productsdb";
var order_namespace = "ordersdb";

var order_no = 1;

let order_list = (req, res) => {
    db[order_namespace].find({}, (err, data) => {
        return res.send({success:true, data: data});
    });
}

let create_order = (req, res) => {
    try{
        var req_data = req.body;
        if(Object.keys(req_data).length > 0){
            var req_data = time_utils.setObjectTimeStamp(req_data);
            req_data['id'] = "ORD" + parseInt(Math.random(1,50) * 10000000000);
            db[order_namespace].insert(req_data, (err) => {
                if(err)
                    console.error(err);
            });
            return res.status(201).send({success: true, data: "Order has been created."});
        }
        else
            return res.status(400).send({success: true, data: "Invalid JSON."});
    } catch (error) {
        return res.status(500).send({success: false, data: "Unexpected Error(s)."})
    }
}

let get_order = (req, res) => {
    db[order_namespace].findOne({_id: req.params.order_id}, (err, data) => {
        if(err)
            console.log(err);
        else{
            if(data){
                return res.send({success: true, data: data})
            }else{
                return res.status(204).send({success: true, data: "Order Not Found."})
            }
        }
    });
}

let edit_order = (req, res) => {
    var req_data = req.body;
    db[order_namespace].findOne({_id: req.params.order_id}, (err, data) => {
        if(err){
            console.error(err);
            return res.status(500).send({success: false, data: "Unexpected Error(s)."});
        }

        if(!data){
            return res.status(204).send({success: true, data: "Order Not Found"});
        }

        db[order_namespace].update({_id: data._id}, {$set: req_data}, (err) => {
            if(err){
                console.error(err);
                return res.status(400).send({success: true, data: "Invalid JSON."});
            }
            return res.send({success: true, data: "Order has been updated."})            
        });

    });
}

let edit_orders = (req, res) => {
    var req_data = req.body;
    req_data.map(
        (d, index) => {
            db[order_namespace].findOne(
                {_id: d._id}, 
                (err, olddata) => {
                    if(err){
                        console.error(err);
                        return res.status(500).send({success: false, data: "Unexpected Error(s)."});
                    }

                    if(!olddata){
                        return res.status(204).send({success: true, data: "Order Not Found"});
                    }
                    var newdata = olddata;
                    newdata.status = d.status;
                    db[order_namespace].update({_id: olddata._id}, {$set: newdata}, (err, data) => {
                        if(err){
                            console.error(err);
                            return res.status(400).send({success: true, data: "Invalid JSON."});
                        }            
                    });
                }
            );
        }
    );
    return res.send({success: true, data: "Order has been updated."})
}

module.exports = {
    orderList: order_list,
    getOrder: get_order,
    createOrder: create_order,
    editOrder: edit_order,
    editOrders: edit_orders
}