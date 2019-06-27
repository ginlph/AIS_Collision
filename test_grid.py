#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/11
import fiona
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import shapely.geometry as sgeom
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

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

plt.show()