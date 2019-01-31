# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 11:33:29 2019

@author: lytov
"""

import numpy as np
from NDT2D import NDT2D as NDT

# Generate some random, correlated data
points = np.random.multivariate_normal(mean=(1,1), cov=[[3, 4],[4, 7]], 
                                       size=100)
    
ndt = NDT()
ndt.setTargetCloud(points)

ndt.align(2)

input("\nPress Enter to continue...")
