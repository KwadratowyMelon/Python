import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from scipy.interpolate import CubicSpline

#zadanie 1
def fun(x, a, b, c, d):

    return c*np.cos(b*x)/(np.exp(a/d))


x = np.linspace(-5, 5, num=20)
y = fun(x, 2, -5, 4, -1) + 30*np.random.normal(size=20)

cs = CubicSpline(x, y, bc_type="natural")

xtype = np.linspace(-2, 6, 100)
ytype = cs(xtype)
plt.plot(x, y, 'ro')
plt.plot(xtype, ytype)
plt.show()
