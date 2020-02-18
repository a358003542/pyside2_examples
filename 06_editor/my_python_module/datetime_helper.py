#!/usr/bin/env python
# -*-coding:utf-8-*-

import time
from datetime import datetime


def is_same_year(dt1, dt2):
    """
    判断两个datetime 对象是否是同一年
    :param dt1:
    :param dt2:
    :return:
    """
    if (dt1.year == dt2.year):
        return True
    else:
        return False


def is_same_month(dt1, dt2):
    """
    判断两个datetime对象是否是同一月
    :param dt1:
    :param dt2:
    :return:
    """
    if (dt1.year == dt2.year) and (dt1.month == dt2.month):
        return True
    else:
        return False


def is_same_day(dt1, dt2):
    """
    判断两个datetime对象是否是同一天
    :param dt1:
    :param dt2:
    :return:
    """
    if (dt1.year == dt2.year) and (dt1.month == dt2.month) and (
            dt1.day == dt2.day):
        return True
    else:
        return False


def is_same_hour(dt1, dt2):
    """
    判断两个datetime对象是否是同一时
    :param dt1:
    :param dt2:
    :return:
    """
    if (dt1.year == dt2.year) and (dt1.month == dt2.month) and (
            dt1.day == dt2.day) and (dt1.hour == dt2.hour):
        return True
    else:
        return False


def round_to_day(dt):
    """
    datetime对象round到天，更小的刻度归零
    :param dt:
    :return:
    """
    res = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return res


def round_to_hour(dt):
    """
    datetime对象round到小时，更小的刻度归零
    :param dt:
    :return:
    """
    res = dt.replace(minute=0, second=0, microsecond=0)
    return res


def round_to_minute(dt):
    """
    datetime对象round到分钟
    :param dt:
    :return:
    """
    res = dt.replace(second=0, microsecond=0)
    return res


def round_to_second(dt):
    """
    datetime对象round到秒
    :param dt:
    :return:
    """
    res = dt.replace(microsecond=0)
    return res


def normal_format_now():
    """
    标准格式 now

    '2018-12-21 15:39:20'
    :return:
    """
    return datetime.now().__format__('%Y-%m-%d %H:%M:%S')


def normal_format_utcnow():
    """
    标准格式 utcnow 服务器那边记录时间应该都是 utcnow

    '2018-12-21 15:39:20'
    :return:
    """
    return datetime.utcnow().__format__('%Y-%m-%d %H:%M:%S')


def get_timestamp(multiplier=1):
    """
    获得当前的timestamp
    :return:
    """
    timestamp = time.time()

    timestamp = timestamp * multiplier

    return int(timestamp)


def dt_to_timestamp(dt, multiplier=1):
    timestamp = dt.timestamp()

    timestamp = timestamp * multiplier

    return int(timestamp)


def get_dt_fromtimestamp(timestamp, utc=True, multiplier=1):
    """
    根据timestamp获得对应的datetime对象
    """

    if isinstance(timestamp, str):
        timestamp = float(timestamp)

    timestamp = timestamp * multiplier

    if utc:
        dt = datetime.utcfromtimestamp(timestamp)
    else:
        dt = datetime.fromtimestamp(timestamp)

    return dt
