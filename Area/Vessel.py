#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/13
from Area.Grid import Grid


class Vessel(Grid):
    def __init__(self, area_ID, args):
        self.MMSI = args[0]
        self.TIME = args[1]
        self.LON = args[2]
        self.LAT = args[3]
        self.COG = args[4]
        self.SOG = args[5]
        Grid.__init__(self, area_ID)

