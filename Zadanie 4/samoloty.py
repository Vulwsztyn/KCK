import threading

import imageio as imageio
from pylab import *
import skimage as ski
from skimage import data, io, filters, exposure
from skimage.filters import rank
from skimage import img_as_float, img_as_ubyte
from skimage.morphology import disk
import skimage.morphology as mp
from skimage import util
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from skimage.filters.edges import convolve
from matplotlib import pylab as plt
import numpy as np
from scipy import misc
from numpy import array
from IPython.display import display
from ipywidgets import interact, interactive, fixed
from ipywidgets import *
from ipykernel.pylab.backend_inline import flush_figures
from skimage import measure
from matplotlib import colors

warnings.simplefilter("ignore")


def wypelnijnazwy(lista):
    for i in range(21):
        a = ""
        if i < 10:
            a = "0"
        lista.append("samolot" + a + str(i) + ".jpg")


class myThread(threading.Thread):
    def __init__(self, threadID, fileName, axes):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.fileName = fileName
        self.axes = axes

    def run(self):
        obrobka(self.fileName, self.axes)


class showThread(threading.Thread):
    def __init__(self, threadID, ax, img, gray):
        threading.Thread.__init__(self)
        self.ax = ax
        self.ite = threadID
        self.img = img
        self.gray = gray
        self.threadID = threadID + 100

    def run(self):
        if self.gray:
            self.ax[self.ite].imshow(self.img, cmap='gray')
        else:
            self.ax[self.ite].imshow(self.img)


# def gamma(img):
#     g = np.mean(img) - 0.2
#     return (img ** g) ** g

def gamma(img):
    g = np.mean(img) - 0.27
    return (img ** g) ** g


def contrast(img):
    percmin = 0.3
    percmax = 2.0
    MIN = np.percentile(img, percmin)
    MAX = np.percentile(img, 100 - percmax)
    norm = (img - MIN) / (MAX - MIN)
    norm[norm > 1] = 1
    norm[norm < 0] = 0
    return norm


def threshold(img, nazwa):
    thr = np.percentile(img, 4)
    std = np.std(img)
    var = np.var(img)
    if std > 0.15 and var<std:
        thr += 0.2
    else:
        thr -= 0.1
    if std < 0.1: thr -= 0.2

    print(nazwa + " " + str(std) + " " + str(var))
    return img > thr


def dilation(img):
    return mp.erosion(img)


def erosion(img):
    return mp.dilation(img)


def threadPokazywania(ite, ax, img, gray, threads):
    thread = showThread(ite, ax, img, gray)
    thread.start()
    threads.append(thread)


def obrobka(imgName, ax):
    ite = 0
    threads = []
    img_org = data.imread(imgName, flatten=False)

    img = data.imread(imgName, flatten=True)

    threadPokazywania(ite, ax, img, True, threads)
    ite += 1

    img = gamma(img)

    threadPokazywania(ite, ax, img, True, threads)
    ite += 1

    img = contrast(img)

    threadPokazywania(ite, ax, img, True, threads)
    ite += 1

    img = threshold(img, imgName)

    threadPokazywania(ite, ax, img, True, threads)
    ite += 1

    for i in range(14):
        img = dilation(img)
        if i % 7 == 6:
            threadPokazywania(ite, ax, img, True, threads)
            ite += 1

    for i in range(1):
        img = erosion(img)

        threadPokazywania(ite, ax, img, True, threads)
    ite += 1

    contours = measure.find_contours(img, 0.5)

    ax[ite].imshow(img_org)

    for n, contour in enumerate(contours):
        if (len(contour) > 400):
            centroid = np.sum(contour, axis=0) / len(contour)
            q = np.random.uniform()
            c = colors.hsv_to_rgb([q, 1, 1])
            ax[ite].plot(contour[:, 1], contour[:, 0], linewidth=3, color=c)
            if (q > 0.5):
                q -= 0.5
            else:
                q += 0.5
            c = colors.hsv_to_rgb([q, 1, 1])
            ax[ite].plot(centroid[1], centroid[0], marker="o", color=c)

    for i in threads:
        i.join()


def wyswietl(nazwyPlikow):
    f, axes = plt.subplots(len(nazwyPlikow), len(nazwyPlikow), figsize=(200, 200))
    threads = []
    start_time = time.time()
    for i in range(len(nazwyPlikow)):
        thread = myThread(i, nazwyPlikow[i], axes[i])
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
    plt.savefig("samoloty.pdf")
    elapsed_time = time.time() - start_time
    print(elapsed_time)


if __name__ == '__main__':
    nazwyPlikow = []
    wypelnijnazwy(nazwyPlikow)
    wyswietl(nazwyPlikow)
