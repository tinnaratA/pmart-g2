var db = require("../database/nedb");
var permissions = require("../utils/permissions");
var time_utils = require("../utils/time");

var user_namespace = "usersdb";
var product_namespace = "productsdb";
var order_namespace = "ordersdb";
var po_namespace = "purchasesdb";

var order_no = 1;

let order_s_list = (req, res) => {
    db[order_namespace].find(req.query, (err, data) => {
        if(err){
            console.log(err);
            return res.send({success: true, data: err})
        }
        if(!data){
            return res.status(204).send({success: true, data: "Sale Order Not Found."})
        }
        return res.send({success:true, data: data});
    });
}

let order_p_list = (req, res) => {
    db[po_namespace].find(req.query, (err, data) => {
        if(err){
            console.log(err);
            return res.send({success: true, data: err})
        }
        if(!data){
            return res.status(204).send({success: true, data: "Purchase Order Not Found."})
        }
        return res.send({success:true, data: data});
    });
}

let create_s_order = (req, res) => {
    try{
        var req_data = req.body;
        if(Object.keys(req_data).length > 0){
            // Set Id and Timestamp of Object
            var req_data = time_utils.setObjectTimeStamp(req_data);
            req_data['id'] = "ORD" + parseInt(Math.random(1,50) * 10000000000);
            // Get Product real object from database.
            db[product_namespace].find({}, (err, products) => {
                if(err){
                    console.error(err);
                    return res.send(500).send({success: false, data: "Unexpected Error(s)."});
                }
                var ordProductList = req_data.arrayitem.map(d => { return d.item; });
                var arrayitems = products.filter(p => {
                    return ordProductList.indexOf(p.Description) >= 0;
                });
                var finalItems = req_data.arrayitem.map((d, index) => {
                    d['vendor'] = arrayitems[index]['vendor'];
                    return d;
                });
                req_data.arrayitem = finalItems;
                db[order_namespace].insert(req_data, (err) => {
                    if(err)
                        console.error(err);
                });
            });
            return res.status(201).send({success: true, data: "Order has been created."});
        }
        else
            return res.status(400).send({success: true, data: "Invalid JSON."});
    } catch (error) {
        return res.status(500).send({success: false, data: "Unexpected Error(s)."})
    }
}

let create_p_order = (req, res) => {
    try {
        var orders = req.body;
        var allItems = [];
        orders.map(
            order => order.arrayitem.filter(d => d.vendor == req.params.vendor_id).map(
                item => {
                    allItems.push(item);
                }
            )
        );

        allItems.sort((a, b) => {
            if(a.item < b.item) return -1;
            if(a.item > b.item) return 1;
            return 0;
        });

        // var allItemNames = allItems.map(d => { return d.item; });
        // var groupped = allItemNames.map(grp => {
        //     return allItems.filter(item => grp == item.item);
        // });
        // var uniqueItems = groupped.map(ds => {
        //     var sumqty = ds.map(d => { return d.qty }).reduce((prev, current) => { return prev + current } );
        //     var sumprice = ds.map(d => { return d.price }).reduce((prev, current) => { return prev + current } );
        //     ds[0].price = sumprice;
        //     ds[0].qty = sumqty;
        //     return ds[0];
        // });
        // console.log(uniqueItems);

        var uniqueItems = [];
        if(allItems.length > 0){
            allItems.reduce((prev, current) => {
                if(uniqueItems.length <= 0 && prev.item !== current.item){
                    uniqueItems.push(prev);
                    return current;
                }
                else if(prev.item === current.item && uniqueItems.length > 0){
                    var sumprice = current.price + prev.price;
                    var sumqty = current.qty + prev.qty;
                    current.price = sumprice;
                    current.qty = sumqty;
                    return current;
                }
                else if(allItems.indexOf(current) === allItems.length - 1){
                    uniqueItems.push(prev);
                    uniqueItems.push(current);
                    return current;
                }
                else{
                    uniqueItems.push(prev);
                    return current;
                }
            });

            var data = {
                po: {
                    id: "PO" + parseInt(Math.random(1,50) * 10000000000),
                    items: uniqueItems,
                    status: "RAISED"
                },
                detail: orders
            }

            db[po_namespace].insert(data, (err) => {
                if(err){
                    console.log(err);
                    return res.status(500).send({success: false, data: err});
                }
            });
            return res.send({success: true, data: data});
        }
        return res.send({success: true, data: "No item to create purchase order(s)."})
    } catch (error) {
        console.error(error);
        return res.status(400).send({success: false, data: "Invalid JSON."});
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
    so: {
        orderList: order_s_list,
        getOrder: get_order,
        createOrder: create_s_order,
        editOrder: edit_order,
        editOrders: edit_orders
    },
    po: {
        purchaseList: order_p_list,
        createOrder: create_p_order,
    }
}