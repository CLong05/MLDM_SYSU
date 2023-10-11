import random
import math
import numpy as np
import prettytable as pt

loopTime = 100
dotNumsList = [5, 10, 20, 30, 40, 50, 60, 70, 80, 100]


def get_one_dot() -> bool:
    """ 随机获取一个点，并判断是否在 积分区域上
        如果在，返回 true，否则返回 false"""
    x = random.random()
    y = random.random()
    return math.pow(x, 3) > y



def get_a_map(dot_nums) -> float:
    """ 蒙特卡洛方法计算出的积分值 """
    circle = 0
    for _ in range(dot_nums):
        if get_one_dot():
            circle += 1
    return circle / dot_nums


tb = pt.PrettyTable()
tb.field_names=(["投点个数", "均值", "方差"])

for dotnums in dotNumsList:
    res = []
    for i in range(loopTime):
        """不能直接用int进行迭代，而必须加个range."""
        res.append(get_a_map(dotnums))
    tb.add_row([dotnums, np.mean(res), np.var(res)])
print(tb)