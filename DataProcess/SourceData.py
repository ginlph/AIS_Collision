#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/19
import csv
import numpy as np
from datetime import timedelta

from _Time.TimeStamp import date_range
from _Time.ParseTime import parse_time
from BinarySearch import BinarySearch
from Area.Vessel import Vessel

#************************************************************************************************
#                                      SourceData.py
# Parameter:
#       path(元数据路径): "../ShipDataQuery/ChinaCoastalData/year-month-day.csv"
#       longitude(研究区域经度范围) = np.arange(...)
#       latitude(研究区域纬度范围) = np.arange(...)
#       delta(网格粒度) = 0.5
#       **kwargs(时间范围) = start、end、step
# Return:
#       grids:
#           存储网格及网格中船舶的list
#       数据形式:
#           [
#               {"AIS delta_time": [Vessel_1(area_id, args, longitude, latitude, delta), ...]},
#                     ......                  ......              ......                      ,
#           {"AIS delta_time": [Vessel_i(area_id, args, longitude, latitude, delta), ...]}
#        ]
#************************************************************************************************


def source_data(path, *, longitude, latitude, delta, **kwargs):
    lon_length = longitude.size
    # AIS存储网格区域
    # grids = [{time_: list()} for time_ in date_range(start, end, step)]
    grids = [{"TIME": time_, "SHIP_INFO": list()}
        for time_ in date_range(
            kwargs['start'], kwargs['end'], kwargs['step']
        )
    ]
    with open(path) as f_object:
        datas = csv.reader(f_object)
        # data: ['MMSI', 'TIME', 'LON', 'LAT', 'COG', 'SOG']
        next(datas)
        for data in datas:
            lon, lat = data[2], data[3]
            lon_, lat_ = 0, 0
            # 根据经、纬度(data[2], data[3])确定网格编号area_ID
            if int(lon[4]) < 5 and int(lat[3]) < 5:
                lon_ = int(lon[: 3])
                lat_ = int(lat[: 2])
            elif int(lon[4]) >= 5 and int(lat[3]) >= 5:
                lon_ = int(lon[: 3]) + 0.5
                lat_ = int(lat[: 2]) + 0.5
            elif int(lon[4]) < 5 and int(lat[3]) >= 5:
                lon_ = int(lon[: 3])
                lat_ = int(lat[: 2]) + 0.5
            elif int(lon[4]) >= 5 and int(lat[3]) < 5:
                lon_ = int(lon[: 3]) + 0.5
                lat_ = int(lat[: 2])
            else:
                print("")
                print("Can't convert to grid index!!!")
                print("Can't find {}/{}".format(lon, lat))
            print("_lon: ", lon_, "_lat: ", lat_)
            lon_remainder = int(*np.where(longitude == lon_))
            lat_quotient = int(*np.where(latitude == lat_))
            # are_id 根据该船当前时刻的经、纬度, 判断出该船所属网格编号
            area_id = lat_quotient * lon_length + lon_remainder
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
            grids[BinarySearch(grids, _time)]["SHIP_INFO"].append(Vessel(
                area_id, data, gridlon_=longitude, gridlat_=latitude, grid_delta=delta
            ))
    return grids