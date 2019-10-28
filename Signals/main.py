import glob
listaPlikow = glob.glob("./trainall/*.wav")
listaPoprawnych = []
for i in range(len(listaPlikow)):
    listaPlikow[i]=listaPlikow[i][2:]
    listaPlikow[i]=listaPlikow[i].replace('\\','/')
    listaPoprawnych.append(listaPlikow[i][-5])
print(listaPlikow)
print(listaPoprawnych)