from django.db import models

customers = [
    {
        "id": 1,
        "first_name": "วิลเลี่ยม",
        "middle_name": None,
        "last_name": "ศักดิ์สกุล"
    },
    {
        "id": 2,
        "first_name": "วิลล์",
        "middle_name": None,
        "last_name": "กาแก้วมิดมาน"
    },
    {
        "id": 3,
        "first_name": "เทิด",
        "middle_name": None,
        "last_name": "สมิตต์"
    },
    {
        "id": 4,
        "first_name": "บุญชู",
        "middle_name": None,
        "last_name": "แจ็คสัน"
    }
]

store_types = [
    {
        "id": 1,
        "code": "A",
        "name": "ร้านก๋วยเตี๋ยว"
    },
    {
        "id": 2,
        "code": "B",
        "name": "ร้านอาหารตามสั่ง"
    },
    {
        "id": 3,
        "code": "C",
        "name": "ภัตตาคาร"
    }
]

store_addresses = [
    {
        "line1": "1/1",
        "line2": None,
        "district": "หัวหมาก",
        "city": "บางกะปิ",
        "province": "กรุงเทพมหานคร ฯ",
        "postcode": "10240",
        "latitude": "52º66'11\"N",
        "longitude": "140º23'21\"E"

    },
    {
        "line1": "1/2",
        "line2": None,
        "district": "สวนหลวง",
        "city": "สวนหลวง",
        "province": "กรุงเทพมหานคร ฯ",
        "postcode": "10250",
        "latitude": "39º25'11\"N",
        "longitude": "125º28'01\"E"
    },
    {
        "line1": "1/3",
        "line2": None,
        "district": "คลองจั่น",
        "city": "บางกะปิ",
        "province": "กรุงเทพมหานคร ฯ",
        "postcode": "10240",
        "latitude": "41º25'01\"N",
        "longitude": "120º25'01\"E"
    }
]

stores = [
    {
        "id": 1,
        "name": "A",
        "owner": [
            customers[0],
            customers[1]
        ],
        "type": store_types[0],
        "address": store_addresses[0]
    },
    {
        "id": 2,
        "name": "B",
        "owner": [
            customers[1],
            customers[2]
        ],
        "type": store_types[1],
        "address": store_addresses[1]
    },
    {
        "id": 3,
        "name": "C",
        "owner": [
            customers[0],
            customers[2]
        ],
        "type": store_types[2],
        "address": store_addresses[2]
    },
    {
        "id": 4,
        "name": "D",
        "owner": [
            customers[3],
            customers[1]
        ],
        "type": store_types[0],
        "address": store_addresses[0]
    },
    {
        "id": 5,
        "name": "E",
        "owner": [
            customers[3],
            customers[2]
        ],
        "type": store_types[1],
        "address": store_addresses[1]
    },
    {
        "id": 6,
        "name": "F",
        "owner": [
            customers[1],
            customers[3]
        ],
        "type": store_types[2],
        "address": store_addresses[2]
    },
    {
        "id": 7,
        "name": "G",
        "owner": [
            customers[3],
            customers[0]
        ],
        "type": store_types[0],
        "address": store_addresses[0]
    },
    {
        "id": 8,
        "name": "H",
        "owner": [
            customers[1],
            customers[3]
        ],
        "type": store_types[1],
        "address": store_addresses[1]
    },
    {
        "id": 9,
        "name": "I",
        "owner": [
            customers[0],
            customers[1]
        ],
        "type": store_types[2],
        "address": store_addresses[2]
    }
]

orders = [
    {
        "id": 1,
        "store": st,
        "order_list": [
            "หมูสามชั้น",
            "ปลากะพง",
            "หมูสันนอก",
            "กุ้งแม่น้ำ",
            "เนื้อแกะ"
        ]
    } for st in stores
]