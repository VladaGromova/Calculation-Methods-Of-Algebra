import numpy as np

# Метод квадратного корня:

# Метод состоит в нахождении матриц S и D таких, что A = St*D*S, где:
# S - верхнетреугольная матрица
# St - S транспонированная
# D - диагональная с 1 и -1 на главной диагонали (матрица, отвечающая за знаки)

def solve(fileName, it):
    file = open(fileName, 'r')
    n = int(file.readline())
    # для экономии места в памяти будм хранить только верхний треугольник матрицы, т.к. по уловию она симметричсекая
    Arr = []
    for i in range(n):
        line = file.readline()
        a = np.array(list(map(float, line.split())))
        Arr.append(a)
    line = file.readline()
    Barr = np.array(list(map(float, line.split())))     # столбец свободных членов
    S = np.zeros((n, n))
    D = np.zeros(n)

    # Обозначим а(1,1) - первый элмент главной диагонали матрицы А, а(2,2) - второй, и т.д.
    # Для нахождения матриц S и D используются формулы:
    # d(1,1) - это единица со знаком a(1,1)
    # s(1,1) = корень из а(1,1)
    # А далее s(i,i) = корень из модуля разности а(i,i) и суммы по всем k от 1 до (i-1) произведения s(k,i)^2 на d(k,k)
    # d(i,i) - это единица со знаком того выражения, которое стоит под модулем
    # т.к. выражение, которое мы используем и для получения элемента матрицы D, и для вычисления элемента главной диагонали матрицы S, то будем хранить его в отдельной переменной val

    for i in range(n):
        sum = 0.0
        for k in range(i):
            sum += ((S[k][i])**2) * D[k]
        val = Arr[i][0] - sum
        # В D на главной диаонали стоит 1 со знаком val
        # А если val==0, то один из главных миноров будет нулевым, что не даст нам воспользоваться алгоритмом
        # поэтому необходимо сделать дополнительную проверку
        if val == 0:
            name = "Output" + str(it) + ".txt"
            output = open(name, "w")
            output.write("Нет")
            output.close()
            return
        D[i] = np.copysign(1, val)
        S[i][i] = np.sqrt(abs(val))
        # используем формулу:
        # s(i,j) = (a(i,j) - сумма по всем k от 1 до i-1 произведения s(k,i) на s(k,j), взятое со знаком элемента d(k,k))
        for j in range((i+1), n):
            sum = 0.0
            for k in range(i):
                sum += (S[k][i])*(D[k])*(S[k][j])
            S[i][j] = (Arr[i][(j-i)] - sum) / (S[i][i] * D[i])

    # Разложение найдено

    # det(A) = det(StDS) = det(St)*(detD)*(detS)
    # S и St - треугольные матрицы с одинаковыми элементами на главной диагонали
    # А определитель треугольной матрицы равень произведению элементов ее главной диагонали, поэтому получаем:
    # det(A) = ((det(S))^2)*(det(D))
    det = 1
    for i in range(n):
        det *= ((S[i][i])**2)*D[i]

    # Решение СЛАУ сводится к решению системы:
    # StDy = Barr
    # Sx = y

    # Алгоритм решения:
    # 1) прямой ход - нахождение y(i):
    # y(1) = Barr(1)/s(1)
    # y(i) = (Barr(i) - сумма по всем k от 1 до i-1 произведения s(i,k) на y(k))/s(i,i)

    y = np.zeros(n)
    S = S.transpose()
    y[0] = Barr[0] / S[0][0]
    for i in range(1, n):
        sum = 0.0
        for k in range(i):
            sum += S[i][k] * y[k]
        y[i] = (Barr[i] - sum)/S[i][i]


    # 2) обратный ход - нахождение x(i)
    # x(n) = y(n)/s(n,n)
    # x(i) = (y(i) - сумма по всем k от i+1 до n произведения s(i,k) на x(k))/s(i,i)

    x = np.zeros(n)
    S = S.transpose()
    x[n - 1] = (y[n - 1]) / (S[n - 1][n - 1])
    for i in range(n - 2, -1, -1):
        sum = 0.0
        for k in range(i+1, n):
            sum += S[i][k] * x[k]
        x[i] = (y[i] - sum)/(S[i][i])

    x = np.around(x, decimals=3)
    ans = "["
    for i in range(n):
        ans += str(x[i])
        if i != (n - 1):
            ans += ", "
    ans += "]"
    name = "Output" + str(it) + ".txt"
    output = open(name, "w")
    output.write("Да")
    output.write("\n")
    output.write("Решение СЛАУ:")
    output.write("\n")
    output.write(ans)
    output.write("\n")
    output.write("Определитель:")
    output.write("\n")
    output.write(str(det))
    output.close()

solve("input1.txt", 1)
solve("input2.txt", 2)
solve("input3.txt", 3)
solve("input4.txt", 4)
