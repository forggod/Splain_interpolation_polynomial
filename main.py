import math

# Структура, описывающая сплайн на каждом сегменте сетки
class SplineTuple:
    def __init__(self, a = 0, b = 0, c = 0, d = 0, x = 0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.x = x
 
# Построение сплайна
def BuildSpline(x, y, n):
    # x - узлы сетки
    # y - значения функции в узлах сетки
    # n - количество узлов сетки
    splines = [SplineTuple() for _ in range(0, n)]
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
    s = SplineTuple()
    
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
    return round(s.a + (s.b + (s.c / 2.0 + s.d * dx / 6.0) * dx) * dx, 8)

otstup = 100

###################################################################################################################

print(" y = sin((PI * x)) ".center(otstup, '#'))
print("Введите начало отрезка".center(otstup, '-'))
xl = int(input(''.center(round(otstup/2), ' ')))
print("Введите конец отрезка".center(otstup, '-'))
xr = int(input(''.center(round(otstup/2), ' ')))
print("Введите количество узлов".center(otstup, '-'))
knot = int(input(''.center(round(otstup/2), ' ')))

###################################################################################################################

sr = (xr-xl)/knot
x = []
temp = xl
for i in range(knot + 1):
    x.append(temp)
    temp += sr
y = [round(math.sin(math.pi*el), 8)for el in x]

spline = BuildSpline(x, y, len(x))

###################################################################################################################

x_ex = [float(input('введите произвольну точку: ')) for _ in range(2)]
y_ex = [Interpolate(spline, el) for el in x_ex]

###################################################################################################################

print()

###################################################################################################################

print(" y = sin((PI * x)) ".center(otstup, '#'))
print(f''.center(round(otstup/4), ' ') + f'Точное значение'.center(round(otstup/4), ' ')+ f'Приблизительное значение'.center(round(otstup/4), ' ') + f'Погрешность'.center(round(otstup/4), ' '))
[print(f'x = {x_ex[i]}'.center(round(otstup/4), " ") + f' y = {round(math.sin(math.pi*x_ex[i]), 4)}'.center(round(otstup/4), " ") + f'{y_ex[i]}'.center(round(otstup/4), " ") + 
f'{round(abs(round(math.sin(math.pi*x_ex[i]), 4) - y_ex[i]), 10)}'.center(round(otstup/4), " ")) for i in range(2)]

###################################################################################################################

print()
