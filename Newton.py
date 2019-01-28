# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 15:49:06 2019

@author: lytov
"""

import numpy as np
import PDF2d

def Newton(p0, eps, sigma, mu):
    p = p0
    for x in range(0, 6):
        g = PDF2d.gradPDF(sigma, mu, p)
        grad = np.array(g)
#        h = PDF2d.hessianPDF(sigma, mu, p)
        h = PDF2d.hessianPDFtrue(sigma, mu, p)
        hessian = np.array(h)
        hessianInv = np.linalg.inv(hessian)
        deltaP = - np.dot(hessianInv, grad)
        print("deltaP: ", deltaP)
        p = p + deltaP
        print("P: ", p)
    #    while n > 0:
    #        n //= 10  # это эквивалентно n = n // 10
    #        length += 1
    #    print(length)
    return p