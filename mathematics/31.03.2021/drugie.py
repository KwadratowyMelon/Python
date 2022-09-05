import numpy as np

def jacobi (a, b, x, N, debug=False):
    n = len(x)  # długość tablicy
    x_new = x[:] # nowy obiekt nie kopia
    for k in range(N):
        for i in range(n):
            temp = b[i]
            for j in range(n):
                if(j != i):
                    temp -= a[i][j] * x[j]
            x_new[i] = temp/a[i][i]
        x = x_new[:]
        if(debug):
            print(f'{k:3}', end='')
            for i in range(n):
                print(f'{x[i]:13.8f}', end='')
            print()
    return x


def  gaussseidl(a, b, x, N, debug=False):
    n = len(x)  # długość tablicy
    for k in range(N):
        for i in range(n):
            sigma = 0
            for j in range(i):
                sigma = sigma + a[i][j] * x[j]
            for j in range(i+1, n):
                sigma2 = sigma + a[i][j] * x[j]
            x[i] = (b[i] - sigma - sigma2)/a[i][i]

        if(debug):
            print(f'{k:3}', end='')
            for i in range(n):
                print(f'{x[i]:13.8f}', end='')
            print()
    return x


def MPD(n, debug=False):
    rng = np.random.default_rng(12345)
    dod = rng.random()
    A = np.random.rand(n, n)
    if debug:
        print(f'Utworzona macierz wyglada nasteujaco: \n{A}')
        print(f'Dodatkowa dodawana liczba do przekatnej wynosi: {dod}')
    h = 0
    while 1:
        A[h, h] = n+dod
        h = h + 1
        if h == n:
            break
    print(f'Ostateczna postać macierzy przekatniowo dominujacej wyglada tak: \n{A}\n')
    return A


A = MPD(3)
B = [1, 2, 3]
X = [0, 0, 0]


print('Metoda Jacobiego: ')
jacobi(A, B, X, 20, True)
print('Metoda Gaussa-Seidla: ')
gaussseidl(A, B, X, 20, True)
