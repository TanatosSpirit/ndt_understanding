# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 13:10:40 2019

@author: lytov
"""

import numpy as np

def det(sigma):
    return sigma[0][0]*sigma[1][1]-sigma[1][0]**2

def pdf(sigma, X, Y):
    detSigma = det(sigma)
    alfa = 1/(2*np.pi*np.sqrt(detSigma))
    betta = -1/(2*detSigma)
    return alfa * np.exp(betta*((sigma[0][0])*(X**2)+2*sigma[1][0]*X*Y+(sigma[1][1])*(Y**2)))
