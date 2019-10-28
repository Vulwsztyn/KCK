#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
# matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import kiwisolver

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    # rc('text', usetex=True)
    # rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.show()

def hsv2rgb(h, s, v):
    x=colors.hsv_to_rgb([h, s, v])
    return (x[0],x[1],x[2])

def gradient_rgb_bw(v):
    return (v,v,v)


def gradient_rgb_gbr(v):
    if(v<0.5):
        return (0,1-v*2, 2*v)
    v-=0.5
    return (v*2, 0, 1-v*2)

def gradient_rgb_gbr_full(v):
    if(v<0.25):
        return(0,1,v*4)
    if (v < 0.5):
        v-=0.25
        return (0, 1-v*4, 1)
    if (v < 0.75):
        v-=0.5
        return (v*4, 0, 1)
    v-=0.75
    return (1, 0, 1-v*4)


def gradient_rgb_wb_custom(v):
    x=1.0/7.0

    if (v < x):
        #111 to 101
        return (1, 1-v*7, 1)
    v -= x
    if (v < x):
        # 101 to 001
        return (1-v*7, 0, 1)
    v -= x
    if (v < x):
        # 001 to 011
        return (0, v*7, 1)
    v -= x
    if (v < x):
        # 011 to 010
        return (0, 1, 1-v*7)
    v -= x
    if (v < x):
        # 010 to 110
        return (v*7, 1,0)
    v -= x
    if (v < x):
        # 110 to 100
        return (1,1-v*7,0)
    # 100 to 000
    v -= x
    return (1-v*7, 0, 0)


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    return hsv2rgb(1/3+v*2/3, 1,1)

def gradient_hsv_unknown(v):
    return hsv2rgb(1/3-v/3,0.5,1)


def gradient_hsv_custom(v):
    return hsv2rgb(v, 1-v, 1)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])