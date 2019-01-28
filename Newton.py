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
    print("\n----- Number of iteration: ", numberIter, "-----")
    print("gradNorm: ", gradNorm)
    while not converged:
#        h = PDF2d.hessianPDF(sigma, mu, p)
        h = PDF2d.hessianPDFtrue(sigma, mu, p)
        hessian = np.array(h)
        hessianInv = np.linalg.inv(hessian)
        deltaP = - np.dot(hessianInv, grad)
        print("deltaP: ", deltaP)
        p = p + deltaP
        print("P: ", p)
        numberIter += 1
        print("\n----- Number of iteration: ", numberIter, "-----")
        print("gradNorm: ", gradNorm)
        g = PDF2d.gradPDF(sigma, mu, p)
        grad = np.array(g)
        gradNorm = LA.norm(grad)
        if gradNorm < eps:
            print("Converged!")
            print("Number of iteration: ", numberIter)
            converged = True
    #    while n > 0:
    #        n //= 10  # это эквивалентно n = n // 10
    #        length += 1
    #    print(length)
    return p