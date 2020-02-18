#!/usr/bin/env python
# -*-coding:utf-8-*-

from collections import OrderedDict
from hashlib import md5
from urllib.parse import urlencode
from uuid import uuid1


def str_md5(key):
    return md5(key.encode()).hexdigest()


def random_md5(limit=None):
    """
    输出基于uuid1产生的md5标识
    limit 截取最前面的几个
    """
    key = str(uuid1())
    text = str_md5(key)
    if limit:
        assert isinstance(limit, int)
        assert limit > 0
        return text[:limit]
    else:
        return text


def build_unique_key(base_key, *args, **kwargs):
    """
    缓存唯一id标识生成函数

    :param base_key: 基本的区分key值 比如函数名
    :param args: 必填参数
    :param kwargs: 其他参数
    :return:
    """
    args_id = ""
    kwargs_id = ""

    if args:
        args_id = '_'.join(args)

    if kwargs:
        kwargs = OrderedDict(sorted(kwargs.items(), key=lambda t: t[0]))
        kwargs_id = urlencode(kwargs)

    key = '_'.join([i for i in [base_key, args_id, kwargs_id] if i])

    key = md5(key.encode()).hexdigest()
    return key
