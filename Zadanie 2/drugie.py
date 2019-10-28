# Trochę magii
from sympy.interactive import printing
printing.init_printing(use_latex=True)

from __future__ import division
import sympy as sym
from sympy import *

# Definicje zmiennych
x, y, z = symbols("x y z")
k = Symbol("k", integer=True)
f = Function('f')