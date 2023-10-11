import random
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable


def get_data(filename):
    """get the needed data for training or testing
    :param filename:
    :return: data in the file"""

    np.set_printoptions(suppress=True)
    file = open(filename)
    lines = file.readlines()
    line_length = len(lines)
    data = np.zeros((line_length, 3), dtype=np.longcomplex)
    index = 0
    for line in lines:
        line = line.strip()
        line_data = line.split(' ')
        data[index, :] = line_data[0: 3]
        index += 1
    return data


def gradientDecent(learning_rate=0.00015, theta_0=np.longcomplex(0.0),
                   theta_1=np.longcomplex(0.0),theta_2=np.longcomplex(0.0),
                   iteration_time=1500000, show_margin=100000, random_points = 0):
    """梯度下降训练线性模型

    Args:
        learning_rate: 学习率
        theta_0: 初始参数0
        theta_1: 初始参数1
        theta_2: 初始参数2
        iteration_time: 迭代次数
        show_margin: 数据展示的迭代次数间隔

    Returns:
        iterationTimes: 迭代次数数组
        trainingErrors: 训练误差
        testingErrors: 测试误差
        resTable: 结果表"""

    # 获取数据
    train_set = get_data('./data/dataForTrainingLinear.txt')  # 训练集
    test_set = get_data('./data/dataForTestingLinear.txt')  # 测试集
    train_set_size = len(train_set)  # 训练集大小
    test_set_size = len(test_set)  # 测试集大小

    res_table = PrettyTable(["iteration_times", "theta_0", "theta_1",
                            "theta_2", "training_error", "testing_error"])  # 表各栏名称
    training_errors = []  # 训练误差
    testing_errors = []  # 测试误差
    iteration_times = []  # 迭代次数

    for iterTime in range(1, iteration_time + 1):
        sum_0 = np.longcomplex(0)
        sum_1 = np.longcomplex(0)
        sum_2 = np.longcomplex(0)

        if random_points == 0:
            # 正常梯度下降迭代
            for trainIndex in range(train_set_size):
                # 初始化三个参数的和，用于更新 theta
                h_x = theta_0 + theta_1 * train_set[trainIndex][0] \
                      + theta_2 * train_set[trainIndex][1]  # 计算结果
                h_x = np.around(h_x, decimals=6)
                # error=h_x - train_set[trainIndex][2]
                sum_0 += h_x - train_set[trainIndex][2]
                sum_1 += (h_x - train_set[trainIndex][2]) * train_set[trainIndex][0]
                sum_2 += (h_x - train_set[trainIndex][2]) * train_set[trainIndex][1]
                sum_0 = np.longcomplex(np.around(sum_0, decimals=6))
                sum_1 = np.longcomplex(np.around(sum_1, decimals=6))
                sum_2 = np.longcomplex(np.around(sum_2, decimals=6))
        else:
            # 随机梯度下降迭代
            for _ in range(random_points):
                index = random.randint(0, train_set_size - 1)
                h_x = theta_0 + theta_1 * train_set[index][0] \
                      + theta_2 * train_set[index][1]  # 计算结果
                error = h_x - train_set[index][2]
                sum_0 += error
                sum_1 += error * train_set[index][0]
                sum_2 += error * train_set[index][1]

        # 迭代参数
        theta_0 = theta_0 - learning_rate * (sum_0 / (train_set_size if (random_points == 0) else random_points))
        theta_1 = theta_1 - learning_rate * (sum_1 / (train_set_size if (random_points == 0) else random_points))
        theta_2 = theta_2 - learning_rate * (sum_2 / (train_set_size if (random_points == 0) else random_points))

        # 每间隔 show_margin 次进行一次结果展示
        if iterTime % show_margin == 0:
            iteration_times.append(iterTime + 1)
            trainVar = np.longcomplex(0.0)  # 训练集误差
            testVar = np.longcomplex(0.0)  # 测试集误差

            # 计算训练集误差
            for train_setIndex in range(train_set_size):
                H_x = np.longcomplex(theta_0 + theta_1 *
                                     train_set[train_setIndex][0] + theta_2 *
                                     train_set[train_setIndex][1])  # 计算结果
                # (y* - y_i)^2 用于计算方差
                trainVar += np.square(np.longcomplex(H_x) -
                                      np.longcomplex(train_set[train_setIndex][2]))

            trainError = np.longcomplex(trainVar * 1.0 / train_set_size)
            training_errors.append(trainError)

            # 计算测试集误差
            for testSetIndex in range(test_set_size):
                H_x = np.longcomplex(theta_0 + theta_1 *
                                     test_set[testSetIndex][0] + theta_2 *
                                     test_set[testSetIndex][1])  # 计算结果
                testVar += np.square(np.longcomplex(H_x) -
                                     np.longcomplex(test_set[testSetIndex][2]))

            testError = np.longcomplex(testVar * 1.0 / test_set_size)
            testing_errors.append(testError)

            res_table.add_row([iterTime, theta_0, np.real(theta_1),
                              np.real(theta_2), trainError, testError])

    # print(resTable)

    return (iteration_times, training_errors, testing_errors, res_table)


# 题目a
(iterationTimes, trainingErrors, testingErrors, resTable) = \
    gradientDecent( )

print(resTable)

# 画图
plt.figure()
plt.plot(iterationTimes, trainingErrors, "-o",
         c="r", linewidth=1, label="training error")
plt.plot(iterationTimes, testingErrors, "-o",
         c="g", linewidth=1, label="testing error")

plt.xlabel("Iteration Times")
plt.ylabel("Error")
plt.legend()
plt.title("Gradient Descent")
plt.grid()
plt.show()
