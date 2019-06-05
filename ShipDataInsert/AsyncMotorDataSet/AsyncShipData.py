#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/7
import os
import logging
import time
import asyncio
import motor.motor_asyncio
from datetime import datetime
path = '/Volumes/My Passport/test_motor'

# Support URL
# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

# Getting a Database
db = client.ais_motor

# Getting a Collection
collection = db.test_motor

file_path = [
    os.path.join(root, file)
    for root, dirs, files in os.walk(path)
    for file in files
]

print("There are {} endswith txt files".format(len(file_path)))

# Inserting a Document


async def do_insert():
    start = time.time()
    for file in file_path:
        single_ship = list()
        if not os.path.getsize(file):
            print("This {} is None".format(file))
        else:
            with open(file, encoding='utf8') as f:
                try:
                    for line in f:
                        lines = line.strip().split(';')
                        ship_info = {
                            "MMSI": int(lines[0]),
                            "TIME": datetime.strptime(lines[1], "%Y-%m-%d %H:%M:%S"),
                            "location": {
                                "type": "Point",
                                "coordinates": [
                                    float(lines[2]), float(lines[3])
                                ]
                            },
                            "COG": float(lines[4]),
                            "SOG": float(lines[5])
                        }
                        single_ship.append(ship_info)
                    result = await collection.insert_many(single_ship)
                    print('inserted %d ShipInfo' % (len(result.inserted_ids),))
                except Exception as e:
                    logging.exception(e)
                    print("The file path is {}".format(file))
                    print("Reason: ", e)
    end = time.time()
    total = end - start
    print("Total time spent inserting the MongoDB: " + str(total) + " s.")

loop = asyncio.get_event_loop()
loop.run_until_complete(do_insert())
print("All txt files have already inserted in the MongoDB")