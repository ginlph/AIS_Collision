#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/13
import numpy as np

# 网格范围
longitude = np.arange(120, 126, 0.5)
latitude = np.arange(30, 36, 0.5)


class Grid:
    grid_delta = 0.5
    LON_LENGTH = len(longitude)

    def __init__(self, area_ID):
        # 根据传进来的网格编号area_ID, 可以直接定位该网格左下角的经纬度
        # 省了两层嵌套for循环
        self.area_ID = area_ID
        self.Left_lon = longitude[area_ID % Grid.LON_LENGTH]
        self.Left_lat = latitude[area_ID // Grid.LON_LENGTH]
        self.Right_lon = self.Left_lon + Grid.grid_delta
        self.Right_lat = self.Left_lat + Grid.grid_delta
        self.flag = 3
        if self.Left_lat == min(latitude) or self.Left_lat == max(latitude):
            self.flag = 2
            if self.Left_lon == min(longitude) or self.Left_lon == max(longitude):
                self.flag = 1
        if self.Left_lon == min(longitude) or self.Left_lon == max(longitude):
            self.flag = 2
            if self.Left_lat == min(latitude) or self.Left_lat == max(latitude):
                self.flag = 1
        self.need_ID = None

    def need_id(self):
        if self.flag == 3:  # 中部网格计算, flag=3
            id_1 = self.area_ID
            id_2 = self.area_ID + 1
            id_3 = self.area_ID + Grid.LON_LENGTH - 1
            id_4 = self.area_ID + Grid.LON_LENGTH
            id_5 = self.area_ID + Grid.LON_LENGTH + 1
            self.need_ID = [id_1, id_2, id_3, id_4, id_5]
        elif self.flag == 2:  # 4种边界网格计算, flag=2
            if self.Left_lat == min(latitude):
                id_1 = self.area_ID
                id_2 = self.area_ID + 1
                id_3 = self.area_ID + Grid.LON_LENGTH - 1
                id_4 = self.area_ID + Grid.LON_LENGTH
                id_5 = self.area_ID + Grid.LON_LENGTH + 1
                self.need_ID = [id_1, id_2, id_3, id_4, id_5]
            elif self.Left_lat == max(latitude):
                id_1 = self.area_ID
                id_2 = self.area_ID + 1
                self.need_ID = [id_1, id_2]
            elif self.Left_lon == min(longitude):
                id_1 = self.area_ID
                id_2 = self.area_ID + 1
                id_3 = self.area_ID + Grid.LON_LENGTH
                id_4 = self.area_ID + Grid.LON_LENGTH + 1
                self.need_ID = [id_1, id_2, id_3, id_4]
            elif self.Left_lon == max(longitude):
                id_1 = self.area_ID
                id_2 = self.area_ID + Grid.LON_LENGTH - 1
                id_3 = self.area_ID + Grid.LON_LENGTH
                self.need_ID = [id_1, id_2, id_3]
        elif self.flag == 1:  # 网格4个角落, flag=1
            if self.Left_lon == min(longitude) and self.Left_lat == min(latitude):
                id_1 = self.area_ID
                id_2 = self.area_ID + 1
                id_3 = self.area_ID + Grid.LON_LENGTH
                id_4 = self.area_ID + Grid.LON_LENGTH + 1
                self.need_ID = [id_1, id_2, id_3, id_4]
            elif self.Left_lon == max(longitude) and self.Left_lat == min(latitude):
                id_1 = self.area_ID
                id_2 = self.area_ID + Grid.LON_LENGTH - 1
                id_3 = self.area_ID + Grid.LON_LENGTH
                self.need_ID = [id_1, id_2, id_3]
            elif self.Left_lon == min(longitude) and self.Left_lat == max(latitude):
                id_1 = self.area_ID
                id_2 = self.area_ID + 1
                self.need_ID = [id_1, id_2]
            elif self.Left_lon == max(longitude) and self.Left_lat == max(latitude):
                id_1 = self.area_ID
                self.need_ID = [id_1]
        return self.need_ID
