#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/13
from math import sin, radians, fabs, cos, asin, sqrt, atan2, pi
from geohelper import bearing
# EARTH_RADIUS = 6371  # 地球平均半径，6371km
EARTH_RADIUS = 6378.1
# 1nm = 1.852km
n_mile = 1.852


def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance_hav(lat0, lng0, lat1, lng1):
    # 用haversine公式计算球面两点间的距离
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance / n_mile


def mid_point(lat0, lon0, lat1, lon1):
    """
    mid_point(*args): Mid point between two latitude and longitude
    return: Mid Point(mid_lat, mid_lon)
    Unit: degree(°)
    """
    # 经差dLon
    dLon = radians(lon1 - lon0)
    # 将经纬度转弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lon0 = radians(lon0)
    Bx = cos(lat1) * cos(dLon)
    By = cos(lat1) * sin(dLon)
    x = sqrt((cos(lat0) + Bx) * (cos(lat0) + Bx) + pow(By, 2))
    y = sin(lat0) + sin(lat1)
    mid_lat = 180 / pi * atan2(y, x)
    mid_lon = 180 / pi * (lon0 + atan2(By, cos(lat0) + Bx))
    return mid_lat, mid_lon
