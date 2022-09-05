def fun(x):
    return x**2 - x - 1

def bisection(f,a,b,d,debug=False):
    left = a
    right = b
    epsilon = d
    i = 0
    while (epsilon < (right-left)):
        i += 1
        mid = (left + right) / 2
        if debug:
            print("krok          x0      epsilon")
            print(f"{i:4} {mid:12} {right - left:12}")
        else:
            return None
        if f(left) * f(mid) < 0:
            right = mid
        elif f(mid) * f(right) < 0:
            left = mid
        elif f(mid) == 0:
            return mid
        else:
            return None
        if i > 100:
            break
    return mid

a = float(input("prosze podac lewa granice przedzialu: "))
b = float(input("prosze podac prawa granice przedzialu: "))
d = float(input("prosze podac z jaka precyzja policzyc miejsce zerowe: "))
print("komputer policzyl")

x = bisection(fun,a,b,d,debug=True)
if x == None:
    print("brak miejsc zerowych")
else:
    print(f"miejsce zerowe to {x:.12f}")