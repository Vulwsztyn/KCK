import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import csv

lista=[]
with open("132289_WD.csv", newline='') as file:
    myReader = csv.reader(file, delimiter=',')
    for row in myReader:
        lista.append(row)
for i in range(len(lista)):
    lista[i][1]=float(lista[i][1])
    for j in range(2,7):
        lista[i][j] = int(lista[i][j])

for i in lista:
    print(i)
print("DEBUG")
for i in lista:
    for j in lista:
        if i[1]<j[1] and i[2]>j[2] and i[3]>j[3] and i[4]<j[4] and i[5]>j[5] and i[6]<j[6]:
            print(i,j)
miny=[0,289.88,16,45,540,3,0]
maxy=[1,1079.2,85,68,3429,12,3]
zyski=[0,0,1,1,0,1,0]
wagi=[0,7,8,6,5,3,2]
maxv=20
minv=20
for i in lista:
    value=0
    for j in range(1,len(i)):
        if zyski[j]==1:
            value+=wagi[j]*(i[j]-miny[j])/(maxy[j]-miny[j])
        else:
            value += wagi[j] * (maxy[j]-i[j]) / (maxy[j] - miny[j])
    i.append(value)
    if value>maxv:
        maxv=value
    if value<minv:
        minv=value
for i in sorted(lista, key=lambda rzecz: rzecz[7]) :
    print(i)
print(maxv,minv)
