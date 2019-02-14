# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 15:33:30 2019

@author: lytov
"""

from numpy import *
from math import sqrt, acos, pi
import matplotlib.pyplot as plt

# Input: expects Nx3 matrix of points
# Returns R,t
# R = 3x3 rotation matrix
# t = 3x1 column vector

def rigid_transform_3D(A, B):
    assert len(A) == len(B)

    N = A.shape[0]; # total points
    print("total points: ", N)

    centroid_A = mean(A, axis=0)
    centroid_B = mean(B, axis=0)
    print("centroid_A: ", centroid_A)
    print("centroid_B: ", centroid_B)
    
    # centre the points
    AA = A - tile(centroid_A, (N, 1))
    BB = B - tile(centroid_B, (N, 1))
    print("centre the points A: \n", AA)

    # dot is matrix multiplication for array
    H = transpose(AA) * BB
    print("H: \n", H)

    U, S, Vt = linalg.svd(H)

    R = Vt.T * U.T

    # special reflection case
    if linalg.det(R) < 0:
       print("Reflection detected")
       Vt[2,:] *= -1
       R = Vt.T * U.T

    t = -R*centroid_A.T + centroid_B.T

    return R, t

# Test with random data

# Random rotation and translation
#R = mat(random.rand(3,3))
#t = mat(random.rand(3,1))
R = mat(random.rand(2,2))
t = mat(random.rand(2,1))

# make R a proper rotation matrix, force orthonormal
U, S, Vt = linalg.svd(R)
R = U*Vt

# remove reflection
if linalg.det(R) < 0:
#   Vt[2,:] *= -1
   Vt[1,:] *= -1
   R = U*Vt

# number of points
n = 10

#A = mat(random.rand(n,3));
A = mat(random.rand(n,2));
B = R*A.T + tile(t, (1, n))
B = B.T;
B[0,0] = B[0,0] + 0.1
B[1,1] = B[1,1] + 0.1

# recover the transformation
ret_R, ret_t = rigid_transform_3D(A, B)

A2 = (ret_R*A.T) + tile(ret_t, (1, n))
A2 = A2.T

# Find the error
err = A2 - B

err = multiply(err, err)
err = sum(err)
rmse = sqrt(err/n);

print("Points A")
print( A)
print( "")

print("Points B")
print(B)
print ("")

print( "Rotation")
print( R)
print( "")

print("Valid angle")
print((acos(R[0,0])/pi)*180)
print("")

print("Calculated angle")
print((acos(ret_R[0,0])/pi)*180)
print("")

print( "Translation")
print( t)
print ("")

print ("RMSE:", rmse)
print ("If RMSE is near zero, the function is correct!")

fig, ax = plt.subplots()
ax.plot(A[:,0], A[:,1], 'ro', B[:,0], B[:,1], 'bo')

plt.show()
