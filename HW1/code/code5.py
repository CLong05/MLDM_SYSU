import random

loopTime = 1000
count1, count2 = 0, 0
count = 0


def get_one_test():
    """ 随机获取3个点，对应A、B、C
        并计算最终是否成功，分别记录在count1、count2中 """
    a = random.random()
    b = random.random()
    c = random.random()
    """全局变量，用于计算成功次数"""
    global count1, count2, count #！！！
    flag = False
    if a <= 0.85:
        count1 += 1
        flag = True
    if b <= 0.95 and c <= 0.9:
        count2 += 1
        flag = True
    if flag:
        count += 1


for _ in range(loopTime):
    get_one_test()
print(f"上半部分成功次数：{count1};下半部分成功次数：{count2};总成功次数：{count}")
print(f"上半部分成功概率：{format(count1 / loopTime, '.4f')};"
      f"下半部分成功概率：{format(count2 / loopTime, '.4f')};"
      f"总成功概率：{format(count / loopTime, '.4f')}")
