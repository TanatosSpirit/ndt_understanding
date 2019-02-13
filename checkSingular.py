# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 16:04:02 2019

@author: lytov
"""
import numpy as np
def checkSingular(A):
    #   Check if a matrix is singular by comparing its eigen values.
    # If the smallest eigenvalue must be at least 0.001 times the biggest one.
    
    # WARNING, vals can also be singular.......
    
    cov = np.array(A)
    vals, vecs = np.linalg.eigh(cov)
    
    # emin = min(vecs.diagonal())
    # emax = max(vecs.diagonal())
    emin = min(vals)
    emax = max(vals)
    
    out = 0
    
    if emin/emax < 0.001:
        # in this case the matrix is singular
        out = 1
    else:
        return out, cov
    
    # we want to se the smallest eigen values to be 0.001 times the biggest one
    while emin/emax < 0.001:
        
        I = np.identity(2)
        cov = cov + I * 0.0001

        vals, vecs = np.linalg.eigh(cov)
    
        # emin = min(vecs.diagonal())
        # emax = max(vecs.diagonal())
        emin = min(vals)
        emax = max(vals)
        
    return out, cov
    