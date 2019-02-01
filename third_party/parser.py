# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:06:38 2019

@author: lytov
"""
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib import animation


def spherical2Euclidean(scan):
    scanEucl = []
    for i in range(len(scan)):
        p = [0,0]
        p[0] = scan[i] * math.cos(i*math.pi/180)
        p[1] = scan[i] * math.sin(i*math.pi/180)
        scanEucl.append(p)
    return scanEucl

filepath = r'D:\workspace\python\NDT_Understanding\ndt_understanding\dataset\sick_dataset.txt'  

scanRaw = []
with open(filepath) as fp:  
   line = fp.readline()
   while line:
       singleScan = [float(x) for x in line.split()]
       scanRaw.append(singleScan)
       line = fp.readline()
       
scanNp = np.array(scanRaw)

print(len(scanNp[2000,:]))

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure(figsize=(10,10))
#plt.gca().set_aspect('equal', adjustable='box')
ax = plt.axes(xlim=(-35, 35), ylim=(0, 70))
line, = ax.plot([], [],'ro')

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    scanRange = spherical2Euclidean(scanNp[i,:])
    scanForPlot = np.array(scanRange)
    x, y = scanForPlot.T
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(scanNp[:,0]), interval=20, blit=True)

anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
