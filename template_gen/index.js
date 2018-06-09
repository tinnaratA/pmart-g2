var db = require("../database/nedb");

let inv_namespace = "invoicesdb";
let po_namespace = "purchasesdb";

findinv = (inv_id) => new Promise(
    (resolve, _) => {
        db[inv_namespace].findOne({_id: inv_id}, (err , data) => resolve(data));
    }
)


addToTable = data => {
    return '<tr>'+
    Object.values(data).map(col => '<td>'+col+'</td>').join('')+
    '</tr>'
}

addTotal =  (total) => { 
    return  `<tr>
        <td colspan="5" style="text-align: right;">Grand Total</td>
        <td>`+total+`</td>
    </tr>`
}



module.exports = async (invNo) => {
    var html = `

<!doctype html>
<html>

<head>
    <meta charset="utf-8">
    <title>Horizont Invoice Template</title>

    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    

    <style>
        .invoice-box {
            /* max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0, 0, 0, .15);
        font-size: 16px;
        line-height: 24px;
        font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        color: #555; */
        }

        .invoice-box table {
            width: 100%;
            line-height: inherit;
            text-align: left;
        }

        .invoice-box table td {
            padding: 5px;
            vertical-align: top;
        }

        .invoice-box table tr td:nth-child(2) {
            text-align: right;
        }

        .invoice-box table tr.top table td {
            padding-bottom: 20px;
        }

        .invoice-box table tr.top table td.title {
            font-size: 45px;
            line-height: 45px;
            color: #333;
        }

        .invoice-box table tr.information table td {
            padding-bottom: 40px;
        }

        .invoice-box table tr.heading td {
            background: #eee;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
        }

        .invoice-box table tr.details td {
            padding-bottom: 20px;
        }

        .invoice-box table tr.item td {
            border-bottom: 1px solid #eee;
        }

        .invoice-box table tr.item.last td {
            border-bottom: none;
        }

        .invoice-box table tr.total td:nth-child(2) {
            border-top: 2px solid #eee;
            font-weight: bold;
        }

        @media only screen and (max-width: 600px) {
            .invoice-box table tr.top table td {
                width: 100%;
                display: block;
                text-align: center;
            }

            .invoice-box table tr.information table td {
                width: 100%;
                display: block;
                text-align: center;
            }
        }

        /** RTL **/

        .rtl {
            direction: rtl;
            font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        }

        .rtl table {
            text-align: right;
        }

        .rtl table tr td:nth-child(2) {
            text-align: left;
        }
    </style>
</head>

<body>
    <div class="invoice-box">
        <table cellpadding="0" cellspacing="0">
            <tr class="top">
                <td colspan="2">
                    <table>
                        <tr>
                            <td class="title" style="padding:0; vertical-align: text-top">
                                Horizont
                            </td>

                            <td>
                                Invoice #: !!!invno!!!
                                <br> Created: !!!created!!!
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>

            <tr class="information">
                <td colspan="2">
                    <table>
                        <tr>
                            <td>
                                Horizont, Inc.
                                <br> Line 1
                                <br> Line 2
                            </td>

                            <td>
                                Acme Corp.
                                <br> John Doe
                                <br> john@example.com
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>

            <tr class="heading">
                <td>
                    Payment Method
                </td>

                <td>
                    Information
                </td>
            </tr>

            <tr class="details">
                <td>
                    Bank Transfer
                </td>

                <td>
                    KBANK: 077-2-42531-5
                </td>
            </tr>

        </table>


        <table class="table table-striped" style="width:100%" id="invoice_item">
            <colgroup>
                <col width="5%">
                <col width="55%">
                <col width="10%">
                <col width="10%">
                <col width="10%">
                <col width="10%">
            </colgroup>
            <thead>
                <tr class="heading">
                    <td>No</td>
                    <td>Description</td>
                    <td>Unit</td>
                    <td>Price</td>
                    <td>Qty.</td>
                    <td>Total</td>
                </tr>
            </thead>
            <tbody>
                !!!body!!!

            </tbody>
            <tfoot>
                !!!total!!!
            </tfoot>
        </table>

    </div>
</body>



</html>
`
    var fs = require('fs');


    data = {
        total: 62,
        arrayitem: [
            {
                item: "PCF ไก่หมักซอสพริกไทยดำ  แพ็คละ 1 กก.",
                unit: "Kg",
                unitprice: "62",
                qty: 1,
                price: 62,
            }
        ],
        datetime: "1527757786274",
        delivery: "2018-06-01",
        status: "SCHEDULED",
        customer: "A. ",
        created: "2018-05-31T16:07:50.126Z",
        updated: "2018-05-31T16:07:50.126Z",
        id: "ORD7507246849",
        _id: "1eCuTewIg9Zcr7B0",
        payment: "kbank",
        payment_ref: "114155989161",
        vendor: "พีซี ฟูดส์ เซ็นเตอร์",
        po: {
            id: "PO7507246849",
            status: "RAISED",
        },
    }
    

    data = await findinv(invNo);

    // Add Items
    no = 1;

    if(data){
        arritem = data.arrayitem
        .map(item => Object.assign({no: (no++).toString()}, item))
        .map(item => { Object.keys(item).map(col => { if(item[col].toFixed) item[col] = item[col].toFixed(2) });  return item} )
        .map(addToTable)
        .join("")

   
        totalitem = addTotal(data.total)  
    }
    else{
        arritem = ''
        totalitem = ''
    }

    let newhtml = html
        .replace('!!!body!!!', arritem)
        .replace('!!!total!!!', totalitem)
        .replace('!!!invno!!!', invNo)
        .replace('!!!created!!!', "June 1 2018")



    fs.writeFileSync('./template_gen/template/'+invNo+'.html', newhtml);
    return './template_gen/template/'+invNo+'.html'
}