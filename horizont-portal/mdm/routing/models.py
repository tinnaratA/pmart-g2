from django.db import models
from customer_store.models import stores

routing = {
    "sale1": {
        "id": 1,
        "name": "route1",
        "customer_store": [
            stores[0],
            stores[1],
            stores[2]
        ]
    },
    "sale2": {
        "id": 2,
        "name": "route2",
        "customer_store": [
            stores[3],
            stores[4],
            stores[5]
        ]
    },
    "sale3": {
        "id": 3,
        "name": "route3",
        "customer_store": [
            stores[6],
            stores[7],
            stores[8]
        ]
    }
}