import copy
import sys
import numpy as np

zeroEkviv = 0.0000000000001     #эквивалент нуля

def solve(fileName, it):
    file = open(fileName, 'r')
    n = int(file.readline())  # получаем размер матрицы и создаем пустой массив
    arr = np.empty([n, n])
    for i in range(n):
        # заполняем массив
        line = file.readline()
        a = np.array(list(map(float, line.split())))
        arr[i] = a
    bArr = np.array(list(map(float, (file.readline()).split())))

    # Прямой ход метода Гаусса
    numOfChanges = 0  # создаем переменную для подсчета перестановок строк местами (нужно для определения знака определителя)
    for j in range(n):
        index = j  # сохраняем индекс строки для дальнейшего понимания, нужно ли менять местами строки
        maxi = abs(arr[j][j])  # считаем, что элемент первого необработанного столбца на главной диагонали есть максимум
        for i in range((j + 1), n):
            if abs(arr[i][j]) > maxi:  # ищем максимум среди других элементов нашего столбца
                maxi = abs(arr[i][j])
                index = i  # если максимум найден, то переопределяем индекс
        if index != j:  # сравниваем с номером исходной строки
            ++numOfChanges  # если индекс строки с максимальным по модулю элементом в столбце не равен изначальному, то  требуется поменять местами строки, чтобы максимальный по модулю элемент стоял на главной диагонали
            tmp = bArr[j]
            bArr[j] = bArr[index]
            bArr[index] = tmp
            tmp = copy.deepcopy(arr[j])
            arr[j] = arr[index]
            arr[index] = tmp
        for i in range((j + 1), n):  # исключаем переменные под главной дагональю
            m = ((arr[i][j]) * (-1)) / (arr[j][j])
            arr[i] += (arr[j]) * m
            bArr[i] += (bArr[j]) * m  # не забываем провести арифметические операции над столбцом свободных членов
    # теперь наша матрица имеет треугольный вид (верхнетреугольная матрица)
    # по формуле(для треугольной матрицы): det = ((-1)^k)*(arr[0][0])*(arr[1][1])*...*(arr[n-1][n-1]), где k - количество перестановок строк местами (у нас это число хранится в numOfChanges)
    # причем индексация идет с нуля и таким образом a11 = arr[0][0],..., ann=arr[n-1][n-1]
    det = (-1) ** numOfChanges
    for i in range(n):
        if abs(arr[i][i]) <= zeroEkviv:
            # проверяем каждый элемент на главной диагонали на равенство 0
            # ведь если хоть один ~ 0 , то определитель равен 0, и тогда матрица вырожденная, т.е. СЛАУ или не имеет решений, или имеет бесконечно много решений
            name = "Output" + str(it) + ".txt"
            output = open(name, "w")
            output.write("Вырожденная матрица")
            output.close()
            return
        else:
            det *= (arr[i][i])

    # Начинаем обратный ход метода Гаусса:
    answer = np.empty(n)
    answer[(n - 1)] = (bArr[(n - 1)]) / (arr[(n - 1)][(n - 1)])  # получаем из последнего уравнения неизвестное xn
    # далее из предпоследнего уравнения, подставляя в него xn, находим значение x(n-1)
    # и т.д.
    for i in reversed(range(n - 1)):
        summ = 0.0
        j = (n - 1)
        while j > i:
            summ += (arr[i][j]) * answer[
                j]  # сумма вычисленных элементов, умноженных на соотв.коэффициенты для каждой строки
            j = (j - 1)
        answer[i] = (bArr[i] - summ) / arr[i][i]
    a = np.around(answer, decimals=1)
    ans = "["
    for i in range(n):
        ans += str(a[i])
        if i != (n-1):
            ans += ", "
    ans += "]"
    name = "Output" + str(it) + ".txt"
    output = open(name, "w")
    output.write(ans)
    output.write('\n')
    output.write(str(det))
    output.close()

solve("Input1.txt", 1)
solve("Input2.txt", 2)
solve("Input3.txt", 3)
solve("Input4.txt", 4)
solve("Input5.txt", 5)
solve("Input6.txt", 6)
solve("Input7.txt", 7)

