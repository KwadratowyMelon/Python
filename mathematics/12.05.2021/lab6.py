import numpy as np
import time
import scipy.integrate as calka

def trapez(f, a, b, h):
    x = np.arange(a,b+h,h)
    s = np.sum(f(x))-0.5*f(a)-0.5*f(b)
    return h*s

def fun(x):
    return np.sin(x)

a = 0
b = np.pi
h = (b-1)/100000000
t1 = time.perf_counter()
c = trapez(fun,a,b,h)
t2 = time.perf_counter()
print('wynik:',c,'czas:',t2-t1)

t1 = time.perf_counter()
c = calka.quad(fun,a,b)[0]
t2 = time.perf_counter()
print('wynik:',c,'czas:',t2-t1)

calka.romberg(fun,a,b,show=True)

def MetodaRomberga(f,a,b):
    h = b - a
    I = np.zeros(4,float)
    for j in range(0,4):
        I[j] = trapez(f,a,b,h/2**j)
        for k in range(0,j):
            R = ((4**(k+1))*I[j]-I[j-1])/(4**(k+1) - 1)
    return R

t1 = time.perf_counter()
c = MetodaRomberga(fun, a, b)
t2 = time.perf_counter()
print('wynik:',c,'czas:',t2-t1)

# kiedy ilosc iteracji we wlasnej metodzie wybralem 33,
# to wyniku nigdy nie poznalem, a po 40 sekundach komputer sie zacial
# dlatego tez zostaja 4 kroki