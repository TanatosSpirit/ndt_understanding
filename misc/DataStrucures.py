# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 18:34:20 2018

@author: lytov
"""

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

p1 = Point(10,3)
#print(p1.x,p1.y)

X = [0,  1,2,3.1,4,5.5,  6,8,9,9.1, 4.1,5.6,6.3,7,8.1,9.6,10.2]
Y = [0,1.4,2,  3,4,  5,6.3,8, 8.5, 9,    -1.1,-1.5,-1,-1.2,-1,-1.3,-1]

cloud = []
for i in range(len(X)):
    cloud.append(Point(X[i],Y[i]))
    
for i in range(len(cloud)):
    print(cloud[i].x, cloud[i].y)

#list (список)
carList = ['vaz', 'mazda', 'bmw']

print(carList[0])

#help(print)

print('Cars:', end=' ')
for car in carList:
    print(car, end=' ')
    
    
# пожалуй лучший способ для создания облака точек, пока количество измерений
# не больше трех :)
class AB(object):
    __slots__ = ('x', 'y')
    
cloudTest = []
point2d = AB()
point2d.x = 1
point2d.y = 2
print(point2d.x)
cloudTest.append(point2d)

point2d.x = 4
point2d.y = 3
print(point2d.y)
cloudTest.append(point2d)
print("cloudTest:" , cloudTest[1].y)

