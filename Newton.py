# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 15:49:06 2019

@author: lytov
"""

import numpy as np
import PDF2d
from numpy import linalg as LA

def Newton(p0, eps, sigma, mu):
    converged = False
    numberIter = 1
    gradNorm = 0
    p = p0
    g = PDF2d.gradPDF(sigma, mu, p)
    grad = np.array(g)
    gradNorm = LA.norm(grad)
    print("gradNorm: ", gradNorm)
    print("\n----- Number of iteration: ", numberIter, "-----")
    while not converged:
#        h = PDF2d.hessianPDF(sigma, mu, p)
        h = PDF2d.hessianPDFtrue(sigma, mu, p)
        hessian = np.array(h)
        hessianInv = np.linalg.inv(hessian)
        deltaP = - np.dot(hessianInv, grad)
        print("deltaP: ", deltaP)
        p = p + deltaP
        print("P: ", p)
        g = PDF2d.gradPDF(sigma, mu, p)
        grad = np.array(g)
        gradNorm = LA.norm(grad)
        print("gradNorm: ", gradNorm)
        if gradNorm < eps:
            print("\nConverged!")
            print("Spent iterations: ", numberIter)
            converged = True
        else:
            numberIter += 1
            print("\n----- Number of iteration: ", numberIter, "-----")
    return p