#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/6/29
import json
import numpy as np
import pandas as pd
import matplotlib.path as mplPath


origin_path = './Temporary_Data/2016-10-01.csv'
geojson_path = './channel_geojson/map.geojson'

origin_data = pd.read_csv(origin_path)

with open(geojson_path) as f:
    geojson_data = json.load(f)


longitude = origin_data.LON.values
latitude = origin_data.LAT.values
points = np.column_stack((longitude, latitude))
PolygonLen = len(geojson_data['features'])

for i in range(PolygonLen):
    polygon = geojson_data['features'][i]['geometry']['coordinates'][0]
    path = mplPath.Path(polygon)
    selector = path.contains_points(points)
    index = origin_data[selector].index
    points = np.delete(points, np.where(selector), axis=0)
    origin_data.drop(index, inplace=True)

origin_data.to_csv('./Meta_Data/2016-10-01.csv', index=None)

