#!/usr/bin/env python
# -*-coding:utf-8-*-


import os
import json


def write_json(file, data):
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_json_file(json_filename):
    """
    :return:
    """
    if not os.path.exists(json_filename):
        data = {}
        write_json(json_filename, data)

    return json_filename


def get_json_data(json_filename):
    """
    获取json文件存储的值
    :return:
    """
    with open(get_json_file(json_filename), encoding='utf8') as f:
        res = json.load(f)
        return res


def get_json_value(json_filename, k):
    res = get_json_data(json_filename)
    return res.get(k)


def set_json_value(json_filename, k, v):
    """
    对json文件的某个k设置某个值v
    """
    res = get_json_data(json_filename)
    res[k] = v
    write_json(get_json_file(json_filename), res)
