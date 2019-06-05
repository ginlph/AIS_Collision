#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/7
import json
import numpy as np
from datetime import datetime
from datetime import timedelta
"""
    研究区域:
            (Longitude, Latitude)
        Left Corner:    Right Corner:
        (120°, 30°)     (125°, 35°)

    网格精度:
            0.5° * 0.5°
    
    时间范围:
            2016-10-01 2016-10-31
"""

# generate time data


def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step


longitude = np.arange(120, 125, 0.5)
latitude = np.arange(30, 35, 0.5)
Time = date_range(datetime(2016, 10, 1), datetime(2016, 11, 1), timedelta(hours=1))

# 建立网格
grid_index = list()
for time in Time:
    count = 0
    _time = datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
    temporary = []
    for lat in latitude:
        for lon in longitude:
            sub_grid = {
                "Left": {"Lon": lon, "Lat": lat},
                "Right": {"Lon": lon + 0.5, "Lat": lat + 0.5}
            }

            if (lat == min(latitude) and lon == min(longitude)) or \
                    (lat == max(latitude) and lon == max(longitude)) or \
                    (lat == min(latitude) and lon == max(longitude)) or \
                    (lat == max(latitude) and lon == min(longitude)):
                sub_grid['Flag'] = 1
            elif (lat == min(latitude) and min(longitude) < lon < max(longitude)) or \
                    (lat == max(latitude) and min(longitude) < lon < max(longitude)) or \
                    (lon == min(longitude) and min(latitude) < lat < max(latitude)) or \
                    (lon == max(longitude) and min(latitude) < lat < max(latitude)):
                sub_grid['Flag'] = 2
            else:
                sub_grid['Flag'] = 3
            sub_grid['area_id'] = count
            count += 1
            temporary.append(sub_grid)
    grid_index.append({_time: temporary})


with open('test_grid.json', 'w') as f:
    json.dump(grid_index, f)

