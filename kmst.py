from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import numpy as np
from sklearn.neighbors import NearestNeighbors
import codecs

import matplotlib.pyplot as plt

def getLeafsCount(arr):
    a = np.array(arr)
    count_non_zero_cols = np.count_nonzero(a, axis=0)
    count_non_zero_rows = np.count_nonzero(a, axis=1)
    r = []
    for i in range(len(count_non_zero_cols)):
        if (count_non_zero_cols[i] + count_non_zero_rows[i] == 1):
            r.append(i)
    return len(r)

def showResult(data, raw_data, best_indexes):
    for index, point in enumerate(data):
        plt.plot(point[0], point[1], 'bo', markersize=10)
        plt.text(point[0]-0.5, point[1]-0.5, index +2 , fontsize=8)

    for i in range(0, len(best_indexes)):
            plt.plot(raw_data[int(best_indexes[i])][0], raw_data[int(best_indexes[i])][1], 'ro')
            plt.text(raw_data[int(best_indexes[i])][0], raw_data[int(best_indexes[i])][1], "(%d %d) %d" % (raw_data[int(best_indexes[i])][0], raw_data[int(best_indexes[i])][1], best_indexes[i] + 2), fontsize=12)

    for i in range(len(best_result)):
        for j in range(len(best_result)):
            if (best_result[i][j] != 0):
                plt.plot([raw_data[int(best_indexes[j])][0],raw_data[int(best_indexes[i])][0]], [raw_data[int(best_indexes[j])][1], raw_data[int(best_indexes[i])][1]])
    plt.grid()
    plt.show()

file1 = open("Taxicab_64.txt", "r")
raw_data = []
t = 0
X = []
Y = []
while True:
    line = file1.readline()
    if not line:
        break
    if t != 0:
        a = line.strip().split('\t')
        X.append(int(a[0]))
        Y.append(int(a[1]))
        raw_data.append([int(a[0]), int(a[1])])
    else: n = int(line.split('=')[1])
    t = t + 1
X = np.array(X)
Y = np.array(Y)

data = np.array(raw_data)

knn = NearestNeighbors(algorithm='auto', n_neighbors=(int(n/8)), p=1,radius=1.0).fit(data)
distances, indexes = knn.kneighbors(data)

best_result = []
best_leafs = 99999
best_c = 99999
for iteration in range(0, len(distances)):
    matrix = []
    for i in range(0, len(indexes[iteration])):
        row = []
        for j in range(0, len(indexes[iteration])):
            if (i < j):
                row.append(abs(int(data[indexes[iteration][i]][0]) - int(data[indexes[iteration][j]][0])) + abs(int(data[indexes[iteration][i]][1]) - int(data[indexes[iteration][j]][1])))
            else: row.append(0)
        matrix.append(row)
    X = csr_matrix(matrix)

    Tcsr = minimum_spanning_tree(X)
    result_matrix = Tcsr.toarray().astype(int)
    
    c = 0 
    for i in range(len(result_matrix)):
        for j in range(len(result_matrix)):
            c = c + result_matrix[i][j]
    if ((c < best_c) | ((c == best_c) & (getLeafsCount(result_matrix) < best_leafs))):
        best_result = result_matrix
        best_leafs = getLeafsCount(result_matrix)
        best_c = c
        best_indexes = indexes[iteration]


writefile = codecs.open("1/Chernyshova%d.txt" % n, 'w', 'utf-8')
writefile.write("c Вес дерева = %d, число листьев = %d\n" % (best_c, best_leafs))
writefile.write("p edge %d %d\n" % (n, len(best_indexes)-1))
for i in range(len(best_result)):
    for j in range(len(best_result)):
        if (best_result[i][j] != 0):
            writefile.write("e %d %d\n" % (best_indexes[i] + 2, best_indexes[j] + 2))
writefile.close()

showResult(data, raw_data, best_indexes)