#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/5
from datetime import datetime
from datetime import date
import json
"""
    json处理datetime时, 抛出TypeError:
        TypeError: Object of type 'datetime' is not JSON serializable
    
    解决方式:
        重写json.JSONEncoder子类
        ComplexEncoder
"""


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
