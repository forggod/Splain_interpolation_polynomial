import math

# Структура, описывающая сплайн на каждом сегменте сетки
class SplineTuple:
    def __init__(self, a, b, c, d, x):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x = x
 
# Построение сплайна
def BuildSpline(x, y, n):
    # x - узлы сетки, должны быть упорядочены по возрастанию, чётные узлы запрещены
    # y - значения функции в узлах сетки
    # n - количество узлов сетки
    splines = [SplineTuple(0, 0, 0, 0, 0) for _ in range(0, n)]
    for i in range(0, n):
        splines[i].x = x[i]
        splines[i].a = y[i]
    
    splines[0].c = splines[n - 1].c = 0.0
    
    # Решение СЛАУ относительно коэффициентов сплайнов c[i] методом прогонки
    # Вычисление прогоночных коэффициентов - прямой ход метода прогонки
    alpha = [0.0 for _ in range(0, n - 1)]
    beta  = [0.0 for _ in range(0, n - 1)]
 
    for i in range(1, n - 1):
        hi  = x[i] - x[i - 1]
        hi1 = x[i + 1] - x[i]
        A = hi
        C = 2.0 * (hi + hi1)
        B = hi1
        F = 6.0 * ((y[i + 1] - y[i]) / hi1 - (y[i] - y[i - 1]) / hi)
        z = (A * alpha[i - 1] + C)
        alpha[i] = -B / z
        beta[i] = (F - A * beta[i - 1]) / z
  
 
    # Нахождение решения - обратный ход метода прогонки
    for i in range(n - 2, 0, -1):
        splines[i].c = alpha[i] * splines[i + 1].c + beta[i]
    
    # По известным коэффициентам c[i] находим значения b[i] и d[i]
    for i in range(n - 1, 0, -1):
        hi = x[i] - x[i - 1]
        splines[i].d = (splines[i].c - splines[i - 1].c) / hi
        splines[i].b = hi * (2.0 * splines[i].c + splines[i - 1].c) / 6.0 + (y[i] - y[i - 1]) / hi
    return splines
 
 
# Вычисление значения интерполированной функции в произвольной точке
def Interpolate(splines, x):
    n = len(splines)
    s = SplineTuple(0, 0, 0, 0, 0)
    
    if x <= splines[0].x: # Если x меньше точки сетки x[0] - пользуемся первым эл-тов массива
        s = splines[0]
    elif x >= splines[n - 1].x: # Если x больше точки сетки x[n - 1] - пользуемся последним эл-том массива
        s = splines[n - 1]
    else: # Иначе x лежит между граничными точками сетки - производим поиск нужного эл-та массива
        i = 0
        j = n - 1
        while i + 1 < j:
            k = i + (j - i) // 2
            if x <= splines[k].x:
                j = k
            else:
                i = k
        s = splines[j]

    dx = x - s.x
    return s.a + (s.b + (s.c / 2.0 + s.d * dx / 6.0) * dx) * dx


x = [round(1/i, 4) for i in range(1, 6)]
y = [round(math.sin(math.pi*el), 4) for el in x]
print(*x, '\n', *y)

spline = BuildSpline(x, y, len(x))
x_ex = [0.8, 0.4]
y_ex = [Interpolate(spline, el) for el in x_ex]

print()

###################################################################################################################

print(" y = sin((PI * x)) ".center(40, '#'))
print(f'Точное значение'.center(40, '-'))
[print(f'x = {x_ex[i]} | y = {round(math.sin(math.pi*x_ex[i]), 4)}'.center(40, " ")) for i in range(2)]
print(f'Приблизительное значение'.center(40, '-'))
[print(f'x = {x_ex[i]} | y = {y_ex[i]}'.center(40, " ")) for i in range(2)]
print(f'Погрешность'.center(40, '*'))
[print(f'{round(abs(round(math.sin(math.pi*x_ex[i]), 4) - y_ex[i]), 10)}'.center(40, " ")) for i in range(2)]

###################################################################################################################

print()

    
spline = BuildSpline([1, 3, 7, 9], [5, 6, 7, 8], 4)
print(Interpolate(spline, 5))