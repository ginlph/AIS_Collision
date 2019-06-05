#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lph time:2019/5/13
from _Time.ParseTime import parse_time


def BinarySearch(sequence, value):
    """
    二分法BinarySearch
    [注] 序列sequence必须采用顺序存储结构，而且表中元素按关键字有序排列
    sequence: 目标序列
    value: 在序列中查找的值
    return: 查找value的索引值
    """
    begin = 0
    end = len(sequence) - 1
    while begin <= end:
        middle = (begin + end) // 2
        # middle = int(begin + (value - sequence[begin])/(sequence[end] - sequence[begin])*(end-begin))
        if list(sequence[middle].keys())[0] < value:
            begin = middle + 1
        elif list(sequence[middle].keys())[0] > value:
            end = middle - 1
        else:
            return middle

