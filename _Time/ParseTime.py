#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/14
from datetime import datetime


def parse_time(string):
    """
     Function: "%Y-%m-%d %H:%M:%S" convert to datetime(year, month, day, hour, minute, second)
    """
    year, month, day = string[:10].split('-')
    hour, minute, second = string[11:].split(':')
    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

