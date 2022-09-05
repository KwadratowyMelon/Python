import numpy as np
import matplotlib.pyplot as plt


def step(spins, M, T):
    for i in range(N):
        x = np.random.randint(N)  #losuje jeden spin
        z = np.sum(spins) - spins[x]  #licze sume spinow moich sasiadow
        B = 1/(kb*T)

    return spins, M


nsteps = 10  #liczba krokow symulacji
N = 1000  #rozmiar ukladu
T = 2000  #temperatura maksymalna
kb = 8.617*10^(-5) #stala boltzmana
spins = np.ones(N)
M = N
m = np.zeros(nsteps)

fig = plt.figure()
plt.axis([500, 2000, -2, 2])

for i in range(500, T):
    for t in range(nsteps):
        spins, M = step(spins, M, T)
        m[t] = M/N
        plt.plot(, m)

plt.show()
