import copy
import sys


def arrayIsNegative(array, size):
    """
    Функция проверки массива на наличие отрицательных чисел
    :param array:
    массив для проверки на неотрицательность
    :return: True - массив имеет отрицательные элементы, иначе False
    """
    for i in range(size):
        if array[0][i] != 0:
            return True
        elif (array[0][i] == 0 and array[1][i] > 0):
            return True
    return False


def findOptimalVector(a, b, c):
    """
    Функция расчёта оптимального значения симплексным методом
    Подходит для расчёта моделей, которые имеют ограничения =
    :param a: Матрица коэффициентов при переменных при ограничениях
    :param b: Вектор значений ограничений
    :param c: Вектор коэффициентов переменных целевой функции
    :return: Вектор оптимальных значений при максимуме целевой функции
    """
    """
    Для удобства данные представлены как таблица

    |Базисные переменные | Базис | x(1)    | x(2)    | x(3)    ... | x(n)    |
    --------------------------------------------------------------------------
    | x (n + 1)          | b(1)  | a[1][1] | a[1][2] | a[1][3] ... | a[1][n] |
    --------------------------------------------------------------------------
    | x (n + 2)          | b(2)  | a[2][1] | a[2][2] | a[2][3] ... | a[2][n] |
    --------------------------------------------------------------------------
    ...
    --------------------------------------------------------------------------
    | x (n + m)          | b(m)  | a[m][1] | a[m][2] | a[m][3] ... | a[m][n] |
    --------------------------------------------------------------------------
    |                    |Z(f)(Q)| z[1](Q) | z[2](Q) | z[3](Q) ... | z[n](Q) |
    | Z                  -----------------------------------------------------
    |                    | Z(f)  | z[1]    | z[2]    | z[3]    ... | z[n]    |
    --------------------------------------------------------------------------

    a задаёт коэффициенты x[i][j]
    b задает коэффициенты b[i]
    c задаёт коэффициенты при целевой функции

    Для расчёта конкретных коэффициентов используется преобразование Гаусса 
    Q - некоторое большое число
    """
    # Запоминаем количество коэффициентов в изначальном целевом выражении
    size = len(c)

    # Добавляем искусственные переменные по числу ограничений
    for i in range(len(a)):
        for j in range(len(b)):
            if i == j:
                a[i].append(1)
            else:
                a[i].append(0)

    # bazis[0] - список переменных в базисе
    # bazis[1] - список значений коэффициентов при переменных в базисе
    bazis = []
    n = []
    for i in range(len(b)):
        c.append(0)
        n.append(len(c))

    bazis.append(n)
    bazis.append(b)

    # funcZ - значений целевой функции
    # funcZ [0] - коэффициент Q у значения функции
    # funcZ [0] - числовой коэффициент у значения функции
    funcZ = [0, 0]
    for i in range(len(bazis[0])):
        if (bazis[0][i] > size):
            funcZ[0] += bazis[1][i]
        else:
            funcZ[1] += c[bazis[0][i] - 1] * bazis[1][i]

    # z - вектор z
    # z [0] - коэффициент Q у значения вектора z
    # z [1] - числовой коэффициент у значения вектора z
    z = []
    z.append([])
    z.append([])
    for i in range(len(a[0])):
        deltaZ = [0, 0]
        for j in range(len(bazis[0])):
            if (bazis[0][j] > size):
                deltaZ[0] += a[j][i]
            else:
                deltaZ[1] += c[bazis[0][j] - 1] * a[j][i]
        if (i + 1 > size):
            deltaZ[0] -= 1
        else:
            deltaZ[1] -= c[i]
        z[0].append(deltaZ[0])
        z[1].append(deltaZ[1])

    # цикл пока в векторе z присутствуют отрицательные значения
    s = 0
    r = 0
    while (arrayIsNegative(z, size)):

        # s - направляющий столбец
        # В первую очередь смотрим на коэффициент Q
        max = -sys.maxsize
        for i in range(size):
            if (z[0][i] > max and z[0][i] > 0):
                max = z[0][i]
                s = i
        # Если коэффициент Q == 0, то смотрим на числовой коэффициент
        if max == -sys.maxsize:
            for i in range(size):
                if (z[1][i] > max and z[1][i] > 0):
                    max = z[1][i]
                    s = i

        # Если все значения столбца отрицательны - выбрасываем ошибку
        ch = True
        for i in range(len(bazis[0])):
            if a[i][s] > 0:
                ch = False
        if ch:
            return Exception

        # r - направляющая строка
        min = sys.maxsize
        for i in range(len(bazis[0])):
            if (a[i][s] > 0):
                m = bazis[1][i] / a[i][s]
                if m < min:
                    min = m
                    r = i

        # Перерасчёт базиса
        b = copy.deepcopy(bazis)
        for i in range(len(bazis[0])):
            if i != r:
                b[1][i] = (bazis[1][i] * a[r][s] - a[i][s] * bazis[1][r]) / a[r][s]
            else:
                b[1][i] = bazis[1][i] / a[r][s]
        b[0][r] = s + 1
        bazis = copy.deepcopy(b)

        # Перерасчёт матрицы коэфициентов
        newA = copy.deepcopy(a)
        for i in range(len(a)):
            for j in range(len(a[i])):
                if r == i:
                    newA[i][j] = a[i][j] / a[r][s]
                else:
                    newA[i][j] = (a[r][s] * a[i][j] - a[r][j] * a[i][s]) / a[r][s]
        a = copy.deepcopy(newA)

        # funcZ - значений целевой функции
        funcZ = [0, 0]
        for i in range(len(bazis[0])):
            if (bazis[0][i] > size):
                funcZ[0] += bazis[1][i]
            else:
                funcZ[1] += c[bazis[0][i] - 1] * bazis[1][i]

        # z -  вектор z
        z = []
        z.append([])
        z.append([])
        for i in range(len(a[0])):
            deltaZ = [0, 0]
            for j in range(len(bazis[0])):
                if (bazis[0][j] > size):
                    deltaZ[0] += a[j][i]
                else:
                    deltaZ[1] += c[bazis[0][j] - 1] * a[j][i]
            if (i + 1 > size):
                deltaZ[0] -= 1
            else:
                deltaZ[1] -= c[i]
            z[0].append(deltaZ[0])
            z[1].append(deltaZ[1])

    # Запись результата
    result = []
    for i in range(size):
        if (bazis[0].__contains__(i + 1)):
            for j in range(len(bazis[0])):
                if (bazis[0][j] == i + 1):
                    result.append(bazis[1][j])
        else:
            result.append((0))
    return result

a = [
    [-2, 4, 3, 1, 3, 3, 3, 3],
    [5, 4, 5, 4, 2, 0, 3, 1],
    [1, 2, -1, 6, 0, 4, 1, 5]
]
b = [10, 10, 8]
c = [8, 8, 6, 5, 7, 6, 3, 5]

print(findOptimalVector(a, b, c))