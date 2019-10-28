#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division  # Division in Python 2.7
import matplotlib
# matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from matplotlib import colors


def toCos(a, b):
    return a.dot(b.T) / np.linalg.norm(a) / np.linalg.norm(b)


def toAngle(a, b):
    return np.arccos(toCos(a, b))


def normalize(a):
    dlugosc = np.linalg.norm(a)
    for i in range(len(a)):
        a[i] /= dlugosc
    return a


if __name__ == '__main__':
    dane = np.loadtxt("big.dem", delimiter=" ", usecols=range(500))
    # print(min(dane))
    # print(max(dane))
    print(len(dane))
    minH = 0
    maxH = 0
    for k in dane:
        if minH == maxH == 0:
            minH = maxH = k[0]
        tempMin = min(k)
        tempMax = max(k)
        if tempMax > maxH:
            maxH = tempMax
        elif minH > tempMin:
            minH = tempMin
    difH = maxH - minH
    colorMap = []
    i = 0
    minKat = 1e6
    maxKat = -1e6
    minD = 1e10
    maxD = -1e10
    for k in dane:
        colorMap.append([])
        j = 0
        for l in k:

            if True or 70 < i < 250 and 120 < j < 320:
                hue = (maxH - l) / difH / 3
                sat = 1
                value = 1
                if 0 < i < 499 and 0 < j < 499:
                    odl = 20  # 75.37
                    pra = np.array([odl, 0, -dane[i][j] + dane[i][j + 1]])
                    lew = np.array([-odl, 0, -dane[i][j] + dane[i][j - 1]])
                    gor = np.array([0, odl, -dane[i][j] + dane[i - 1][j]])
                    dol = np.array([0, -odl, -dane[i][j] + dane[i + 1][j]])
                    nor = np.cross(lew, gor) + np.cross(gor, pra) + np.cross(pra, dol) + np.cross(dol, lew)
                    vecSlo = np.array([0, -0.447214, -0.894427])
                    kat = toCos(nor, vecSlo)

                    q = 0.5
                    if kat < 0.93:

                        value = kat ** 1.5
                    else:

                        s = q
                        sat = (1 - kat) / 0.07
                colorMap[i].append(colors.hsv_to_rgb((hue, sat, value)))
            else:
                colorMap[i].append((0, 0, 0))
            j += 1
        i += 1

    fig, ax = plt.subplots()
    plt.imshow(colorMap)
    plt.show()
