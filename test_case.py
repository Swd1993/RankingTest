#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime:2020/3/2 18:28
import json

import urllib3
import random


def add(client_id, score):
    """
    上传分数
    @param client_id: 客户端ID
    @param score: 分数
    @return:
    """
    http = urllib3.PoolManager()
    response = http.request(
        method="post",
        url="http://127.0.0.1:8000/upload/",
        body=json.dumps({"client_id": client_id, "score": score}),
    )
    return json.loads(response.data.decode())


def get(client_id, start, end):
    """
    获取排名段
    @param client_id: 客户端ID
    @param start: 开始排名
    @param end: 结束排名
    @return:
    """
    http = urllib3.PoolManager()
    response = http.request(
        method="get",
        url="http://127.0.0.1:8000/query/{}/{}/{}/".format(client_id, start, end)
    )
    return json.loads(response.data.decode())


def version_comparison(version_1, version_2):
    """
    比较版本
    @param version_1: 版本1
    @param version_2: 版本2
    @return:
    """

    list_1 = [int(i) for i in version_1.split(".")]
    list_2 = [int(i) for i in version_2.split(".")]
    if len(list_1) > len(list_2):
        for i in range(len(list_1) - len(list_2)):
            list_2.append(0)
    elif len(list_1) < len(list_2):
        for i in range(len(list_2) - len(list_1)):
            list_1.append(0)
    else:
        pass

    version1 = ""
    for i in list_1:
        version1 += str(i)

    version2 = ""
    for i in list_2:
        version2 += str(i)

    if int(version1) - int(version2) > 0:
        return 1
    elif int(version1) - int(version2) < 0:
        return -1
    else:
        return 0


if __name__ == "__main__":

    # 添加成员分数
    for i in range(1, 11):
        print((add(client_id=i, score=random.randint(1, 10000000))))

    # 查询
    print(get(5, 1, 10))

    # 比对版本
    print(version_comparison(version_1="0.1", version_2="1.1"))
    print(version_comparison(version_1="1.0.1", version_2="1"))
    print(version_comparison(version_1="7.5.2.4", version_2="7.5.3"))
    print(version_comparison(version_1="1.01", version_2="1.001"))
    print(version_comparison(version_1="1.0", version_2="1.0.0"))
