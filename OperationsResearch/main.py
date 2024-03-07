import copy
import sys


def arrayIsNegative(array):
    for i in array:
        if i > 0:
            return True
    return False

def checkNegativeBazis(bazis, size):
    for i in range(len(bazis[0])):
        if (bazis[0][i] > size):
            return True
    return False

a = [
    [3, 2, 1, 5, 0, -1],
    [6, 3, 5, 5, 5, -2],
    [-1, -1, 0, 0, -2, 5]
]
b = [8, 7, 4]
c = [-6, -7, -3, -6, -3, -7]
size = len(c)

bazis = []
n = []
for i in range(len(b)):
    c.append(0)
    n.append(len(c))

bazis.append(n)
bazis.append(b)

funcZ = 0
for i in range(len(bazis[0])):
    funcZ += c[bazis[0][i] - 1] * bazis[1][i]

z = []
for i in range(len(a[0])):
    deltaZ = 0
    for j in range(len(bazis[0])):
        deltaZ += c[bazis[0][j] - 1] * a[j][i]
    deltaZ -= c[i]
    z.append(deltaZ)

s = 0
r = 0
while (checkNegativeBazis(bazis, size) or arrayIsNegative(z)):

    max = -sys.maxsize
    for i in range(len(z)):
        if (z[i] > max):
            max = z[i]
            s = i

    minB = sys.maxsize
    for i in range(len(bazis[0])):
        if (a[i][s] > 0):
            mB = bazis[1][i] / a[i][s]
            if mB < minB:
                minB = mB
                r = i

    for i in range(len(bazis[0])):
        if i != r:
            bazis[1][i] = (bazis[1][i] * a[r][s] - a[i][s] * bazis[1][r]) / a[r][s]
    bazis[0][r] = s
    bazis[1][r] = a[r][s]

    newA = copy.deepcopy(a)
    for i in range(len(a)):
        for j in range(len(a[i])):
            if r == i:
                newA[i][j] = a[i][j] / a[r][s]
            else:
                a1 = a[r][s]
                a2 = a[i][j]
                a3 = a[r][j]
                a4 = a[i][s]
                ri = (a[r][s] * a[i][j] - a[r][j] * a[i][s]) / a[r][s]
                newA[i][j] = (a[r][s] * a[i][j] - a[r][j] * a[i][s]) / a[r][s]

    a = newA

    funcZ = 0
    for i in range(len(bazis[0])):
        funcZ += c[bazis[0][i] - 1] * bazis[1][i]

    z = []
    for i in range(len(a[0])):
        deltaZ = 0
        for j in range(len(bazis[0])):
            deltaZ += c[bazis[0][j] - 1] * a[j][i]
        deltaZ -= c[i]
        z.append(deltaZ)



