import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib import animation

# w kodzie zaimplementowano dobrane na oko sily oporu aby wahadlo po pewnym czasie sie zatrzymalo
def pendulum(u, t):
    du = np.zeros(4)
    du[0] = u[1]
    du[1] = (- 3*np.sin(u[0]) - np.sin(u[0]-2*u[2]) - 2*np.sin(u[0]-u[2])*(u[3]*u[3]+(u[1]*u[1])*np.cos(u[0]-u[2])))/(3 - np.cos(2*u[0]-2*u[2])) - 0.05*u[1]   #dodana mala sila oporu
    du[2] = u[3]
    du[3] = (2*np.sin(u[0]-u[2])*(2*u[1]*u[1]+2*np.cos(u[0])+(u[3]*u[3])*np.cos(u[0]-u[2])))/(3 - np.cos(2*u[0]-2*u[2])) - 0.05*u[3]  #mala sila oporu
    return du


def update(i):
    plt.clf()
    plt.axis([-2, 2, -2, 2])
    plt.plot([0, x1[i]], [0, y1[i]])
    plt.plot([x1[i]], [y1[i]], 'o')
    plt.plot([x1[i], x2[i]], [y1[i], y2[i]])
    plt.plot([x2[i]], [y2[i]], 'o')


u0 = [np.pi/2, 0, np.pi/2, 0]  # warunki poczatkowe
tmax = 1000  # czas symulacji
N = 2000  # liczba krokow symulacji
t = np.linspace(0, tmax, N)

wynik = odeint(pendulum, u0, t)
theta1 = wynik[:, 0]

x1 = np.sin(theta1)
y1 = -np.cos(theta1)

theta2 = wynik[:, 2]

x2 = x1 + np.sin(theta2)
y2 = y1 - np.cos(theta2)

fig = plt.figure()

anim = animation.FuncAnimation(fig, update, frames=N, interval=20)
plt.show()
