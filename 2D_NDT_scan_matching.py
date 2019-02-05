# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 15:31:58 2019

@author: lytov
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from third_party.parser import parse
from cutter import cut

filepath = r'D:\workspace\python\NDT_Understanding\ndt_understanding\dataset\sick_dataset.txt'
scans = parse(filepath)

params = [[-25,0],[25, 50]]
cellSize = 2

nOS = 20

subcloud_x, subcloud_y, x_line, y_line = cut(scans[nOS,:], params, cellSize)

# цвета элипсов [sigma1, sigma2, sigma3]
colorEll = ['red', 'orange', 'blue']  

def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:,order]

parameters = []
for i in range(len(subcloud_x)):         

    x = np.asarray(subcloud_x[i])
    y = np.asarray(subcloud_y[i])
    
    cov = np.cov(x, y)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    parameters.append([cov,x_mean,y_mean])


# Отрисовка распределения в ячейках
ax = plt.subplot(111)

for i in range(len(parameters)):
    vals, vecs = eigsorted(parameters[i][0])
    theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))
    max_sigma = 2
    for y in range(1,max_sigma+1):
        print
        w, h = 2 * y * np.sqrt(vals)
        ell = Ellipse(xy=(parameters[i][1],parameters[i][2]),
                      width=w, height=h,
                      angle=theta, color = colorEll[y-1])
        ell.set_facecolor('none')
        ax.add_artist(ell)

ax.set_yticks(y_line, minor=False)
ax.yaxis.grid(True, which='major')

ax.set_xticks(x_line, minor=True)
ax.xaxis.grid(True, which='minor')      
 
X = scans[nOS,:,0].T
Y = scans[nOS,:,1].T
plt.scatter(X, Y)
plt.axis('equal')
plt.xlim(-25, 25)
plt.ylim(0, 50)
plt.gca().set_aspect('equal', adjustable='box')
#plt.grid(b=True, which='major', color='#666666', linestyle='-')

plt.show()
# Конец отрисовки