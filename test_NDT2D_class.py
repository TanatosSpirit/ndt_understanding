# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 11:33:29 2019

@author: lytov
"""

import numpy as np
from NDT2D import NDT2D as NDT
import math
import matplotlib.pyplot as plt

# Generate some random, correlated data
points = np.random.multivariate_normal(mean=(1,1), cov=[[3, 4],[4, 7]], 
                                       size=100)
    
ndt = NDT()
ndt.setEpsilon(1e-2)
ndt.setResolutionGrid(1)
ndt.setTargetCloud(points)
ndt.setSourceCloud(points)

init_guess = [2, 2, 0 ]
ndt.align(init_guess)



## Plot the raw points...
#x, y = points.T
#xR, yR = ndt.filtered_cloud
#plt.plot(x, y, 'ro', xR, yR, 'bo')
#plt.show()

#input("\nPress Enter to continue...")
