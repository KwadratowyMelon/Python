def fun(x):
    return x**2 - x - 1

def secant(f,a,b,N):
    for i in range(N):
        x = b - (f(b) * (a - b)) / (f(a) - f(b))
        if f(x)*f(b) > 0:
            b = x
        if f(x)*f(a) > 0:
            a = x
    return x

a = float(input("prosze podac lewa granice przedzialu: "))
b = float(input("prosze podac prawa granice przedzialu: "))
N = int(input("prosze podac ilosc iteracji: "))
print("komputer policzyl")

x = secant(fun,a,b,N)
if x == None:
    print("brak miejsc zerowych")
else:
    print(f"miejsce zerowe to {x:.12f}")