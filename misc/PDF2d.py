# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 13:10:40 2019

@author: lytov
"""

import numpy as np
from scipy.misc import derivative

def det(sigma):
    return sigma[0][0]*sigma[1][1]-sigma[1][0]**2

def norm(detSigma):
    return 1/(2*np.pi*np.sqrt(detSigma))

def coef(detSigma):
    return -1/(2*detSigma)

def expr(sigma, mu, X, Y):
    return ((sigma[0][0])*((X-mu[0])**2)+
            2*sigma[1][0]*(X-mu[0])*(Y-mu[1])+
            (sigma[1][1])*((Y-mu[1])**2))
    
def exprdx(sigma, mu, x, y):
    return 2*sigma[0][0]*(x-mu[0]) + 2*sigma[1][0]*(y-mu[1])

def exprdy(sigma, mu, x, y):
    return 2*sigma[1][0]*(x-mu[0]) + 2*sigma[1][1]*(y-mu[1])

def pdf(sigma, mu, X, Y):
    detSigma = det(sigma)
    alfa = norm(detSigma)
    betta = coef(detSigma)
    expression = expr(sigma, mu, X, Y)
    return alfa * np.exp(betta*expression)

def gradPDF(sigma, mu, p):
    x = p[0]
    y = p[1]
    detSigma = det(sigma)
    alfa = norm(detSigma)
    betta = coef(detSigma)
    ex = expr(sigma, mu, x, y)
    exdx = exprdx(sigma, mu, x, y)
    exdy = exprdy(sigma, mu, x, y)
    dfdx = alfa * betta * np.exp(betta*ex) * exdx
    dfdy = alfa * betta * np.exp(betta*ex) * exdy
    grad = [dfdx, dfdy]
    return grad

def hessianPDF(sigma, mu, p):
    x = p[0]
    y = p[1]
    detSigma = det(sigma)
    alfa = norm(detSigma)
    betta = coef(detSigma)
    ex = expr(sigma, mu, x, y)
    exdx = exprdx(sigma, mu, x, y)
    exdy = exprdy(sigma, mu, x, y)
    ddfdxx = alfa * betta**2 * np.exp(betta*ex) * 2*sigma[0][0] * exdx
    ddfdxy = alfa * betta**2 * np.exp(betta*ex) * 2*sigma[1][0] * exdy
    ddfdyy = alfa * betta**2 * np.exp(betta*ex) * 2*sigma[1][1] * exdy
    ddfdyx = alfa * betta**2 * np.exp(betta*ex) * 2*sigma[1][0] * exdx
    hessian = [[ddfdxx, ddfdxy], [ddfdyx, ddfdyy]]
    return hessian

def fdx(x, y, sigma, mu):
    detSigma = det(sigma)
    alfa = norm(detSigma)
    betta = coef(detSigma)
    expression = expr(sigma, mu, x, y)
    exdx = exprdx(sigma, mu, x, y)
    return(alfa * betta * np.exp(betta*expression)*exdx) 

def fdy(x, y, sigma, mu):
    detSigma = det(sigma)
    alfa = norm(detSigma)
    betta = coef(detSigma)
    expression = expr(sigma, mu, x, y)
    exdy = exprdy(sigma, mu, x, y)
    return(alfa * betta * np.exp(betta*expression)*exdy) 

def partial_derivative(func, var=0, point=[]):
    args = point[:]
    def wraps(x):
        args[var] = x
        return func(*args)
    return derivative(wraps, point[var], dx = 1e-6, n=1)

def hessianPDFtrue(sigma, mu, p):
    initPos = [p[0], p[1], sigma, mu]
    h11 = partial_derivative(fdx, 0, initPos)
    h12 = partial_derivative(fdx, 1, initPos)
    h21 = partial_derivative(fdy, 0, initPos)
    h22 = partial_derivative(fdy, 1, initPos)
    return [[h11, h12], [h21, h22]]
