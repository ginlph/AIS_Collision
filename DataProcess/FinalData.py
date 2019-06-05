#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/19
import csv
import numpy as np
from DataProcess.SourceData import source_data
from CPA.DCPA_TCPA import CPA


def sort_final_data(function):
    def wrapper(*args, **kwargs):
        from operator import itemgetter
        from itertools import groupby
        results = function(*args, **kwargs)
        results.sort(key=itemgetter('Tar_Ship', 'Ref_Ship'))
        header = ['Tar_Ship', 'Ref_Ship', 'mid_lon', 'mid_lat', 'distance', 'DCPA', 'TCPA']
        results = [min(items, key=itemgetter('distance')) for tar, items in groupby(results, key=itemgetter('Tar_Ship', 'Ref_Ship'))]
        with open('final_data.csv', 'w') as f:
            datas = csv.DictWriter(f, header)
            datas.writeheader()
            datas.writerows(results)
        return
    return wrapper


@sort_final_data
def final_data(path):
    results = list()
    for grid in source_data(path):
        vessel = grid[list(grid.keys())[0]]
        length = len(vessel)
        for num in range(length):
            for _next_num in range(num+1, length):
                if vessel[_next_num].MMSI != vessel[num].MMSI:
                    if vessel[_next_num].area_ID in vessel[num].need_id():
                        try:
                            _cpa = CPA(vessel[num], vessel[_next_num])
                            DCPA, TCPA = _cpa.cpa()
                            if np.fabs(DCPA) <= 1 and 0 <= TCPA <= 0.1:
                                result = {
                                    "Tar_Ship": vessel[num].MMSI,
                                    "Ref_Ship": vessel[_next_num].MMSI,
                                    "mid_lon": _cpa.mid_point()[1],
                                    "mid_lat": _cpa.mid_point()[0],
                                    "distance": _cpa.distance(),
                                    "DCPA": DCPA,
                                    "TCPA": TCPA
                                }
                                results.append(result)
                        except Exception as e:
                            print("Reason: ", e)
    return results

#
# from operator import itemgetter
# from itertools import groupby
#
# datas = final_data("../ShipDataQuery/ChinaCoastalData/2016_10_01.csv")
# datas.sort(key=itemgetter('Tar_Ship', 'Ref_Ship'))
# for tar, items in groupby(datas, key=itemgetter('Tar_Ship', 'Ref_Ship')):
#     print(*tar)
#     # print(min(items, key=itemgetter('distance')))
#     for item in items:
#         print(item)
