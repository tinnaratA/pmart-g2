var md5 = require('md5');
var time_utils = require("../utils/time");
var db = require("../database/nedb");
var token_utils = require("../utils/token");
var settings = require("../initializer").getSettings("./config.json");

var user_namespace = "usersdb";
var token_namespace = "tokensdb";

let login_handler = (req, res) => {
    var req_data = req.body;
    db[user_namespace].findOne(req_data, (err, data) => {
        if(err){
            console.error(err);
            return res.status(401).send({success: false, data: "Unauthorized"});
        }
        else{
            if(data){
                if(data.is_login){
                    return res.status(401).send({success: false, data: "duplicate login."});
                }

                data.last_login = time_utils.toLocalTime(new Date());
                // data.is_login = true;
                data.is_login = false;
                db[user_namespace].update({_id: data._id}, { $set: data}, (err, updated_data) => {
                    if(err){
                        console.error(err);
                        return res.status(401).send({success: false, data: "Unauthorized"});
                    }
                    else
                        token = token_utils.saveToken(data._id)
                        data['authentication'] = token
                        return res.status(200).send({success: true, data: data});
                });
            }
            else
                return res.status(401).send({success: false, data: "User Not Found."});
        }
    });
};

let register_handler = (req, res) => {
    try {
        var req_data = req.body;
        req_data["type"] = req.body.type || "CUSTOMER"
        req_data.password = md5(req_data.password);
        req_data["active"] = true,
        req_data["last_login"] = null,
        req_data["is_login"] = false
        req_data = time_utils.setObjectTimeStamp(req_data)
    } catch (error) {
        console.error(error);
        return res.status(500).send({success: false, data: "Unexpected Error(s)."});
        
    }

    db[user_namespace].insert(req_data, (err) => {
        if(err){
            console.error(err);
            return res.status(400).send({success: false, data: 'Invalid Parameter(s).'});
        }
        return res.send({"success": true, "data": "User has been created."});
    });
};

let logout_handler = (req, res) => {
    try {
        var req_data = req.body;
    } catch (error) {
        console.error(error);
        return res.status(500).send({success: false, data: "Unexpected Error(s)."});
    }

    db[user_namespace].findOne(req_data, (err, data) => {
        if(err){
            console.error(err);
            return res.status(401).send({success: false, data: "Unauthorized"});
        }else{
            if(data){
                data.is_login = false;
                db[user_namespace].update({_id: data._id}, { $set: data}, (err) => {
                    if(err){
                        console.error(err);
                        return res.status(401).send({success: false, data: "Unauthorized"});
                    }
                    else
                        token_utils.removeToken(data._id);
                        return res.status(200).send({success: true, data: "User has been logout."});
                });
            }else{
                return res.status(401).send({success: false, data: "User Not Found."});
            }
        }
    });
}

module.exports = {
    login: login_handler,
    register: register_handler,
    logout: logout_handler
}
