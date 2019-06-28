#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/13
import json
import numpy as np
import pandas as pd
import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io import img_tiles
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

#-------------------------------------------
# 输入参数:
#   (1)FinalDataSet.csv的路径:
#   (2)
#-------------------------------------------

# 读取经纬度
path = './DataProcess/Final_Data_Result/finall_data-10-01.csv'
# 航道geojson
path_geojson = './DataProcess/channel_geojson/map.geojson'

# 读取finall_data-10-01.csv
df = pd.read_csv(path)

# 读取航道信息, 写成Polygon
with open(path_geojson) as f:
    data = json.load(f)

PolygonLen = len(data['features'])
longitude = df.mid_lon.values
latitude = df.mid_lat.values
points = np.column_stack((longitude, latitude))

for index in range(PolygonLen):
    polygon = data['features'][index]['geometry']['coordinates'][0]
    path = mplPath.Path(polygon)
    selector = path.contains_points(points)
    points = np.delete(points, np.where(selector), axis=0)

lon1, lat1 = points[:, 0], points[:, 1]

request = img_tiles.TDT()
fig = plt.figure(figsize=(10, 10), dpi=100)
ax = plt.axes(projection=request.crs)
ax.set_extent([120, 126, 30, 36], crs=ccrs.PlateCarree())

# 经纬度grid
gl = ax.gridlines(color='black', linestyle='--', draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

ax.add_image(request, 8)

ax.scatter(lon1, lat1, transform=ccrs.PlateCarree(), s=.03, color='red')
plt.savefig("./RiskOfCollisionPicture/2016-10-01/Distribution_of_collision_risk_in_Yangtze_river_estuary(2016-10-01).png", bbox_inches='tight')
plt.show()