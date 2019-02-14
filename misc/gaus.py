# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 21:34:47 2018

@author: lytov
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:,order]

# не работает чет
#class point_t(object):
#    __slots__ = ('x', 'y')
    
class Point_t:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init
        
# dataset 
X = [0,  1,2,3.1,4,5.5,  6,8,9,9.1, 4.1,5.6,6.3,7,8.1,9.6,10.2]
Y = [0,1.4,2,  3,4,  5,6.3,8, 8.5, 9,    -1.1,-1.5,-1,-1.2,-1,-1.3,-1] 
       
def cloudCreator(X,Y):
    #cloud = [X, Y] 
    #point = point_t()
    cloud = []
    for i in range(len(X)):
        #    point.x = X[i]
        #    point.y = Y[i]
        #    cloud.append(point)
        cloud.append(Point_t(X[i],Y[i]))
        #    print("POINT[",i,"]: ", point.x, point.y)
        print("cloud[",i,"]: ", cloud[i].x, cloud[i].y)
    return cloud

cloud = cloudCreator(X,Y)

# цвета элипсов [sigma1, sigma2, sigma3]
colorEll = ['red', 'orange', 'blue']  

print("Number of points: " , len(cloud))
#subdividing
x_min, x_max = min(X), max(X)
y_min, y_max = min(Y), max(Y)
print("x_min: ",x_min,"; x_max: ", x_max)
print("y_min: ",y_min,"; y_max: ", y_max)

# Параметр по которому происходит разбиение облака точек (в метрах)
divider = 4

# ширина и длина облака точек
x_range = abs(x_min) + abs(x_max)
y_range = abs(y_min) + abs(y_max)
print("x_range: ",x_range,"; y_range: ", y_range)

# остаток от деления на размер блока
x_remainder = x_range % divider
y_remainder = y_range % divider

print("x_remainder: ",x_remainder)
print("y_remainder: ",y_remainder)

# количество блоков по X и Y размером divider
if x_remainder!=0: 
    x_parts = (x_range // divider) + 1
if y_remainder!=0: 
    y_parts = (y_range // divider) + 1
    
print("x_parts:",x_parts, "y_parts", y_parts)

#X_divided = [[1,2],
#             [3,4]]
#print(X_divided[1][1])


ax = plt.subplot(111)

# списки координат линий сетки на которую будет разделено облако
x_line = []
for xi in range(int(x_parts)+1):
    x_line.append(x_min+(divider*(xi)))
y_line = []
for yi in range(int(y_parts)+1):
    y_line.append(y_min+(divider*(yi)))
    
# пробегаем по всему облаку точек и формируем облако точек соотвествующее
#    определенной ячейке 
subcloud_x = []
subcloud_y = []
for xi in range(int(x_parts)):
    print("xi: ", xi)
    for yi in range(int(y_parts)):
        print("yi: ", yi)
        cloud_sub_x = []
        cloud_sub_y = []
        for i in range(len(cloud)):
            x_temp = cloud[i].x
            #print("x_temp ", x_temp)
            y_temp = cloud[i].y
            if x_temp >= x_min+(divider*(xi)) and x_temp < x_min+(divider*(xi+1)):
                if y_temp >= y_min+(divider*(yi)) and y_temp < y_min+(divider*(yi+1)): 
                    print("Point(", i, "): X =", x_temp, "; Y=", y_temp)
                    cloud_sub_x.append(x_temp)
                    cloud_sub_y.append(y_temp)
        print("Len_cloud_sub: ", len(cloud_sub_x))
        if len(cloud_sub_x) > 2:
            subcloud_x.append(cloud_sub_x)
            subcloud_y.append(cloud_sub_y)
        
        
parameters = []
for i in range(len(subcloud_x)):         

    x = np.asarray(subcloud_x[i])
    y = np.asarray(subcloud_y[i])
    
    cov = np.cov(x, y)
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    parameters.append([cov,x_mean,y_mean])
    
for i in range(len(parameters)):
    vals, vecs = eigsorted(parameters[i][0])
    theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))
    max_sigma = 2
    for y in range(1,max_sigma+1):
        print
        w, h = 2 * y * np.sqrt(vals)
        ell = Ellipse(xy=(parameters[i][1],parameters[i][2]),
                      width=w, height=h,
                      angle=theta, color = colorEll[y-1])
        ell.set_facecolor('none')
        ax.add_artist(ell)


print("subcloud ",cloud_sub_x, cloud_sub_y) 

ax.set_yticks(y_line, minor=False)
ax.yaxis.grid(True, which='major')

ax.set_xticks(x_line, minor=True)
ax.xaxis.grid(True, which='minor')       

plt.scatter(X, Y)
plt.axis('equal')
plt.xlim(-3, 13)
plt.ylim(-4, 13)
plt.gca().set_aspect('equal', adjustable='box')
#plt.grid(b=True, which='major', color='#666666', linestyle='-')

plt.show()