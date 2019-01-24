# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 20:21:03 2018

@author: lytov
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:,order]

mean = [0, 0]
cov = [[2, -1], [-1, 2]]

x, y = np.random.multivariate_normal(mean, cov, 100).T

ax = plt.subplot(111)

nstd = 1
cov = np.cov(x, y)
print("cov: ", cov)
vals, vecs = eigsorted(cov)
theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))

w, h = 2 * nstd * np.sqrt(vals)
ell = Ellipse(xy=(np.mean(x), np.mean(y)),
              width=w, height=h,
              angle=theta, color='red')
ell.set_facecolor('none')
ax.add_artist(ell) 

nstd = 2
w, h = 2 * nstd * np.sqrt(vals)
ell = Ellipse(xy=(np.mean(x), np.mean(y)),
              width=w, height=h,
              angle=theta, color='orange')
ell.set_facecolor('none')
ax.add_artist(ell)

nstd = 3
w, h = 2 * nstd * np.sqrt(vals)
ell = Ellipse(xy=(np.mean(x), np.mean(y)),
              width=w, height=h,
              angle=theta, color='blue')
ell.set_facecolor('none')
ax.add_artist(ell)
            
plt.plot(x, y, 'x', alpha = 0.2)

plt.axis('equal')
plt.show()