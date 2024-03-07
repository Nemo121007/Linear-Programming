import copy
import sys

def GenerateCleanMatrix(A, B):
    """
    Генерация пустого двумерного массива, заполненного 0
    :param A: int - количество строк в масссиве
    :param B: int - количество столбцов в массиве
    :return: [[int]] - пустой двумерный массив, заполненный 0
    """
    c = []
    for i in range(len(A)):
        n = []
        for j in range(len(B)):
            n.append(0)
        c.append(n)
    return c

def CheakArray(array, ignorIndex):
    """
    Проверка массива на наличие в нём подходящих для перегруппировки базисных элементов
    :param array: [str] массив для проверки
    :param ignorIndex: [int] индекс стартового элемента
    :return: [str] - "True" - в массиве есть подходящие для перегруппировки элементы
    "False" - подходящих элементов нет
    "s" - с помочью данного элемента можно замкнуть цикл, вернувшись на старт
    """
    flag = False

    for i in range(len(array)):
        if i == ignorIndex:
            continue
        if array[i] == "":
            continue
        if array[i] == "s" and array[ignorIndex] == "-":
            return "s"
        if array[i] == "?":
            flag = True
        if array[i] != "?":
            return "False"

    if flag:
        return "True"
    else:
        return "False"

def Search(matrix, direction, sign, startI, startJ):
    """
    Рекурсивный поиск цикла для перегруппировки грузов
    :param matrix: [[str]] - матрица с отмеченными пунктами
    :param direction: str - направление поиска (в строку(row) или столбец(column))
    :param sign: str - знак стартовой ячейки
    :param startI: int - стартовый номер строки
    :param startJ: int - стартовый номер столбца
    :return: [[str]] - матрица с ячейками для перегруппировки груза
    """
    """
    Идея поиска:
    Базисные (т.е. доступные для перегруппировки) ячейки в матрице обозначены знаком "?"
    
    Начинаем искать с первоначально полученной ячейки. Ставим в неё знак "s"(только при первой иттерации).
    Проверяем строку (столбец) ячейки, откуда начали поиск. При нахождении ячейки, помеченной "?", вызываем следующую 
    иттерацию функции, указывая в качестве аргументов матрицу, противоположное направление (row меняем на column и наоборот),
    знак "-" и номер строки и столбца ячейки.
    Начало цикла:
        Помечаем ячейку переданным знаком("+" или "-"). Ищем ячейки, помеченные "?" или "s" 
            в переданном направлении(row или column). 
        Если по указанному направлению нет ячеек, помеченных "?" или если в строке(столбце) 
            есть другие элементы ("+" или "-"), возвращаем из функции NOUN и переходим к другой ячейке.
        Если по указанному направлению есть ячейка, помеченная "s"(стартовая ячейка) и в помеченной на данном шаге 
            ячейке содержится "-", то возвращаем матрицу с помеченными ячейками.
        Если по указанному направлению есть ячейка, помеченная "?", вызываем иттерацию функции, указывая 
            в качестве аргументов матрицу, противоположное направление (row меняем на column и наоборот), 
            противоположный знак ("-" меняем на "+" и наоборот) и номер строки и столбца ячейки.
    """
    """
    Де-факто выполняем условия:
    Необходимо расставить чередующиеся значения "+ " и " — " в таблице так, чтобы получился замкнутый цикл 
        и выполнялись правила:
            - остальные знаки цикла (все кроме уже поставленного первого " + ") ставим только в заполненных (базисных) 
                ячейках таблицы,
            - если в строке есть "плюс" ("минус"), то в этой строке должен быть и "минус" ("плюс"),
            - если в столбце есть " плюс" ("минус"), то в этом столбце должен быть и "минус" ("плюс").
    """

    matrix[startI][startJ] = sign

    newSign = ""
    if sign == "+":
        newSign = "-"
    elif sign == "-":
        newSign = "+"
    elif sign == "s":
        newSign = "-"

    if direction == "row":
        if (CheakArray(matrix[startI], startJ) == "s"):
            return matrix

        if (CheakArray(matrix[startI], startJ) == "True"):

            for j in range(len(matrix[0])):
                if (matrix[startI][j] != "" and matrix[startI][j] != matrix[startI][startJ]):
                    c = Search(copy.deepcopy(matrix), "column", newSign, startI, j)

                    if (c != None):
                        return c

    elif direction == "column":
        n = []
        for i in range(len(matrix)):
            n.append(matrix[i][startJ])

        if (CheakArray(n, startI) == "s"):
                return matrix

        if (CheakArray(n, startI) == "True"):

            for i in range(len(matrix)):
                if (matrix[i][startJ] != "" and matrix[i][startJ] != matrix[startI][startJ]):
                    c = Search(copy.deepcopy(matrix), "row", newSign, i, startJ)
                    if (c != None):
                        return c
    return None

def CheckMatrix(u,v):
    """
    Проверка потенциалов на их определенность
    :param u: [int или double] Потенциалы продавца
    :param v: [int или double] Потенциалы покупателя
    :return: True если определены все потенциалы покупателя и продавца, иначе False
    """
    for i in range(len(u)):
        if (u[i] == "?"):
            return False
    for i in range(len(v)):
        if (v[i] == "?"):
            return False
    return True

def Comparison(newUV, oldUV):
    """
    Сравнение двух версий потенциалов
    :param newUV: [int или double] - новый набор потенциалов
    :param oldUV: [int или double] - старый набор потенциалов
    :return: True старый и новый набор потенциалов совпадают, иначе False
    """
    for i in range(len(newUV)):
        for j in range(len(newUV[i])):
            if newUV[i][j] != oldUV[i][j]:
                return False
    return True

def GetCostMatrix(referencePath, costMatrix):
    """
    Расчёт оценочной матрицы
    :param referencePath: [[int или double]] план поставок
    :param costMatrix: [[int или double]] матрица стоимости перевозки
    :return: [[int или double]] матрица оценки
    """
    # Создаём пустую матрицу
    matrix = GenerateCleanMatrix(referencePath, referencePath[0])

    # Заполняем значения, совпадающие с базисными
    for i in range(len(referencePath)):
        for j in range(len(referencePath[i])):
            if (referencePath[i][j] != 0):
                matrix[i][j] = costMatrix[i][j]

    # Заполняем массивы потенциалов знаками "?"
    u, v = [], []  
    for i in range(len(costMatrix)):
        u.append("?")
    for j in range(len(costMatrix[0])):
        v.append("?")

    # Для избежания цикла присваиваем первому потенциалу значение 0
    u[0] = 0

    # Записываем значеия потенциалов
    pastMatrix = copy.deepcopy([u, v])

    # Пока не заполнены потенциалы
    while (not CheckMatrix(u, v)):

        # Заполняем потенциалы, исходя из уравнений
        for i in range(len(u)):
            for j in range(len(v)):
                if (referencePath[i][j] != 0 and u[i] != "?"):
                    v[j] = costMatrix[i][j] - u[i]

        for i in range(len(u)):
            for j in range(len(v)):
                if (referencePath[i][j] != 0 and v[j] != "?"):
                    u[i] = costMatrix[i][j] - v[j]


        # Записываем новые значения потенциалов
        newMatrix = [u, v]
        # Если значения старых и новых потенциалов совпадают
        if (Comparison(pastMatrix, newMatrix)):
            # Пересчитываем систему уравнений
            for i in range(len(u)):
                if u[i] == "?":
                    for j in range(len(v)):
                        if (v[j] != "?"):
                            u[i] = costMatrix[i][j] - v[j]

        pastMatrix = copy.deepcopy(newMatrix)

    # Рассчитываем остальные значения оценочной матрицы
    for i in range(len(u)):
        for j in range(len(v)):
            if referencePath[i][j] == 0:
                costMatrix[i][j] = v[j] + u[i]

    return costMatrix


def isArrayEmpty(array):
    """
    Проверка на наличие 0 в массиве
    :param array: [int или double] массив для проверки
    :return: True, если нет элементов, отличных от 0, иначе False
    """
    for i in range(len(array)):
        if array[i] != 0:
            return False
    return True

def DifferenceArray(array):
    """
    Определение разницы меджу двумя минимальными элементами в массиве
    :param array: [int или double] массив для проверки
    :return: [int или double] разница меджу двумя минимальными элементами массива
    """

    minSizeA, minSizeAI, minSizeB = sys.maxsize, sys.maxsize, sys.maxsize
    # Проходим по всему массиву
    for i in range(len(array)):
        # Если новый элемент меньше первой переменной
        if (array[i] < minSizeA):
            # Если первая переменная меньше второй
            if (minSizeA < minSizeB):
                # Вторую заменяем на первую
                minSizeB = minSizeA
            # Первой присваиваем новое значение
            minSizeA = array[i]
            minSizeAI = i
            continue
        # Вторая переменная больше первой и не равна первой
        if (array[i] < minSizeB and minSizeAI != i):
            minSizeB = array[i]

    # Если один из элементов не найден, присваиваем ему значение 0
    if minSizeA == sys.maxsize:
        minSizeA = 0
    if minSizeB == sys.maxsize:
        minSizeB = 0

    # Возвращаем разницу между переменными
    return minSizeB - minSizeA


def MethodVogel(A, B, C):
    """
    Поиск начального базиса методом Вижинера
    :param A: int или double - предложение у поставщиков
    :param B: int или double - спрос у покупателей
    :param C: [[int или double]] - матрица стоимости перевозок
    :return: [[int или double]] - матрица перевозок
    """
    referencePlan = GenerateCleanMatrix(A, B)
    a = copy.deepcopy(A)
    b = copy.deepcopy(B)

    # Пока у поставщиков есть товар и есть покупатели
    while not (isArrayEmpty(a) and isArrayEmpty(b)):
        maxSize, maxStrI, maxStrJ = -sys.maxsize, 0, 0
        listMaxStr = []

        # Рассматриваем строку (если у поставщика есть товар)
        for i in range(len(A)):

            if a[i] == 0:
                continue

            array = []
            for j in range(len(B)):
                if b[j] != 0:
                    array.append(C[i][j])

            # Считаем значение строки (значение равно сумме разнице наименьших элементов строки)
            m = DifferenceArray(array)
            # Если данный элемент является наименьшим среди аналогичных элементов всех строк
            # то добавляем его в список минимальных элементов
            if (maxSize < m):
                maxSize = m
                listMaxStr = [i]
            elif (maxSize == m):
                listMaxStr.append(i)

        listMaxCol = []
        # Аналогично рассматриваем столбцы (если у покупателя остался спрос)
        for j in range(len(B)):

            if b[j] == 0:
                continue

            array = []
            for i in range(len(A)):
                if a[i] != 0:
                    array.append(C[i][j])

            m = DifferenceArray(array)
            # Дописываем/переписываем список строк и столбцов с минимальными элементами
            if (maxSize < m):
                maxSize = m
                listMaxStr = []
                listMaxCol = [j]
            elif (maxSize == m):
                listMaxCol.append(j)

        mintariff = sys.maxsize

        # Среди всех строк и столбцов с минимальным значением ищем ячейку с минимальной стоимостью
        minElI, minElJ = 0, 0
        for i in range(len(listMaxStr)):
            for j in range(len(B)):
                if b[j] == 0:
                    continue
                if (C[listMaxStr[i]][j] < mintariff):
                    mintariff = C[listMaxStr[i]][j]
                    minElJ = j
                    minElI = listMaxStr[i]

        for j in range(len(listMaxCol)):
            for i in range(len(A)):
                if a[i] == 0:
                    continue
                if (C[i][listMaxCol[j]] < mintariff):
                    mintariff = C[i][listMaxCol[j]]
                    minElI = i
                    minElJ = listMaxCol[j]

        # Заполняем ячейку максимальным объёмом
        d = min(a[minElI], b[minElJ])
        referencePlan[minElI][minElJ] = d
        a[minElI] -= d
        b[minElJ] -= d

    return referencePlan


def GetOptimalRoute(A, B, C):
    """
    Функция поиска оптимального решения транспортной задачи
    :param A: int или double - предложение у поставщиков
    :param B: int или double - спрос у покупателей
    :param C: int или double - матрица стоимости доставки
    :return: [[double]] или [[int]] - матрица оптимального распределения поставок,
    double или int - оптимальная стоимость поставок

    Только для закрытых транспортных задач!!!
    """

    # Находим начальное решение методом северо-западного угла
    a = copy.deepcopy(A)
    b = copy.deepcopy(B)
    # referencePlan - актуальный план поставок
    referencePlan = GenerateCleanMatrix(A, B)

    # Получаем начальный план поставок методом Вижинера
    referencePlan = MethodVogel(A, B, C)

    # Считаем сумму поставок у начального решения
    Pastsum = 0
    for i in range(len(referencePlan)):
        for j in range(len(referencePlan[0])):
            if referencePlan[i][j] != 0:
                Pastsum += referencePlan[i][j] * C[i][j]

    # Флаг оптимальности решения
    flagOptimalSolution = False

    # Пока решение не оптимально
    while not flagOptimalSolution:

        # Переносим в оценочную матрицу оценки из актуального плана поставок
        costMatrix = GenerateCleanMatrix(A, B)
        for i in range(len(A)):
            for j in range(len(B)):
                if (referencePlan[i][j] != 0):
                    costMatrix[i][j] = C[i][j]

        # Рассчитываем остальные поставки, входящие в актуальный план так, что
        # сумма потенциала покупателя и потенциала поставщика равна значению стоимости поставки
        costMatrix = GetCostMatrix(referencePlan, costMatrix)

        # Вычитаем из стоимости поставок оценочные стоимости
        for i in range(len(costMatrix)):
            for j in range(len(costMatrix[0])):
                costMatrix[i][j] = C[i][j] - costMatrix[i][j]

        # Переводим флаг оптимального решения в состояние True
        flagOptimalSolution = True

        # Ищем элементы оценочной матрицы, меньшие 0. Если такие есть - флаг оптимального решения в состояние False
        # Ищем минимальный отрицательный элемент и запоминаем его
        minSize, minI, minJ = sys.maxsize, sys.maxsize, sys.maxsize
        for i in range(len(costMatrix)):
            for j in range(len(costMatrix[0])):
                if costMatrix[i][j] < 0:
                    flagOptimalSolution = False
                    if costMatrix[i][j] < minSize:
                        minSize = costMatrix[i][j]
                        minI = i
                        minJ = j

        # Если решение не оптимально
        if not flagOptimalSolution:

            # Создаём матрицу для поиска цикла перестановок
            matrixPath = []
            for i in range(len(referencePlan)):
                n = []
                for j in range(len(referencePlan[0])):
                    if referencePlan[i][j] != 0:
                        n.append("?")
                    else:
                        n.append("")
                matrixPath.append(n)

            # Ищем цикл перестановок
            matrixDelta = Search(matrixPath, "row", "s", minI, minJ)

            if matrixDelta == None:
                return  referencePlan, sum
            # Среди элементов, помеченных знаком "-" ищем минимальный - это дельта
            maxDelta = sys.maxsize
            for i in range(len(matrixDelta)):
                for j in range(len(matrixDelta[0])):
                    if (matrixDelta[i][j] == "-" and referencePlan[i][j] < maxDelta):
                        maxDelta = referencePlan[i][j]

            # К элементам, помеченным знаком "+" прибавляем дельту
            # К элементам, помеченным знаком "-" отнимаем дельту
            for i in range(len(matrixDelta)):
                for j in range(len(matrixDelta[0])):
                    if (matrixDelta[i][j] == "+" or matrixDelta[i][j] == "s"):
                        referencePlan[i][j] += maxDelta
                    elif matrixDelta[i][j] == "-":
                        referencePlan[i][j] -= maxDelta

        # Пересчитываем сумму поставок
        sum = 0
        for i in range(len(referencePlan)):
            for j in range(len(referencePlan[0])):
                if referencePlan[i][j] != 0:
                    sum += referencePlan[i][j] * C[i][j]

        # Если сумма поставок уменьшилась, записываем новую сумму в PastSum
        # Если сумма поставок не изменилась (т.е. sum == PastSum) - переводим флаг оптимального решения в положение True
        # Написано из-за того, что при некоторых входных данных алгоритм проваливается в вечный цикл и начинает
        # перемещать поставки по кругу, не уменьшая итоговую стоимость
        if (sum == Pastsum):
            flagOptimalSolution = True
        elif (sum < Pastsum):
            Pastsum = sum

    return referencePlan, sum

"""
A = [100, 200]
B = [50, 100, 75, 75]
C = [
    [4, 3, 5, 6],
    [8, 2, 4, 7]
]
"""
"""
Ответ:
50 0 0 50
0 100 75 25
Сумма: 1175
"""

"""
A = [60, 35, 65, 45, 60]
B = [80, 35, 25, 45, 30, 50]
C = [
    [7, 7, 5, 10, 6, 8],
    [6, 9, 9, 9, 6, 4],
    [4, 4, 6, 4, 7, 5],
    [7, 3, 9, 5, 7, 8],
    [10, 3, 5, 6, 5, 9]
]
"""
A = [70, 40, 45, 45, 45]
B = [60, 55, 30, 45, 35, 20]
C = [
    [4, 9, 4, 4, 9, 5],
    [3, 5, 9, 7, 4, 4],
    [7, 7, 6, 5, 4, 9],
    [4, 8, 10, 4, 5, 5],
    [8, 7, 6, 4, 9, 5]
]


plan, sum = GetOptimalRoute(A, B, C)
for i in range(len(plan)):
    print(plan[i])
print("Общая стоимость: " + str(sum))
