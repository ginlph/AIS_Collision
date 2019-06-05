#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/5
import json
import time
from datetime import datetime
from pymongo import MongoClient
from ShipDataQuery.ComplexEncoder import ComplexEncoder
from pprint import pprint

# 使用mongodb登录
client = MongoClient('localhost', 27017)
# 数据库database: ais
db = client.ais
# 集合collection: trajectory4
collection = db.trajectory4
# 开始时间
start_time = time.time()
results = collection.find({
    "TIME": {
        "$gte": datetime(2016, 12, 1),
        "$lte": datetime(2016, 12, 2)
    }, "location": {
        "$geoWithin": {
            "$geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [110, 39],
                        [130, 39],
                        [130, 42],
                        [110, 42],
                        [110, 39]
                    ]
                ]
            }
        }
    }
}, {"_id": 0})

# 将查询结果写入yao11.json
ship_info = [{'location': result['location']['coordinates']} for result in results]
with open('2016_12_01to02.json', 'w') as file_object:
    json.dump(ship_info, file_object, cls=ComplexEncoder)

# 结束时间
end_time = time.time()
total_time = end_time - start_time
print("Total time spent query the MongoDB: " + str(total_time) + " s.")
print("------**********---------")
print("The Work is done!")
# print("The total Time is {}!".format(total_time))
print("The query has {} documents!".format(len(ship_info)))
print("------**********---------")