#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/13


class Grid:

    def __init__(self, area_id, *, gridlon_, gridlat_, grid_delta):
        # 根据传进来的网格编号area_id, 可以直接定位该网格左下角的经纬度
        # 省了两层嵌套for循环

        # 网格属性
        self.area_id = area_id
        self.gridlon_ = gridlon_
        self.gridlat_ = gridlat_
        self.grid_delta = grid_delta
        self.gridlon__length = self.gridlon_.size
        
        self.Leftlon_ = self.gridlon_[area_id % self.gridlon__length]
        self.Leftlat_ = self.gridlat_[area_id // self.gridlon__length]
        self.Rightlon_ = self.Leftlon_ + self.grid_delta
        self.Rightlat_ = self.Leftlat_ + self.grid_delta
        self.flag = 3
        if self.Leftlat_ == min(self.gridlat_) or self.Leftlat_ == max(self.gridlat_):
            self.flag = 2
            if self.Leftlon_ == min(self.gridlon_) or self.Leftlon_ == max(self.gridlon_):
                self.flag = 1
        if self.Leftlon_ == min(self.gridlon_) or self.Leftlon_ == max(self.gridlon_):
            self.flag = 2
            if self.Leftlat_ == min(self.gridlat_) or self.Leftlat_ == max(self.gridlat_):
                self.flag = 1
        self.need_ID = None

    def need_id(self):
        if self.flag == 3:  # 中部网格计算, flag=3
            id_1 = self.area_id
            id_2 = self.area_id + 1
            id_3 = self.area_id + self.gridlon__length - 1
            id_4 = self.area_id + self.gridlon__length
            id_5 = self.area_id + self.gridlon__length + 1
            self.need_ID = [id_1, id_2, id_3, id_4, id_5]
        elif self.flag == 2:  # 4种边界网格计算, flag=2
            if self.Leftlat_ == min(self.gridlat_):
                id_1 = self.area_id
                id_2 = self.area_id + 1
                id_3 = self.area_id + self.gridlon__length - 1
                id_4 = self.area_id + self.gridlon__length
                id_5 = self.area_id + self.gridlon__length + 1
                self.need_ID = [id_1, id_2, id_3, id_4, id_5]
            elif self.Leftlat_ == max(self.gridlat_):
                id_1 = self.area_id
                id_2 = self.area_id + 1
                self.need_ID = [id_1, id_2]
            elif self.Leftlon_ == min(self.gridlon_):
                id_1 = self.area_id
                id_2 = self.area_id + 1
                id_3 = self.area_id + self.gridlon__length
                id_4 = self.area_id + self.gridlon__length + 1
                self.need_ID = [id_1, id_2, id_3, id_4]
            elif self.Leftlon_ == max(self.gridlon_):
                id_1 = self.area_id
                id_2 = self.area_id + self.gridlon__length - 1
                id_3 = self.area_id + self.gridlon__length
                self.need_ID = [id_1, id_2, id_3]
        elif self.flag == 1:  # 网格4个角落, flag=1
            if self.Leftlon_ == min(self.gridlon_) and self.Leftlat_ == min(self.gridlat_):
                id_1 = self.area_id
                id_2 = self.area_id + 1
                id_3 = self.area_id + self.gridlon__length
                id_4 = self.area_id + self.gridlon__length + 1
                self.need_ID = [id_1, id_2, id_3, id_4]
            elif self.Leftlon_ == max(self.gridlon_) and self.Leftlat_ == min(self.gridlat_):
                id_1 = self.area_id
                id_2 = self.area_id + self.gridlon__length - 1
                id_3 = self.area_id + self.gridlon__length
                self.need_ID = [id_1, id_2, id_3]
            elif self.Leftlon_ == min(self.gridlon_) and self.Leftlat_ == max(self.gridlat_):
                id_1 = self.area_id
                id_2 = self.area_id + 1
                self.need_ID = [id_1, id_2]
            elif self.Leftlon_ == max(self.gridlon_) and self.Leftlat_ == max(self.gridlat_):
                id_1 = self.area_id
                self.need_ID = [id_1]
        return self.need_ID