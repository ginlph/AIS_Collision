#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/13
import fiona
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import img_tiles
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import  shapely.geometry as sgeom

#-------------------------------------------
# 输入参数:
#   (1)FinalDataSet.csv的路径:
#   (2)
#-------------------------------------------

# 读取经纬度
path = 'final_data.csv'
data = pd.read_csv(path)

# request = img_tiles.TDT()
# fig = plt.figure(figsize=(10, 10), dpi=300)
# ax = plt.axes(projection=request.crs)
# ax.set_extent([120.6, 121.8, 30.8, 31.5], crs=ccrs.PlateCarree())
#
# # 经纬度grid
# gl = ax.gridlines(color='black', linestyle='--', draw_labels=True)
# gl.xlabels_top = False
# gl.ylabels_right = False
# gl.xformatter = LONGITUDE_FORMATTER
# gl.yformatter = LATITUDE_FORMATTER
#
# ax.add_image(request, 16)
# ax.scatter(data['mid_lon'], data['mid_lat'], transform=ccrs.PlateCarree(), c='#E8175D', s=.03)
# plt.show()
map_url = '/Volumes/My Passport/shp_file/chinamap/cnmap/cnhimap.shp'
fig = plt.figure(figsize=(15, 9))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([115, 130, 25, 40], crs=ccrs.PlateCarree())


# ax.coastlines('10m')
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle=':')
ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
with fiona.open(map_url) as f:
    geometries = [sgeom.shape(shp['geometry']) for shp in f]
    ax.add_geometries(geometries, ccrs.PlateCarree(), facecolor='none', edgecolor='black')

gl = ax.gridlines(color='black', linestyle='--', draw_labels=True)
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabels_top = False
gl.ylabels_right = False

land = cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor=cfeature.COLORS['land'])
ax.add_feature(land)
ocean = cfeature.NaturalEarthFeature('physical', 'ocean', '50m', edgecolor='face', facecolor=cfeature.COLORS['water'])
#
ax.add_feature(ocean)
ax.scatter(data['mid_lon'], data['mid_lat'], s=5, color='r', transform=ccrs.PlateCarree(), zorder=3)
plt.show()
