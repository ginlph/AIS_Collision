#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/8


def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step

