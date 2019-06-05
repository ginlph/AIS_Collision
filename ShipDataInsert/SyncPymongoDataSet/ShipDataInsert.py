#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/2/18
import os
import time
import logging
import pymongo
from pymongo import MongoClient
from datetime import datetime

path = '/Users/lipenghao/Desktop/test_motor'
# path = '/Volumes/My Passport/ais_data_/allshipsin2017_trajectory4'

"""
使用mongodb登录
"""
client = MongoClient('localhost', 27017)
# 数据库database: ais_example
db = client.ais_sync
# 集合collection: test_ais
collection = db.test_sync


file_path = [
    os.path.join(root, file)
    for root, dirs, files in os.walk(path)
    for file in files
]

print("There are {} endswith txt files".format(len(file_path)))

start_time = time.time()

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
                result = collection.insert_many(single_ship)
                print('inserted %d ShipInfo' % (len(result.inserted_ids),))
            except Exception as e:
                logging.exception(e)
                print("The file path is {}".format(file))
                print("Reason: ", e)


end_time = time.time()
total_time = end_time - start_time
print("All txt files have already inserted in the MongoDB")
print("Total time spent inserting the MongoDB: " + str(total_time) + " s.")