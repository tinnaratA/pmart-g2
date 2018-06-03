var db = require("../database/nedb");

let inv_namespace = "invoicesdb";

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
    return res.send(req.body);
}

module.exports = {
    invoiceList: inv_list
};