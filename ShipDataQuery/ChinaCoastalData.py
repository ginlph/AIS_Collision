#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/5
import json
import csv
import time
from pymongo import MongoClient
from ShipDataQuery.ComplexEncoder import ComplexEncoder
"""
    研究区域:
            (Longitude, Latitude)
        Left Corner:    Right Corner:
        (120°, 30°)     (125°, 35°)

    网格精度:
            0.5° * 0.5°
    
    Polygon:
            [
                [
                    [120, 30], 
                    [125, 30],
                    [125, 35],
                    [120, 35],
                    [120, 30]
                ]
            ]
    
    导出形式:
            ChinaCoastalData.json
                
    将位于上述网格区域内的所有船舶经、纬度从mongodb数据库中筛选出来
"""

# 使用mongodb登录
client = MongoClient('localhost', 27017)
# 数据库database: ais_motor
db = client.ChinaCoastalData
# 集合collection: test_motor
collection = db.chinacoastaldata

# 开始时间
start = time.time()

results = collection.find({
    "TIME": {
        "$gte": "2016-10-01",
        "$lt": "2016-10-02"
    },
    "location": {
        "$geoWithin": {
            "$geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [120, 30],
                        [125, 30],
                        [125, 35],
                        [120, 35],
                        [120, 30]
                    ]
                ]
            }
        }
    }
}, {"_id": 0})


"""
# 使用.json格式储存Polygon中的船舶AIS数据
将查询结果写入ChinaCoastalData.json
ship_info = [{"MMSI": result["MMSI"], "TIME": result["TIME"], "LON": result["location"]["coordinates"][0],
              "LAT": result["location"]["coordinates"][1], "COG": result["COG"], "SOG": result["SOG"]}
             for result in results]
with open('./ChinaCoastalData/2016_10_01.json', 'w') as file_object:
    json.dump(ship_info, file_object, cls=ComplexEncoder)
"""


# 使用.csv格式存储Polygon中的船舶AIS数据
with open('./ChinaCoastalData/2016_10_01_test.csv', 'w') as f_write:
    datas = csv.writer(f_write)
    Header = ["MMSI", "TIME", "LON", "LAT", "COG", "SOG"]
    datas.writerow(Header)
    for result in results:
        datas.writerow([
            result["MMSI"],
            result["TIME"],
            result["location"]["coordinates"][0],
            result["location"]["coordinates"][1],
            result["COG"],
            result["SOG"]
        ])

# 结束时间
end = time.time()
# 总用时
total = end - start

print("-------------------------------------")
print("*********The Work is done!***********")
print("The total Time is {}!".format(total))
# print("The query has {} documents!".format(len(ship_info)))
print("-------------------------------------")

