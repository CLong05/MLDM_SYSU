from numpy import *

dataSet = [[5.9, 3.2], [4.6, 2.9], [6.2, 2.8], [4.7, 3.2], [5.5, 4.2],
           [5.0, 3.0], [4.9, 3.1], [6.7, 3.1], [5.1, 3.8], [6.0, 3.0]]
clusters = [
    {"color": "red", "x": 6.2, "y": 3.2, "kind": 0, "num": 0},
    {"color": "green", "x": 6.6, "y": 3.7, "kind": 1, "num": 0},
    {"color": "blue", "x": 6.5, "y": 3.0, "kind": 2, "num": 0},
]


# calculate Euclidean distance
def euclDistance(x1, y1, x2, y2):
    return sqrt(power(x1 - x2, 2) + power(y1 - y2, 2))



## step 1: init centroids
numSamples = 10
# first column stores which cluster this sample belongs to,
# second column stores the error between this sample and its centroid
clusterAssment = [[-1] * 2 for _ in range(numSamples)]
for i in range(numSamples):
    clusterAssment[i][0] = -1
clusterChanged = True
k = len(clusters)

count = 0
while clusterChanged and count < 10:
    count += 1
    print(f"\n第{count}次迭代：")
    clusterChanged = False
    ## for each sample
    for i in range(numSamples):
        minDist = 100000.0
        minIndex = -1
        ## for each centroid
        ## step 2: find the centroid who is closest
        for j in range(k):
            distance = euclDistance(dataSet[i][0], dataSet[i][1],
                                    clusters[j]["x"], clusters[j]["y"])
            if distance < minDist:
                minDist = distance
                minIndex = j

        ## step 3: update its cluster
        if clusterAssment[i][0] != minIndex:
            if clusterAssment[i][0] != -1:
                clusters[clusterAssment[i][0]]["num"] -= 1
            clusterChanged = True
            clusterAssment[i][0], clusterAssment[i][1] = minIndex, minDist ** 2
            clusters[minIndex]["num"] += 1

    ## step 4: update centroids
    newx = [0, 0, 0]
    newy = [0, 0, 0]
    for i in range(numSamples):
        belong_kind = clusterAssment[i][0]
        newx[belong_kind] += dataSet[i][0]
        newy[belong_kind] += dataSet[i][1]
    for j in range(k):
        clusters[j]["x"] = newx[j] / clusters[j]["num"]
        clusters[j]["y"] = newy[j] / clusters[j]["num"]
        print(f"color:{clusters[j]['color']},x:{clusters[j]['x']},"
              f"y:{clusters[j]['y']}")
