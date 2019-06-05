#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/13
from geohelper import bearing
from CPA.Distance import get_distance_hav
from math import sqrt, sin, cos, pi, acos


def cpa(Tar_Ship, Ref_Ship):
    """
    计算目标船与参考船之间的DCPA和DCPA
    Tar_Ship: 目标船
    Ref_Ship: 参考船
    return:  DCPA、TCPA
    """
    Tar_Lat, Tar_Lon = float(Tar_Ship.LAT), float(Tar_Ship.LON)
    Tar_Cog, Tar_Sog = float(Tar_Ship.COG), float(Tar_Ship.SOG)
    Ref_Lat, Ref_Lon = float(Ref_Ship.LAT), float(Ref_Ship.LON)
    Ref_Cog, Ref_Sog = float(Ref_Ship.COG), float(Ref_Ship.SOG)

    # 两船之间的距离distance
    distance = get_distance_hav(Tar_Lat, Tar_Lon, Ref_Lat, Ref_Lon)

    alpha = Tar_Cog - Ref_Cog
    if alpha > 180:
        alpha -= 360
    elif alpha < -180:
        alpha += 360

    # 两船之间的相对速度Relative_Speed
    Relative_Speed = sqrt(Tar_Sog**2 + Ref_Sog**2 - 2*Tar_Sog*Ref_Sog*cos(alpha / 180.0 * pi))
    Q = acos((Relative_Speed**2 + Tar_Sog**2 - Ref_Sog**2) / (2 * Relative_Speed * Tar_Sog)) * 180.0 / pi

    # 两船之间的相对航向Relative_Course
    if alpha > 0:
        Relative_Course = Tar_Cog + Q
    else:
        Relative_Course = Tar_Cog - Q
    # 相对舷角Bearing
    Bearing = bearing.initial_compass_bearing(Tar_Lat, Tar_Lon, Ref_Lat, Ref_Lon) - Relative_Course
    DCPA = distance * sin(Bearing * pi / 180.0)
    TCPA = distance * cos(Bearing * pi / 180.0) / Relative_Speed
    return DCPA, TCPA



