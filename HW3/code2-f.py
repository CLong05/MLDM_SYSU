import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import random
import copy


def getData(filename):
    """读取数据    """
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


def f_gradientDecent(trainSet, learning_rate=0.00015, iteration_time=150):
    '''对第 f 问的专用函数    '''
    theta = np.zeros(7)

    testSet = getData('./data/dataForTestingLogistic.txt')  # 测试集
    testSetSize = len(testSet)  # 测试集大小
    trainSetSize = len(trainSet)

    for iterTime in range(iteration_time):
        sum = np.zeros(7)
        # 遍历训练集
        for trainSetIndex in range(trainSetSize):
            h_x = theta[0]
            for i in range(1, 7):
                h_x += theta[i] * trainSet[trainSetIndex][i - 1]

            sum[0] += trainSet[trainSetIndex][6] - sigmod(h_x)
            for i in range(1, 7):
                sum[i] += (trainSet[trainSetIndex][6] - sigmod(h_x)
                           ) * trainSet[trainSetIndex][i - 1]

        # 更新参数
        for i in range(7):
            theta[i] += (learning_rate * sum[i])

    tmp = 0
    test_tmp = 0

    # 计算训练误差
    for trainSetIndex in range(trainSetSize):
        H_x = theta[0]
        for i in range(1, 7):
            H_x += theta[i] * trainSet[trainSetIndex][i - 1]
        if np.abs(sigmod(H_x) - trainSet[trainSetIndex][6]) < np.longdouble(0.5):
            tmp += 1

    trainError = 1 - (1.0 / trainSetSize) * tmp

    # 计算测试误差
    for testSetIndex in range(testSetSize):
        H_x = theta[0]
        for i in range(1, 7):
            H_x += theta[i] * testSet[testSetIndex][i - 1]
        if np.abs(sigmod(H_x) - testSet[testSetIndex][6]) < np.longdouble(0.5):
            test_tmp += 1
    testError = 1 - (1.0 / testSetSize) * test_tmp

    return trainError, testError, theta


def f():
    """
    对第 f 问的专用函数
    """
    trainSet = getData('./data/dataForTrainingLogistic.txt')  # 训练集

    resTable = PrettyTable(["set", "theta_0", "theta_1",
                            "theta_2", "theta_3", "theta_4", "theta_5", "theta_6",
                            "train_error_rate", "test_error_rate"])  # 用于美观显示
    trainingErrors = []  # 训练误差
    testingErrors = []  # 测试误差
    training_set_size = []

    for i in range(40):
        print('训练集数量：', (i + 1) * 10)

        trainSetCopy = copy.deepcopy(trainSet)
        subSet = []

        # 获取对应的训练子集
        for _ in range((i + 1) * 10):
            index = random.randint(0, len(trainSetCopy) - 1)
            subSet.append(trainSetCopy[index])
            np.delete(trainSetCopy, index)

        # 使用子集训练模型
        trainData, testData, theta = f_gradientDecent(trainSet=subSet)
        resTable.add_row([(i + 1) * 10, format(theta[0], '.4f'), format(theta[1], '.4f'), format(theta[2], '.4f'), format(
            theta[3], '.4f'), format(theta[4], '.4f'), format(theta[5], '.4f'), format(theta[6], '.4f'), trainData, testData])

        training_set_size.append((i + 1) * 10)
        trainingErrors.append(trainData)
        testingErrors.append(testData)

    return training_set_size, trainingErrors, testingErrors, resTable


# 题目f
(training_set_size, trainingData, testingData, resTable) = f()

print(resTable)

# 画图
plt.figure()
plt.plot(training_set_size, trainingData, "o-",
         c="b", linewidth=1, label="training error")
plt.plot(training_set_size, testingData, "o-",
         c="r", linewidth=1, label="testing error")

plt.xlabel("Training Set Size")
plt.ylabel("Error")
plt.legend()
plt.title("Logistic Regression")
plt.grid()
plt.show()
