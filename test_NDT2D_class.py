# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 11:33:29 2019

@author: lytov
"""

import numpy as np
from NDT2D import Ndt2D as NDT
import math
import matplotlib.pyplot as plt
from util.parser import parse

# Generate some random, correlated data
#points = np.random.multivariate_normal(mean=(1,1), cov=[[3, 4],[4, 7]], 
#                                       size=100)

filepath = r'D:\workspace\python\NDT_Understanding\ndt_understanding\dataset\sick_dataset.txt'
scans = parse(filepath)

PARAMS = {
        'L': 1,
        'xmin' : -25,
        'xmax' :  25,
        'ymin' :   0,
        'ymax' :  50
        }

#grids = makeOccupancyGrid(scans[1000],PARAMS)

nOS = 1000
next_nOS = nOS + 1
    
ndt = NDT()
ndt.set_maximum_iterations(50)
ndt.set_epsilon(1e-5)
ndt.set_resolution_grid(2)
ndt.set_target_cloud(scans[nOS])
ndt.set_source_cloud(scans[next_nOS])

init_guess = [0, 0, 0]
parameters = []
R, t, NI = ndt.align(init_guess)

print("R = ", R, "t = ", t, "NI = ", NI)
def transformation(R, t, scan):
    theta = R
    translate = np.array([t[0], t[1]])
    scanNp = np.array(scan)
    cosR = math.cos(theta)
    sinR = math.sin(theta)
    rotate = np.array([[cosR, -sinR], [sinR, cosR]])
    scanNp = np.dot(rotate, scanNp.T)
    for i in range(len(scanNp.T)):
        scanNp[:, i] = scanNp[:, i] + translate
    return scanNp

cloudAligned = transformation(R, t, scans[next_nOS])










###### Далее идет только отрисовка  ######
#        \/       \/         \/          #
      
# # цвета элипсов [sigma1, sigma2, sigma3]
# colorEll = ['red', 'orange', 'blue']
#
# def eigsorted(cov):
#     vals, vecs = np.linalg.eigh(cov)
#     order = vals.argsort()[::-1]
#     return vals[order], vecs[:,order]

# # Отрисовка распределения в ячейках
# ax = plt.subplot(111)

# for i in range(len(parameters)):
#     vals, vecs = eigsorted(parameters[i][0])
#     theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))
#     max_sigma = 2
#     for y in range(1,max_sigma+1):
#         print
#         w, h = 2 * y * np.sqrt(vals)
#         ell = Ellipse(xy=(parameters[i][1][0],parameters[i][1][1]),
#                       width=w, height=h,
#                       angle=theta, color = colorEll[y-1])
#         ell.set_facecolor('none')
#         ax.add_artist(ell)

# ax.set_yticks(y_line, minor=False)
# ax.yaxis.grid(True, which='major')
#
# ax.set_xticks(x_line, minor=True)
# ax.xaxis.grid(True, which='minor')
 
# #X = scans[nOS,:,0].T
# #Y = scans[nOS,:,1].T
# #plt.scatter(X, Y)
# X = scans[next_nOS,:,0].T
# Y = scans[next_nOS,:,1].T
# plt.scatter(X,Y,alpha=1.0, c='red')

# X = alignedCloud[0,:]
# Y = alignedCloud[1,:]
# plt.scatter(X,Y,alpha=0.5, c='black')
# plt.axis('equal')
# plt.xlim(-10, 15)
# plt.ylim(0, 24)
# plt.gca().set_aspect('equal', adjustable='box')
# #plt.grid(b=True, which='major', color='#666666', linestyle='-')

# plt.show()
# Конец отрисовки

# Plot the raw points...
x, y = scans[nOS].T
xR, yR = cloudAligned
plt.plot(x, y, 'ro', xR, yR, 'bo')
plt.show()

#input("\nPress Enter to continue...")
