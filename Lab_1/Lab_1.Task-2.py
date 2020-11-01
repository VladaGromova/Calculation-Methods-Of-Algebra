import copy

import numpy as np

# A*(A^(-1)) = E
# A*E = E*(A^(-1))

arr = np.array([[3.0, 12.0, -1.0, 0.0],
               [-5.0, 2.0, 0.0, 32.0],
               [2.0, 0.0, 16.0, -3.0],
               [12.0, 3.0, 0.0, 0.0]])
a = copy.deepcopy(arr)      # arr будет приводиться к единичной матрице, поэтому для проверки в конце нам нужна будет копия исходной матрицы
n = 4
e = np.eye(n)
#Прямой ход метода Гаусса (подробно описано в Lab_1.py), только теперь мы арифметические операции проводим не над столбцом свободных членов, а над единичной матрицей
for j in range(n):
    index = j
    maxi = abs(arr[j][j])
    for i in range((j + 1), n):
        if abs(arr[i][j]) > maxi:
            maxi = abs(arr[i][j])
            index = i
    if index != j:
        tmp = copy.deepcopy(arr[j])
        arr[j] = arr[index]
        arr[index] = tmp
        tmp = copy.deepcopy(e[j])
        e[j] = e[index]
        e[index] = tmp
    for i in range((j + 1), n):
        m = float(((arr[i][j]) * (-1)) / (arr[j][j]))
        arr[i] += (arr[j]) * m
        e[i] += (e[j]) * m

for i in reversed(range(n)):
    e[i] /= (arr[i][i])
    arr[i] /= (arr[i][i])       #делаем 1 на главной диагонали
    for j in range(i):      #зануляем все элементы, стоящие над главной диагональю (ниже главной диагонали уже стоят нули после прямого зода метода Гаусса)
        if arr[j][i] != 0:      #если элемент уже равен нулю, то его уже занулять не надо, естествено
            m = (-1)*(arr[j][i])
            arr[j] += m*(arr[i])
            e[j] += m*(e[i])
#теперь в e хранится обратная матрица
#Проверка:
check = np.dot(a, e)
check = np.around(check, decimals=1)
ans = "["
for i in range(4):
    for j in range(4):
        ans += str(e[i][j])
        ans += "]"
        ans += ", "
        if j == 3:
            ans += '\n'
checkans = "["
for i in range(4):
    for j in range(4):
        checkans += str(check[i][j])
        checkans += "]"
        checkans += ", "
        if j == 3:
            checkans += '\n'
output = open("Output.txt", "w")
output.write(ans)
output.write('\n')
output.write(checkans)
output.close()