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


def jacobi2(a, b, x, N):
    beta = b/np.diag(a)
    alfa = -np.array(a)
    alfa = (alfa.T/np.diag(a)).T
    np.fill_diagonal(alfa, 0)
    for k in range(N):
        x = beta +np.dot(alfa, x)
    return x

def MPD(n,debug=False):
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


A=MPD(3)
B = [1, 2, 3]
X = [0, 0, 0]

print('Metoda Jacobiego: ')
jacobi(A, B, X, 20, True)
print('Metoda Jacobiego2: ')
jacobi2(A, B, X, 20)
print('Sprawdzenie: ')
print(np.linalg.solve(A, B))