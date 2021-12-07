from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import hcolor
import argparse
from collections import defaultdict
from collections import Counter


parser = argparse.ArgumentParser(description="to jest opis")
parser.add_argument('-file', help='file name', default='antygona.txt')
parser.add_argument('-n1', '--number', help='histogram size', type=int, default=10)
parser.add_argument('-n2', '--number2', help='minimal word length', type=int, default=0)
args = parser.parse_args()

with open(args.file, encoding='utf8') as f:
    data = f.read().strip().split()
    counts = Counter(data)
    print(counts)

sort = sorted(counts.items(), key=lambda e: e[1], reverse=True)

graph = Pyasciigraph(
    line_length=100,
    min_graph_length=50,
    separator_length=4,
    multivalue=False,
    human_readable='si',
    graphsymbol='$',
    )

lengthColor = {20:  Gre, 40: Blu, 60: Yel, 100: Red, 200: Cya}
data = hcolor(sort, lengthColor)


i = 0
for line in graph.graph(label="histogram słówek", data=data):
    if i-1 <= args.number:
        print(line)
        i += 1
    else:
        break

