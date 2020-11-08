import numpy as np

# Метод правой прогонки

# Алгоритм (краткий):
# 1) прямая прогонка - находим все прогоночные коэффициенты альфа и бета

# альфа1 = -(первый элемент верхней диаг.)/(первый элемент главной)
# а дальше используем рекуррентную формулу: альфа(i) = -(i-тый элемент верхней диаг.)/
# /((i-1)-й нижней)*(альфа(i-1)) + i-тый элемент главной диагонали)
# При вычислении альфа i пробегает до n включительно

# бета1 = (первый элемент стобца свободных членов)/(первый элемент главной диагонали)
# бетаi = ((-1)*((i-1)-ый элемент нижней диагонали)*(бета(i-1)) + i-тый элемент столбца свободных членов)/
# /(такой же знаменатель, как у альфа i, поэтому при вычислении будем создавать отдельную переменную))
# при ычислении бета i пробегает до n+1 включительно

# 2) обратная прогонка - вычисление решения с помощью прогоноччных коэффициентов

# x(n) = бета(n)
# x(i) = (x(i+1))*(альфа(i)) + бета(i)
# i до 1 включительно

def solve(fileName, it):
    file = open(fileName, 'r')
    n = int(file.readline())        # получаем размер матрицы (т.е. кол-во неизвестных)
    # для экономии места в памяти будем хранить только 3 массива размером n (диагонали)
    line = file.readline()
    UpperDiag = np.array(list(map(float, line.split())))        # верхняя диагональ
    line = file.readline()
    MainDiag = np.array(list(map(float, line.split())))     # главная диагональ
    line = file.readline()
    LowerDiag = np.array(list(map(float, line.split())))        # нижняя диагональ
    line = file.readline()
    B = np.array(list(map(float, line.split())))        # получаем столбец свободных членов

    # Прямая прогонка:
    alpha = np.empty(n-1)       # создаем массив для прогоночных коэффициентов альфа
    beta = np.empty(n)      # аналогично для бета
    alpha[0] = (UpperDiag[0])*(-1)/(MainDiag[0])        # используем формулы, описанные выше
    beta[0] = (B[0])/(MainDiag[0])
    for i in range(1, (n-1)):           # 1, 2,..., 98
        denom = (LowerDiag[i-1])*(alpha[i-1]) + MainDiag[i]
        # если знаменатель равен 0, то решение будет некорректным, поэтому делаем дополнительную проверку
        if denom == 0:
            name = "Output" + str(it) + ".txt"
            output = open(name, "w")
            output.write("Нет")
            output.close()
            return
        alpha[i] = (-1)*(UpperDiag[i])/denom
        beta[i] = ((-1)*(LowerDiag[i-1])*(beta[i-1]) + B[i])/denom
    nomin = B[(n-1)] - LowerDiag[(n-2)] * beta[(n-2)]
    denomin = MainDiag[(n-1)] + LowerDiag[(n-2)] * alpha[(n-2)]
    beta[(n-1)] = nomin / denomin

    # Обратная прогонка:
    X = np.empty(n)
    X[(n-1)] = beta[n-1]
    for i in reversed(range(0, (n-1))):
        X[i] = (X[i+1])*(alpha[i]) + beta[i]
    # в Х хранится решение СЛАУ

    # Найдем определитель, который задается по рекуррентной формуле:
    # Если f(n) - это определитель трехдиагональной матрицы порядка n, то
    # f(n) = (n-тый эл. главной диаг.)*(f(n-1)) - ((n-1)-й эл. нижней)*((n-1)-й верхней)*(f(n-2))
    # Причем изначально задано: f(1) = 1; f(2) = 1-й элемент главной диагонали
    f = np.empty(n)
    f[0] = 1
    f[1] = MainDiag[0]
    for i in range(2, n):
        f[i] = (MainDiag[i-1])*(f[i-1]) - (LowerDiag[i-2])*(UpperDiag[i-2])*(f[i-2])
    det = (f[n-1])*(MainDiag[n-1]) - (LowerDiag[n-2])*(UpperDiag[n-2])*(f[n-2])

    X = np.around(X, decimals=3)
    ans = "["
    for i in range(n):
        ans += str(X[i])
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

solve("input5.txt", 5)
solve("input6.txt", 6)
solve("input7.txt", 7)