#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/6/17
import csv
import numpy as np
from datetime import timedelta
from operator import itemgetter
from itertools import chain, groupby
from multiprocessing import Pool

from _Time.ParseTime import parse_time
from DataProcess.SourceData import source_data
from DataProcess.FinalData import calculation

#************************************************************
#           data_process.py(待添加功能)
# ——Meta_Data Directory: 2016年10月至12月AIS元数据(.csv)
# ——Final_Data_Result: data_process.py处理后的结果(.csv)
# ——SourceData.py
# ——FinalData.py
#
# Global Variable:
#       (1) longitude、latitude、delta
#       (2) start、end、step
#
# 进程池Pool:
#       MacBook Pro2017: 8核心
#       Dell T7610: 12核心
#
# 待添加功能:
#       将长江口定线制中北槽航道、南槽航道的经纬度写成GeoJson,
#      然后剔除在此GeoJson文件中船舶, 生成最终的final_data.csv,
#      写入Final_Data_Result目录中
#
#************************************************************

# 元数据路径
path = './Meta_Data/2016-10-01.csv'

##网格范围

# 研究区域经度范围
longitude = np.arange(120, 126, 0.5)
# 研究区域纬度范围
latitude = np.arange(30, 36, 0.5)
# 研究区域网格粒度
delta = 0.5

## 时间范围

# 起始时间
start = parse_time("2016-10-01 00:00:00")
# 终止时间
end = parse_time("2016-10-02 00:00:05")
# 时间步长step
step = timedelta(seconds=5)

if __name__ == '__main__':
    import time
    start_time = time.time()
    with Pool() as pool:
        datas = list(chain(*pool.map(calculation, source_data(
            path, longitude=longitude, latitude=latitude, delta=delta, start=start, end=end, step=step
        ))))
        datas.sort(key=itemgetter('Tar_Ship', 'Ref_Ship'))
        print("")
        print("Process has finished!!!")
        print("The Length of datas %s" % len(datas))
        data = [min(items, key=itemgetter('distance')) for tar, items in
                groupby(datas, key=itemgetter('Tar_Ship', 'Ref_Ship'))]
        print(len(data))
        with open("./Final_Data_Result/10-01.csv", 'w') as f:
            _data = csv.DictWriter(f, ['Tar_Ship', 'Ref_Ship', 'mid_lon', 'mid_lat', 'distance', 'DCPA', 'TCPA'])
            _data.writeheader()
            _data.writerows(data)
    end_time = time.time()
    print("Time Cost: {:.3f}s".format(end_time - start_time))