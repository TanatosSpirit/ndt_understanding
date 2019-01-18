# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 16:45:20 2018

@author: lytov
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


ax = plt.subplot(111)

w = 1.0
h = 2.0
a = -45

ell = Ellipse(xy=(0.0, 0.0), 
              width=w, height=h, 
              angle=a, color='blue')
ell.set_facecolor('none')
ax.add_artist(ell)
ell = Ellipse(xy=(0.0, 0.0), 
              width=w+0.5, height=h+0.5, 
              angle=a, color='red')
ell.set_facecolor('none')
ax.add_artist(ell) 

plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
