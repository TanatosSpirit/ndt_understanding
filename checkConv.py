# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:50:05 2019

@author: lytov
"""

import math
import numpy as np

def checkConv(err, t):
    #   Given an input of values consevutive representing error function outputs, returns % whether the function is
    # converging.The convergence tolerance is given as input
    out = False

    niterconv = 3       # minimum number of iterations before convergence check
    convalue = 0.00001             # below this value the result is acceptable


    if len(err) > 0:  # err = [x1, x2, ... , xn]

        dt = []
        for i in range(len(t)):     # t = [[x1, y1, yaw1],
                                    #      [x2, y2, yaw2]]
            tmp = math.sqrt(pow(t[i][0], 2) + pow(t[i][1], 2))
            dt.append(tmp)

        dth = []
        for i in range(len(t)):
            dth.append(t[i][2])

        errNp = np.array(err)    # is it possible to improve?!
        dtNp = np.array(dt)
        dthNp = np.array(dth)

        if len(err) >= niterconv and (np.std(errNp) < convalue or np.std(dtNp) < convalue*10 and np.std(dthNp) < convalue*10):
            out = True


    return out
