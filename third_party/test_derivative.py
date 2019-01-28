# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 13:07:52 2019

@author: lytov
"""

from scipy.misc import derivative
import numpy as np

def foo(x, y, sigma):
    print(sigma)
    return(0.0918 * -0.166 * np.exp((-0.166)*
                                    (2.0*x**2 + 2*1.0*x*y + 2.0*y**2)) *
                                    (2*2*x + 2*1*y)) 

def partial_derivative(func, var=0, point=[]):
    args = point[:]
    def wraps(x):
        args[var] = x
        return func(*args)
    return derivative(wraps, point[var], dx = 1e-6, n=1)

sigma= [[1,2],[3,4]]
p = [0.,-2., sigma]
print(partial_derivative(foo, 0, p))
print(partial_derivative(foo, 1, p))
