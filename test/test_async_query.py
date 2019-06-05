#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/7
import time
import asyncio
import motor.motor_asyncio
from datetime import datetime
from pprint import pprint

# Support URL
# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

# Getting a Database
db = client.ais_motor

# Getting a Collection
collection = db.test_motor


async def do_find():
    start = time.time()
    cursor = collection.find({
    "TIME": {
        "$gte": datetime(2016, 12, 25),
        "$lte": datetime(2016, 12, 26)
    }, "location": {
        "$geoWithin": {
            "$geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [109, 23],
                        [130, 23],
                        [130, 40],
                        [109, 40],
                        [109, 23]
                    ]
                ]
            }
        }
    }
}, {"_id": 0})
    # async for document in cursor:
    #     pprint(document)
    ship_info = [{'location': result['location']['coordinates']} async for result in cursor]
    print(ship_info[0])
    end = time.time()
    total = end - start
    print("Total time spent query the MongoDB: " + str(total) + " s.")

loop = asyncio.get_event_loop()
loop.run_until_complete(do_find())
