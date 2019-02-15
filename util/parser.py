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
        if scan[i] < 51.:
            p[0] = scan[i] * math.cos(i*math.pi/180)
            p[1] = scan[i] * math.sin(i*math.pi/180)
            scanEucl.append(p)
    return scanEucl

def parse_lidar_log(path):
    scanRaw = []
    with open(path) as fp:  
       line = fp.readline()
       while line:
           singleScan = [float(x) for x in line.split()]
           scanRaw.append(singleScan)
           line = fp.readline()
           
    scanTemp = []
    for i in range(len(scanRaw)):
        scanTemp.append(spherical2Euclidean(scanRaw[i][:]))
    return scanTemp


def parse_odometry_log(path):
    odo_raw = []
    with open(path) as fp:
        line = fp.readline()
        while line:
            odo_line = [float(x) for x in line.split()]
            odo_raw.append(odo_line)
            line = fp.readline()

    return odo_raw

def main(lidar_log, odometry_log):
    scanXY = parse_lidar_log(lidar_log)
    odometry = parse_odometry_log(odometry_log)
    print(odometry)
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
        scanForPlot = np.array(scanXY[i])
        x, y = scanForPlot.T
        line.set_data(x, y)
        return line,

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(scanXY), interval=50, blit=True)
    #anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    
    plt.show()

if __name__ == '__main__':
    lidar_log = r'D:\workspace\python\NDT_Understanding\ndt_understanding\dataset\sick_dataset.txt'
    odometry_log = r'D:\workspace\python\NDT_Understanding\ndt_understanding\dataset\dataset_edmonton.rawlog_ODO.txt'
    main(lidar_log, odometry_log)
    