#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/4/26
import datetime
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.inventory
collection = db.test_collection

# data
post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()
}

# 插入document
# collection.insert_one(post)

# 重点！！！Bulk insert
# 大量插入！insert_many()

new_posts = [
    {
        "author": "Mike",
        "text": "Another post!",
        "tags": ["bulk", "insert"],
        "date": datetime.datetime(2009, 11, 12, 11, 14)
    },
    {
        "author": "Eliot",
        "title": "MongoDB is fun",
        "text": "and pretty easy too!",
        "date": datetime.datetime(2009, 11, 10, 10, 45)
    }
]

# result = collection.insert_many(new_posts)
# for i in collection.find({"author": "Mike"}):
#     print(i)

# Range Queries
d = datetime.datetime(2009, 11, 12, 12)
for i in collection.find({"date": {"$lte": d}}, {"_id": 0}).sort("author"):
    pprint(i)

# Indexing

# sort、limit
# for info in collection.find({"MMSI": 488000172}).sort('TIME', pymongo.ASCENDING).limit(3):
#     pprint(info)

# explain
"""
pprint(db.command(
   {
      "explain": {"count": "test_ais", "query": {"MMSI": 488000172} },
      "verbosity": "executionStats"
   }
)['executionStats'])

"""