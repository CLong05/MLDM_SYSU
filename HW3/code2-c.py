import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import random
import math
import copy


def getData(filename):
    """读取数据
    Args:
      filename 文件名（包含路径）
    Returns:
      data
    """
    np.set_printoptions(suppress=True)

    file = open(filename)
    lines = file.readlines()
    lineNum = len(lines)

    data = np.zeros((lineNum, 7), dtype=np.longdouble)
    index = 0

    for line in lines:
        line = line.strip()
        lineData = line.split(' ')
        data[index, :] = lineData[0: 7]
        index += 1

    return data


def sigmod(z):
    """逻辑函数
    Args:
        z
    Returns:
        1/(1 + e^{-z})
    """
    return ((np.longdouble(1.0) / (np.longdouble(1.0) + np.exp(-z))))


def gradientDecent(learning_rate=0.00015, theta=np.zeros(7), iteration_time=1500000, show_margin=100000,
                   random_points=0, error_or_lcl=1):
    """
    梯度下降训练线性模型

    Args:
        learning_rate: 学习率
        iteration_time: 迭代次数
        show_margin: 数据展示的迭代次数间隔
        theta: 7个参数
        error_or_lcl: 选择显示误差(1)还是 lcl(0)

    Returns:
        iterationTimes: 迭代次数数组
        trainingErrors: 训练误差
        testingErrors: 测试误差
        resTable: 结果表
    """
    # 获取数据
    # print(theta)
    trainSet = getData('./data/dataForTrainingLogistic.txt')  # 训练集
    testSet = getData('./data/dataForTestingLogistic.txt')  # 测试集
    trainSetSize = len(trainSet)  # 训练集大小
    testSetSize = len(testSet)  # 测试集大小

    resTable = PrettyTable(["iteration_times", "theta_0", "theta_1",
                            "theta_2", "theta_3", "theta_4", "theta_5", "theta_6",
                            "train_error_rate" if error_or_lcl == 1 else "train_LCL",
                            "test_error_rate" if error_or_lcl == 1 else "test_LCL"])  # 用于美观显示
    trainingErrors = []  # 训练误差
    trainingLCL = []  # 训练 LCL

    testingErrors = []  # 测试误差
    testingLCL = []  # 测试 LCL

    iterationTimes = []  # 迭代次数

    for iterTime in range(1, iteration_time + 1):
        sum = np.zeros(7)

        if random_points == 0 or random_points >= trainSetSize:
            # 一次循环
            for trainSetIndex in range(trainSetSize):
                h_x = theta[0]
                for i in range(1, 7):
                    h_x += theta[i] * trainSet[trainSetIndex][i - 1]

                sum[0] += trainSet[trainSetIndex][6] - sigmod(h_x)
                for i in range(1, 7):
                    sum[i] += (trainSet[trainSetIndex][6] - sigmod(h_x)) * \
                              trainSet[trainSetIndex][i - 1]
        else:
            for _ in range(random_points):
                index = random.randint(0, trainSetSize - 1)
                h_x = theta[0]
                for i in range(1, 7):
                    h_x += theta[i] * trainSet[index][i - 1]

                sum[0] += trainSet[index][6] - sigmod(h_x)
                for i in range(1, 7):
                    sum[i] += (trainSet[index][6] - sigmod(h_x)) * \
                              trainSet[index][i - 1]

        # 更新参数
        for i in range(7):
            theta[i] += learning_rate * sum[i]

        if iterTime % show_margin == 0:
            iterationTimes.append(iterTime)
            print("迭代次数：", iterTime)

            tmp = np.longdouble(0)
            LCL = np.longdouble(0)

            test_tmp = np.longdouble(0)
            test_LCL = np.longdouble(0)

            # 训练集误差
            for trainSetIndex in range(trainSetSize):
                H_x = theta[0]
                for i in range(1, 7):
                    H_x += theta[i] * trainSet[trainSetIndex][i - 1]
                LCL += trainSet[trainSetIndex][6] * np.log(sigmod(H_x)) + (
                        1 - trainSet[trainSetIndex][6]) * np.log(1 - sigmod(H_x))
                # print(LCL)
                if np.abs(sigmod(H_x) - trainSet[trainSetIndex][6]) < np.longdouble(0.5):
                    tmp += 1

            trainError = 1 - (1.0 / trainSetSize) * tmp
            trainingErrors.append(trainError)
            trainingLCL.append(LCL)

            # 测试集误差
            for testSetIndex in range(testSetSize):
                H_x = theta[0]
                for i in range(1, 7):
                    H_x += theta[i] * testSet[testSetIndex][i - 1]
                test_LCL += testSet[testSetIndex][6] * np.log(sigmod(H_x)) + (
                        1 - testSet[testSetIndex][6]) * np.log(1 - sigmod(H_x))
                if np.abs(sigmod(H_x) - testSet[testSetIndex][6]) < np.longdouble(0.5):
                    test_tmp += 1

            testError = 1 - (1.0 / testSetSize) * test_tmp
            testingErrors.append(testError)
            testingLCL.append(test_LCL)

            resTable.add_row(
                [iterTime, format(theta[0], '.4f'), format(theta[1], '.4f'), format(theta[2], '.4f'), format(
                    theta[3], '.4f'), format(theta[4], '.4f'), format(theta[5], '.4f'), format(theta[6], '.4f'),
                 trainError if error_or_lcl == 1 else LCL, testError if error_or_lcl == 1 else test_LCL])
            # print(iterTime, format(theta[0], '.4f'), format(theta[1], '.4f'), format(theta[2], '.4f'), format(
            #     theta[3], '.4f'), format(theta[4], '.4f'), format(theta[5], '.4f'), format(theta[6], '.4f'), LCL, test_LCL)

    return (iterationTimes, trainingErrors if error_or_lcl == 1 else trainingLCL,
            testingErrors if error_or_lcl == 1 else testingLCL, resTable)


# 题目c
(iterationTimes, trainingData, testingData,
 resTable) = gradientDecent(learning_rate=0.0015, iteration_time=30,
                            show_margin=1, random_points=0)

# 画图
plt.figure()
plt.plot(iterationTimes, trainingData, "o-",
         c="r", linewidth=1, label="training error")
plt.plot(iterationTimes, testingData, "o-",
         c="g", linewidth=1, label="testing error")

plt.xlabel("Iteration Times")
plt.ylabel("Error")
plt.legend()
plt.title("Gradient Descent")
plt.grid()
plt.show()
