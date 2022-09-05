import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# jako ze mozna podac dowolna ilosc wezlow i krawedzi
# to warunek zadania rowniez jest spelniony
print("prosze podac liczbe wezlow grafu")
N = int(input())
print("prosze podac liczbe krawedzi grafu, jako \nprzynajmniej dziesieciokrotnosc liczby wezlow")
E = int(input())
wykres = nx.gnm_random_graph(N, E)
nx.draw(wykres, with_labels=True)
plt.show()
