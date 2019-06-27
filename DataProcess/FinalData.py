#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/6/13
import numpy as np

from CPA.DCPA_TCPA import CPA


# 计算DCPA和TCPA
def calculation(_dict):
    _vessel = _dict["SHIP_INFO"]
    length = len(_vessel)
    results = []
    for num in range(length):
        for _next_num in range(num+1, length):
            if _vessel[_next_num].MMSI != _vessel[num].MMSI:
                if _vessel[_next_num].area_id in _vessel[num].need_id():
                    try:
                        _cpa = CPA(_vessel[num], _vessel[_next_num])
                        dcpa, tcpa = _cpa.cpa()
                        if np.fabs(dcpa) <= 1 and 0 <= tcpa <= 0.1:
                            result = {
                                "Tar_Ship": _vessel[num].MMSI,
                                "Ref_Ship": _vessel[_next_num].MMSI,
                                "mid_lon": _cpa.mid_point()[1],
                                "mid_lat": _cpa.mid_point()[0],
                                "distance": _cpa.distance(),
                                "DCPA": dcpa,
                                "TCPA": tcpa
                            }
                            results.append(result)
                    except Exception as e:
                        print("Reason: ", e)
    return results