# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 14:48:11 2019

@author: lytov
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

import PDF2d
import Newton

fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
mu_1 = 0.
mu_2 = 0.
mu = [mu_1, mu_2] 
sigma_1 = 8. 
sigma_2 = 4.
sigma_12 = 1.
sigma = [[sigma_1, sigma_12],
         [sigma_12, sigma_2]]
X = np.arange(-5, 5, 0.1)
Y = np.arange(-5, 5, 0.1)

X, Y = np.meshgrid(X, Y)

Z = PDF2d.pdf(sigma, mu, X, Y)

#Test of grad
##print("sigma: ", sigma)
#p = [-1.,-2.]
#print(PDF2d.gradPDF(sigma, mu, p))
#h = PDF2d.hessianPDFtrue(sigma, mu, p)
#print("H: ", h)

#t1 = np.arange(-2.0, 2.0, 0.1)
#t2 = np.zeros(t1.size)
#value = []
#for i in range(t1.size):
#    p = [t1[i], t2[i]]
#    t = PDF2d.gradPDF(sigma, mu, p)
#    value.append(t[0])
#print(t1)

#plt.figure(1)
#plt.subplot(211)
#plt.plot(t1, value, 'r--')


#Example of Newton's algorithm
p = [-1.2, 1.3]
eps = 1e-3
print("Init guess: ", p)
p = Newton.Newton(p, eps, sigma, mu)
print("Solution ", p)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.1, 1.1)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
