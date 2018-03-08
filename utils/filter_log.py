#!/usr/bin/env python
# Author: 'JiaChen'

import os
import time


def post_file(abs_path, ret_list=None):
    if ret_list is None:
        ret_list = []
    file_list = [os.path.join(abs_path, item) for item in os.listdir(abs_path)]
    for item in file_list:
        if os.path.isfile(item):
            ret_list.append(item)
        elif os.path.isdir(item):
            post_file(item, ret_list)
    return ret_list


def cut_file_list(application_path, ret_list):
    result = []
    for item in ret_list:
        temp = {}
        file_name = item.split(application_path, 1)[-1].lstrip('\\').lstrip('/')
        temp['file_name'] = file_name
        file_size = round(os.path.getsize(item)/(1024*1024), 2)
        temp['file_size'] = file_size
        file_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(item) + 28800))
        temp['file_time'] = file_time
        temp['file_path'] = item
        result.append(temp)
    for i in range(len(result) - 1):
        for j in range(len(result) - i - 1):
            if result[j]['file_time'] > result[j + 1]['file_time']:
                result[j], result[j + 1] = result[j + 1], result[j]
    result.reverse()
    return result
