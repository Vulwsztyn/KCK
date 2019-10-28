import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import csv


def srednia(l):
    return sum(l) / len(l)


def formaterOsiPoziomejDolnej(x, pos):
    'The two args are the value and tick position'
    return '%1i' % (x * 1e-3)


def formaterOsiPionowej(x, pos):
    'The two args are the value and tick position'
    return '%1i' % (x * 1e2)


# program właściwy
listaNazw = ['rsel.csv', 'cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv']
listaDanych = [[], [], [], [], []]
srednieWyniki = [[], [], [], [], []]
listaGier = [[], [], [], [], []]
listaPokolen = [[], [], [], [], []]
listaDoPrawego = []
# wczyt
for i in range(len(listaNazw)):
    with open(listaNazw[i], newline='') as file:
        myReader = csv.reader(file, delimiter=',')
        numerWiersza = -1
        for row in myReader:

            if numerWiersza < 0:
                numerWiersza += 1
                continue

            listaGier[i].append(float(row[1]))
            listaPokolen[i].append(int(row[0]))
            listaDanych[i].append([])
            for rzecz in row[2:]:
                listaDanych[i][numerWiersza].append(float(rzecz))
            numerWiersza += 1

for i in range(len(listaDanych)):
    for l in listaDanych[i]:
        srednieWyniki[i].append(srednia(l))
    listaDoPrawego.append(listaDanych[i][len(listaDanych[i]) - 1])

# koniec wczytu

# rozmiar
plt.figure(figsize=(10, 10))
plt.rc('text', usetex=True)
# dwa subploty ax1 i ax2, f niepotrzebne
f, (ax1, ax2) = plt.subplots(1, 2)

# Markery
markerStyles = ['o', 'v', 'D', 's', 'd']
lineColors = ["b", "g", "r", "k", "m"]
for i, j, s, c in zip(srednieWyniki, listaGier, markerStyles, lineColors):
    ax1.plot(j, i, c, linewidth=0.7, marker=s,
             markevery=25, markeredgewidth=0.5,
             markeredgecolor=(0, 0, 0, 1),
             markersize=5)

# Czcionka
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

listaNazwAlgorytmow = ["1-Evol-RS", "1-Coev-RS", "2-Coev-RS", "1-Coev", "2-Coev"]
# legenda
ax1.legend(listaNazwAlgorytmow, numpoints=2)

# Trzeba zrobić drugi plot w tym samym miejscu co pierwszy
ax11 = ax1.twiny()
ax11.plot(range(100), np.ones(100))  # Create a dummy plot
ax11.xaxis.set_ticks(np.arange(0, 201, 40))
ax11.set_xlim([0, 200])
ax11.set_xlabel('Pokolenie')
# ax11.cla()

# Oś x dolna
ax1.xaxis.set_ticks(np.arange(0, 500001, 100000))
ax1.set_xlim([0, 500000])
ax1.xaxis.set_major_formatter(FuncFormatter(formaterOsiPoziomejDolnej))

# Oś y
ax1.yaxis.set_ticks(np.arange(0.6, 2, 0.05))
ax1.set_ylim([0.6, 1])
ax1.yaxis.set_major_formatter(FuncFormatter(formaterOsiPionowej))

# Labelki
ax1.set_xlabel('Rozegranych gier (' + r'$\times$' + '1000)')

# procent w labelce%%%
ax1.set_ylabel("Odsetek wygranych gier[" + r'$\%$' + ']')

# siatka w tle
ax1.xaxis.grid(color='gray', linestyle=':')
ax1.yaxis.grid(color='gray', linestyle=':')
ax2.xaxis.grid(color='gray', linestyle=':')
ax2.yaxis.grid(color='gray', linestyle=':')

# PRawy
bp = ax2.boxplot(listaDoPrawego, notch=True, sym='+', showmeans=True)

# labele z rotacja
ax2.set_xticklabels(listaNazwAlgorytmow, rotation=20)

# oś y prawy
ax2.yaxis.tick_right()
ax2.set_ylim([0.6, 1])
ax2.yaxis.set_major_formatter(FuncFormatter(formaterOsiPionowej))

# kolory prawego

for i in bp['whiskers']:
    i.set(color='b', linestyle="-.")

for i in bp['means']:
    i.set(marker='o', markerfacecolor='b',  markeredgecolor='k', markersize=5)

for box, med in zip(bp['boxes'], bp['medians']):
    box.set(color='b', linewidth=1)
    med.set(color='r')

plt.show()
plt.close()
