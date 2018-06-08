var db = require("../database/nedb");

let inv_namespace = "invoicesdb";
let po_namespace = "purchasesdb";

let inv_list = (req, res) => {
    var status = 200;
    var data = [];
    var success = false;

    db[inv_namespace].find(req.query, (err, data) => {
        if(err){
            console.error(err);
            data = err;
            status = 500;
            success = false;
            return res.status(status).send({success: success, data: data});
        }
        else
        {
            if(data.length > 0){
                status = 200;
                success = true;
                data = data;
                return res.status(status).send({success: success, data: data});
            }
            else
            {
                status = 204;
                data = "Invoices Not Found.";
                success = true;
                return res.status(status).send({success: success, data: data});
            }
        }
    });
}

let create_inv = (req, res) => {
    var errors = [];
    var purchaseOrders = req.body;
    purchaseOrders.map(porder => {
        var dataToSave = {};
        dataToSave._id = porder._id;
        dataToSave.id = "INV" + parseInt(Math.random(1,50) * 10000000000);
        dataToSave.items = porder.items;
        dataToSave.total = porder.total;
        dataToSave.status = "RAISED";
        dataToSave.date = new Date().getTime();
        dataToSave.purchaseOrder = porder.id;
        dataToSave.delivery = porder.delivery;
        dataToSave.vendor = porder.vendor;

        db[inv_namespace].insert(dataToSave, (err) => {
            if(err){
                console.error(err);
                errors.push(err);
            }
        });

        db[po_namespace].update({_id: porder._id}, {$set: {processed: true}}, (err) => {
            if(err){
                console.error(err);
                errors.push(err);
            }
        });
    });
    if(errors.length > 0){
        return res.status(500).send({success: false, data: errors});
    }
    return res.status(200).send({success: true, data: "Invoice(s) has been created."});
};

let get_invoice = (req, res) => {
    db[inv_namespace].findOne({_id: req.params.inv_id}, (err, data) => {
        if(err){
            console.error(err);
            return res.status(500).send({success: false, data: err});
        }
        else
        {
            if(data){
                return res.status(200).send({success: true, data: data});
            }
            else
            {
                return res.status(204).send({success: true, data: "Invoice Not Found."});
            }
        }
    });
};

let edit_invoice = (req, res) => {
    db[inv_namespace].findOne({_id: req.params.inv_id}, (err, data) => {
        if(err){
            console.error(err);
            return res.status(500).send({success: false, data: err});
        }
        else
        {
            if(data){
                db[inv_namespace].update({_id: data._id}, { $set: req.body }, { multi: true}, (err) => {
                    if(err){
                        console.error(err);
                        return res.status(500).send({success: false, data: err});
                    }
                    else{
                        return res.status(200).send({success: true, data: "Invoice has been updated."})
                    }
                });
            }
            else
            {
                return res.status(204).send({success: true, data: "Invoice Not Found."});
            }
        }
    });
}

module.exports = {
    getInvoice: get_invoice,
    invoiceList: inv_list,
    createInvoice: create_inv,
    editInvoice: edit_invoice
};