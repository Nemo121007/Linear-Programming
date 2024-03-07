import copy
import sys

def Reduction(array):
    """
    Получение минимального элемента массива
    :param array: [int или double] массив
    :return: минимальный элемент
    """
    minSize = sys.maxsize
    for i in range(len(array)):
        if array[i] == "M":
            continue
        if array[i] < minSize:
            minSize = array[i]

    if (minSize != sys.maxsize):
        return minSize
    else:
        return None

def ReductionIgnore(array):
    """
    Исключение одного ноля из строки и нахождение минимального значения в массиве
    :param array: [int или double] массив
    :return: минимальный элемент без одного ноля
    """
    minSize = sys.maxsize
    flagNull = False
    for i in range(len(array)):
        if (array[i] == 0 and flagNull == False):
            flagNull = True
            continue
        elif array[i] == "M":
            continue
        elif array[i] < minSize:
            minSize = array[i]

    if (minSize != sys.maxsize):
        return minSize
    else:
        return None

def GetCostCrawl(matrix):
    """
    Подсчёт стоимости пути
    :param matrix: [[int или double]] матрица пути
    :return: int или double стоимость пути
    """

    di, dj = ["di"], ["dj"]

    # Проходим по всем строкам
    for i in range(1, len(matrix)):
        n = []
        for j in range(1, len(matrix)):
            n.append(matrix[i][j])
        # Находим и запоминаем минимальный элемент в строке
        di.append(Reduction(n))

    # Аналогично со всеми столбцами
    for j in range(1, len(matrix[0])):
        n = []
        for i in range(1, len(matrix)):
            n.append(matrix[i][j])
        dj.append(Reduction(n))

    # Считаем сумму всех минимальных элементов
    sum = 0
    for i in range(1, len(di)):
        sum += di[i]
    for i in range(1, len(dj)):
        sum += dj[i]

    return sum

def GetMaxElementMatrix(matrix):
    """
    Получение элемента с максимальным потенциалом
    :param matrix: [[int или double]] матрица пути
    :return: [[int, int]] список дуг с максимальным потенциалом
    """

    di, dj = ["di"], ["dj"]
    # Проходим по всем строками
    for i in range(1, len(matrix)):
        n = []
        for j in range(1, len(matrix)):
            n.append(matrix[i][j])
        # Исключаем один ноль из строки и находим минимальное значение в строке
        di.append(ReductionIgnore(n))

    # Аналогично проходим по столбцам
    for j in range(1, len(matrix[0])):
        n = []
        for i in range(1, len(matrix)):
            n.append(matrix[i][j])
        dj.append(ReductionIgnore(n))

    # Считаем сумму потенциалов в каждом элементе матрицы путей, равном 0
    maxSize = -sys.maxsize
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            if matrix[i][j] == 0:
                d = di[i] + dj[j]
                # Находим наибольшую сумму
                if d > maxSize:
                    maxSize = d

    indexMaxEl = []
    # Формируем список дуг с наибольшим потенциалом
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            if matrix[i][j] == 0:
                d = di[i] + dj[j]
                if d == maxSize:
                    indexMaxEl.append([i, j])

    return indexMaxEl

def ReductionMatrix(matrix, indexI, indexJ):
    """
    Редуцировнаие матрицы
    :param matrix: [[int или double]] изначальная матрица
    :param indexI: int номер строки для редуцирования
    :param indexJ: int номер столбца для редуцирования
    :return: [[int или dooble]] редуцированная матрица
    """
    m = []

    # Запоминаем точки, между которыми строим дугу
    deleteIndexI = matrix[indexI][0]
    deleteIndexJ = matrix[0][indexJ]

    # Проход по всем строкам
    for i in range(len(matrix)):
        n = []
        # Проход по всем столбцам
        for j in range(len(matrix[i])):
            # Исключаем строку и столбец, по которым происходи редукция
            if (i != indexI and j != indexJ):
                # Если элементы образуют дугу, обратную дуге, по которой происходит редуцирование
                if deleteIndexI == matrix[0][j] and deleteIndexJ == matrix[i][0]:
                    # Исключаем её из рассмотрения
                    n.append("M")
                    continue
                # Иначе
                n.append(matrix[i][j])
        if n != []:
            m.append(n)
    # Возвращаем редуцированную матрицу
    return m

def NormalizeMatrix(matrix):
    """
    Оценивание матрицы
    :param matrix: [[int или double]] матрица пути
    :return: [[int  double]] обработанная матрица пути, int или double стоимость пути
    """

    summary = 0
    # Проходим по всем строкам
    for i in range(1, len(matrix)):
        n = []
        for j in range(1, len(matrix)):
            n.append(matrix[i][j])
        # Находим минимальный элемент строки
        d = Reduction(n)
        # Добавляем элемент к стоимости пути
        summary += d
        # Отнимаем от всех значений строки минимальный элемент
        for j in range(1, len(matrix)):
            if matrix[i][j] == "M":
                continue
            else:
                matrix[i][j] -= d

    # Аналогично по всем столбцам
    for j in range(1, len(matrix[0])):
        n = []
        for i in range(1, len(matrix)):
            n.append(matrix[i][j])
        d = Reduction(n)
        summary += d
        for i in range(1, len(matrix)):
            if matrix[i][j] == "M":
                continue
            else:
                matrix[i][j] -= d

    # Возвращаем пересчитанную матрицу и стоимость пути
    return matrix, summary

def ReturnPath(path):
    """
    Восстановление пути
    :param path: [(int, int)] список дуг в маршруте
    :return: [(int, int)] маршрут
    """
    # Формируем список дуг
    l = []
    for i in range(len(path)):
        l.append([path[i]])

    flag = True
    # Пока происходят изменения в списке дуг
    while(flag):
        flag = False
        i, j, lenI, lenJ = 0, 0, len(l), len(l)
        # Проход по всем дугам в списке
        while i < lenI:
            # Проход по всем дугам в списке
            while j < lenJ:
                # Если конец одной дуги является началом другой
                if (l[i][len(l[i]) - 1][1] == l[j][0][0] and
                    (l[i][len(l[i]) - 1][0] != l[j][0][0] and l[i][len(l[i]) - 1][1] != l[j][0][1])):
                    # Представляем эти две дуги как одну
                    for k in range(len(l[j])):
                        m = l[j][0]
                        l[i].append(m)
                        l[j].remove(m)
                        if l[j] == []:
                            l.remove([])

                        flag = True
                j += 1
                lenJ = len(l)
            j = 0
            i += 1
            lenI = len(l)
        i = 0
        j = 0

    if len(l) == 1:
        path = l[0]

        """
        #Для замкнутого обхода!
        path.append((path[len(path) - 1][1], path[0][0]))
        """
        return path
    else:
        return None

def BranchCycle(matrix, lenghtPath, path):
    """
    Иттеративный шаг обхода
    :param matrix: [int или double] матрица пути
    :param lenghtPath: [int] актуальная длинна пути
    :param path: [(int, int)] дуги пути
    :return: [(int, int)] дуги пути
    """
    """
    Исключённые ребра (например, петли) имеют длинну M, гораздо большую любой длинны ребра
    """

    # Если размер матрицы 2 на 2
    if len(matrix) == 3:
        # Для элемента со стоимостью перехода 0
        for i in range(1, len(matrix)):
            for j in range(1, len(matrix[i])):
                if matrix[i][j] == 0:
                    m = copy.deepcopy(path)
                    # Добавляем дугу обхода
                    m.append((matrix[i][0], matrix[0][j]))
                    # Восстанавливаем путь
                    p = ReturnPath(m)
                    # Возвращаем путь
                    if p != None:
                        return p
        return None

    # Определяем переходы с максимальным потенциалом
    maxIndex = GetMaxElementMatrix(matrix)

    # Проходим по переходам с максимальным потенциалом
    for i in range(len(maxIndex)):

        # Исключаем переход по дуге
        matrixExcludedEdge = copy.deepcopy(matrix)
        matrixExcludedEdge[maxIndex[i][0]][maxIndex[i][1]] = "M"
        # Считаем стоимость исключения дуге
        lenghtmatrixExcludedEdge = GetCostCrawl(matrixExcludedEdge)

        # Редуцируем матрицу
        reduceMatrix = ReductionMatrix(copy.deepcopy(matrix), maxIndex[i][0], maxIndex[i][1])
        # Оцениваем и считаем стоимость редуцированной матрицы
        reduceMatrix, lenghtReduceMatrix = NormalizeMatrix(copy.deepcopy(reduceMatrix))

        # Если исключить дугу дешевле перехода по ней
        if lenghtReduceMatrix > lenghtmatrixExcludedEdge:
            # Продолжаем расчёты
            p = BranchCycle(matrixExcludedEdge, lenghtPath + lenghtmatrixExcludedEdge, path)

            # Возвращаем маршрут
            if p != None:
                return p
        # Иначе
        else:
            # Добавляем дугу к маршруту
            path.append((matrix[maxIndex[i][0]][0], matrix[0][maxIndex[i][1]]))
            # Продолжаем расчёты
            p = BranchCycle(reduceMatrix, lenghtPath + lenghtReduceMatrix, path)
            # Возвращаем маршрут
            if p != None:
                return p

def TravellingSalesmanProblem(matrixPath):
    """
    Решение задачи коммивояжёра
    :param matrixPath: [[int или double]] матрица пути
    :return: [(int, int)] маршрут, int или double расстояние
    """

    matrix = []
    n = []
    # Добавляем к матрице перехода нулевую строку с номерами городов
    for i in range(len(matrixPath[0]) + 1):
        n.append(i)
    matrix.append(n)

    # Добавляем к матрице перехода нулевой столбец с номерами городов
    for i in range(len(matrixPath)):
        n = [i + 1]
        for j in range(len(matrixPath[i])):
            n.append(matrixPath[i][j])
        matrix.append(n)

    # Оцениваем матрицу пути и первоначальную длинну маршрута
    mat, lenghtPath = NormalizeMatrix(copy.deepcopy(matrix))
    path = []

    # Запускаем циклический обход
    l = BranchCycle(mat, lenghtPath, path)

    # Рассчитываем пройденное расстояние
    s = 0
    for k in range(len(l)):
        for i in range(len(matrix)):
            if matrix[i][0] == l[k][0]:
                for j in range(len(matrix[i])):
                    if matrix[0][j] == l[k][1]:
                        s += matrix[i][j]

    return l, s


matrixPath = [
    ["M", 5, 6, 8, 5, 8],
    [5, "M", 4, 6, 6, 3],
    [4, 3, "M", 1, 9, 2],
    [3, 4, 7, "M", 5, 4],
    [5, 4, 8, 8, "M", 3],
    [1, 6, 0, 3, 7, "M"]
]

pathMove, distance = TravellingSalesmanProblem(matrixPath)
print(pathMove)
print("Дистанция " + str(distance))