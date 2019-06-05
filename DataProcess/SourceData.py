#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/19
import csv
import numpy as np
from _Time.TimeStamp import date_range
from _Time.ParseTime import parse_time
from datetime import timedelta
from BinarySearch import BinarySearch
from Area.Vessel import Vessel

#*********************************************************
#           SourceData.py
# SourceData文件夹存放原始数据
# 存储在网格中船舶数据形式:
#    [{"AIS delta_time": [Vessel_1(area_id, args), ...]},
#                       ......                          ,
#     {"AIS delta_time": [Vessel_i(area_id, args), ...]}]
# 其中:
#     AIS delta_time: AIS播发间隔
# Vessel(area_id, args): 船舶对象
# (area_id: 网格编号, args: 船舶属性, 如MMSI、TIME...)
#*********************************************************


# 网格范围
longitude = np.arange(120, 126, 0.5)
latitude = np.arange(30, 36, 0.5)

# longitude的长度
Lon_Length = len(longitude)

# 起始时间
start = parse_time("2016-10-01 00:00:00")
# 终止时间
end = parse_time("2016-10-02 00:00:05")
# 时间步长step
step = timedelta(seconds=5)


def source_data(path):
    # AIS存储网格区域
    grids = [{time_: list()} for time_ in date_range(start, end, step)]
    with open(path) as f_object:
        datas = csv.reader(f_object)
        # data: ['MMSI', 'TIME', 'LON', 'LAT', 'COG', 'SOG']
        next(datas)
        for data in datas:
            # 根据经、纬度(data[2], data[3])确定网格编号area_ID
            if int(data[2][4]) >= 5 or int(data[3][3]) >= 5:
                _lon = int(data[2][: 3]) + 0.5
                _lat = int(data[3][: 2]) + 0.5
            else:
                _lon = int(data[2][: 3])
                _lat = int(data[3][: 2])
            print("_lon: ", _lon, "_lat: ", _lat)
            lon_remainder = int(*np.where(longitude == _lon))
            lat_quotient = int(*np.where(latitude == _lat))
            area_ID = lat_quotient * Lon_Length + lon_remainder
            time = parse_time(data[1])
            time_remainder = time.second % 10
            if time_remainder in range(8, 10):
                s = 10 - time_remainder
                _time = time + timedelta(seconds=s)
            elif time_remainder in range(0, 3):
                _time = time - timedelta(seconds=time_remainder)
            elif time_remainder in range(3, 6):
                s = 5 - time_remainder
                _time = time + timedelta(seconds=s)
            else:
                s = time_remainder - 5
                _time = time - timedelta(seconds=s)
            grids[BinarySearch(grids, _time)][_time].append(Vessel(area_ID, data))
    return grids