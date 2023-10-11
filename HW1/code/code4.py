import random

loop_time = 20000
ant_map = [[1 for i in range(7)] for j in range(7)]  # 定义2维数组
# [[1]*7]*7 ant_map[3][3]+=1 所有的第三个均会+1
ant_map[3][3] += 1
count = 0


def ant_move(x, y):
    """蚂蚁从当前点（x，y）开始，每次随机移动一步
    若移动成功则修改地图信息并返回True，
    若到达边界则移动失败返回False"""
    global ant_map
    ant_map[x][y] -= 1  # 修改地图信息

    '''选择方向'''
    direc_list = []
    if x - 1 >= 0 and ant_map[x - 1][y]:
        direc_list.append(1)  # left
    if x + 1 <= 6 and ant_map[x + 1][y]:
        direc_list.append(2)  # right
    if y - 1 >= 0 and ant_map[x][y - 1]:
        direc_list.append(3)  # up
    if y + 1 <= 6 and ant_map[x][y + 1]:
        direc_list.append(4)  # down
    # print(direc_list)

    '''无法继续移动'''
    if len(direc_list) == 0:
        return False

    '''可以继续移动'''
    pdirec = random.random()
    direc = 0
    for i in range(len(direc_list)):
        if pdirec < (i + 1) / len(direc_list):
            direc = direc_list[i]
            break
    # print(direc)
    if direc == 1:
        x -= 1
    if direc == 2:
        x += 1
    if direc == 3:
        y -= 1
    if direc == 4:
        y += 1

    if x == 6 and y == 6:
        return True
    else:
        # for i in range(7):
        #     print(ant_map[i])
        # print("-------------------------------------")
        return ant_move(x, y)


for _ in range(loop_time):
    """蚂蚁走一次地图"""
    ant_map = [[1 for i in range(7)] for j in range(7)]  # 定义2维数组
    ant_map[3][3] += 1
    if ant_move(0, 0):
        count += 1
    # for i in range(7):
    #     print(ant_map[i])
print(f"P:{count / loop_time}")
