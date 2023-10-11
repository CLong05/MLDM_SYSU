import cmath
import random
import math
import numpy as np
import prettytable as pt

loopTime = 100
dotNumsList = [10, 20, 30, 40, 50, 60, 70, 80, 100, 200, 500]


def get_one_dot():
    """ 随机获取一个点，并计算该点的函数值 """
    x = random.random() * 2 + 2 #x
    y = random.random() * 2 - 1
    return (math.pow(y, 2) * cmath.exp(-math.pow(y, 2)) +
            math.pow(x, 4) * cmath.exp(-math.pow(x, 2))) /\
           (x * math.pow(cmath.e, -math.pow(x, 2)))



def get_a_map(dot_nums):
    """ 蒙特卡洛方法计算出的积分值 """
    sum = 0
    for _ in range(dot_nums):
        sum += get_one_dot()
    return sum * 4 / dot_nums


tb = pt.PrettyTable()
tb.field_names=(["投点个数", "均值", "方差"])

for dotnums in dotNumsList:
    res = []
    for i in range(loopTime):
        """不能直接用int进行迭代，而必须加个range."""
        res.append(get_a_map(dotnums))
    tb.add_row([dotnums, np.mean(res).real, np.var(res)])
print(tb)