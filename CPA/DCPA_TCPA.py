#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/18
import numpy as np


class CPA:
    """
    1. The Distance between Target Ship and Reference Ship
        get_distance_hav(*args):
    args = (lat1, lon1, lat2, lon2)

    2. The Mid Point between Target Ship and Reference Ship
        min_point(*args)
    args = (lat1, lon1, lat2, lon2)

    3. The DCPA and TCPA between Target Ship and Reference Ship
        cpa(*args):
    args = (Tar_Ship, Ref_Ship)
    Tar_Ship: Target Vessel Object, Ref_Ship: Reference Vessel Object
    """
    EARTH_RADIUS = 6378.1
    n_mile = 1.852

    def __init__(self, Tar_Ship, Ref_Ship):
        self.Tar_Lat = float(Tar_Ship.LAT)
        self.Tar_Lon = float(Tar_Ship.LON)
        self.Ref_Lat = float(Ref_Ship.LAT)
        self.Ref_Lon = float(Ref_Ship.LON)
        self.Tar_Cog = float(Tar_Ship.COG)
        self.Tar_Sog = float(Tar_Ship.SOG)
        self.Ref_Cog = float(Ref_Ship.COG)
        self.Ref_Sog = float(Ref_Ship.SOG)

    def haversine(self, theta):
        return pow(np.sin(theta / 2), 2)

    def distance(self):
        """
        Use Haversine formula To Calculate The Distance Between Tar_Ship and Ref_Ship On The Sphere
        return: The distance between Tar_Ship and Ref_Ship
        Unit: nm
        """
        Tar_Lat, Tar_Lon = np.radians((self.Tar_Lat, self.Tar_Lon))
        Ref_Lat, Ref_Lon = np.radians((self.Ref_Lat, self.Ref_Lon))
        diff_lon = np.fabs(Tar_Lon - Ref_Lon)
        diff_lat = np.fabs(Tar_Lat - Ref_Lat)
        h = self.haversine(diff_lat) + np.cos(Tar_Lat) * np.cos(Ref_Lat) * self.haversine(diff_lon)
        distance = 2 * CPA.EARTH_RADIUS * np.arcsin(np.sqrt(h))
        return distance / CPA.n_mile

    def mid_point(self):
        """
        mid_point(): Mid point between two latitude and longitude
        return: Mid Point(mid_lat, mid_lon)
        Unit: degree(°)
        """
        Tar_Lat, Tar_Lon = np.radians((self.Tar_Lat, self.Tar_Lon))
        Ref_Lat, Ref_Lon = np.radians((self.Ref_Lat, self.Ref_Lon))
        diff_lon = Ref_Lon - Tar_Lon
        Bx = np.cos(Ref_Lat) * np.cos(diff_lon)
        By = np.cos(Ref_Lat) * np.sin(diff_lon)
        x = np.sqrt((np.cos(Tar_Lat) + Bx) * (np.cos(Tar_Lat) + Bx) + pow(By, 2))
        y = np.sin(Tar_Lat) + np.sin(Ref_Lat)
        mid_lat = 180 / np.pi * np.arctan2(y, x)
        mid_lon = 180 / np.pi * (Tar_Lon + np.arctan2(By, np.cos(Tar_Lat) + Bx))
        return mid_lat, mid_lon

    def bearing(self):

        tar_lat, ref_lat = np.radians((self.Tar_Lat, self.Ref_Lat))
        diff_lon = np.radians(self.Ref_Lon-self.Tar_Lon)

        x = np.sin(diff_lon) * np.cos(ref_lat)
        y = (np.cos(tar_lat) * np.sin(ref_lat)) - (np.sin(tar_lat) * np.cos(ref_lat) * np.cos(diff_lon))

        inital_bearing = np.arctan2(x, y)
        inital_bearing = np.rad2deg(inital_bearing)
        compass_bearing = (inital_bearing + 360) % 360
        return compass_bearing

    def cpa(self):
        """
            The Method of Calculate DCPA and TCPA
            return: (DCPA, TCPA)
        """
        alpha = self.Tar_Cog - self.Ref_Cog
        if alpha > 180:
            alpha -= 360
        elif alpha < -180:
            alpha += 360

        # 两船之间的相对速度Relative_Speed
        temp = 2 * self.Tar_Sog * self.Ref_Sog * np.cos(alpha / (180 * np.pi))
        Relative_Speed = np.sqrt(pow(self.Tar_Sog, 2) + pow(self.Ref_Sog, 2) - temp)

        # 舷角Q
        x = pow(Relative_Speed, 2) + pow(self.Tar_Sog, 2) - pow(self.Ref_Sog, 2)
        y = 2 * Relative_Speed * self.Tar_Sog
        Q = np.arccos(x / y) * 180.0 / np.pi

        # 两船之间的相对航向Relative_Course
        if alpha > 0:
            Relative_Course = self.Tar_Cog + Q
        else:
            Relative_Course = self.Tar_Cog - Q

        # 相对舷角Bearing
        Bearing = self.bearing() - Relative_Course

        # 计算Tar_Ship和Ref_Ship之间的DCPA和TCPA
        DCPA = self.distance() * np.sin(Bearing * np.pi / 180.0)
        TCPA = self.distance() * np.cos(Bearing * np.pi / 180.0) / Relative_Speed

        return DCPA, TCPA

