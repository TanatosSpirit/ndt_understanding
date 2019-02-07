# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:41:57 2019

@author: lytov
"""
import numpy as np
import math
from Newton import Newton

class NDT2D:
    def __init__(self):
        self.filtered_cloud = np.zeros((2, 1))
        self.epsilon = 1.
        self.resolution = 0
        
    def setTargetCloud(self, target_cloud):
        self.target_cloud = target_cloud
    
    def setSourceCloud(self, filtered_cloud):
        self.filtered_cloud = filtered_cloud
    
    def setEpsilon(self, eps):
        self.epsilon = eps
    
    def setResolutionGrid(self, resolution):
        self.resolution = resolution
        
    def setStepSize(self):
        pass
    
    def setMaximumIterations(self, maxIter):
        self.maxIter = maxIter
    
    def hasConverged(self):
        pass
    
    def getFitnessScore(self):
        pass
    
    def getFinalTransformation(self):
        pass
    
    def getSourceCloud(self):
        return self.filtered_cloud
    
    def calcDistributionParameters(self, cloud):
        sigma = np.cov(cloud)
        mu = np.mean(cloud, axis=1)
        
        return mu, sigma
    
    def transformFilteredCloud(self):
        theta = self.init_guess[2]
        translate = np.array([self.init_guess[0],self.init_guess[1]])
        
        cosR = math.cos(theta)
        sinR = math.sin(theta)
        rotate = np.array([[cosR, -sinR], [sinR, cosR]])
        self.filtered_cloud = np.dot(rotate, self.filtered_cloud.T)
        for i in range(len(self.filtered_cloud.T)):
            self.filtered_cloud[:,i] = self.filtered_cloud[:,i] + translate
        
    def allocateCellStructure(self):
        #Границы скана определяются параметрами лидара
        x_min, x_max, y_min, y_max = -25, 25, 0, 50
        cellSize = self.resolution
        
        # остаток от деления на размер блока
        x_remainder = x_range % cellSize
        y_remainder = y_range % cellSize
        
        x_parts, y_parts = 0, 0
        x_parts = x_range // cellSize
        y_parts = y_range // cellSize
        if x_remainder!=0: 
            x_parts = x_parts + 1
        if y_remainder!=0: 
            y_parts = y_parts + 1
       
        # списки координат линий сетки на которую будет разделено облако
        x_line = []
        for xi in range(int(x_parts)+1):
            x_line.append(x_min+(cellSize*(xi)))
        y_line = []
        for yi in range(int(y_parts)+1):
            y_line.append(y_min+(cellSize*(yi)))
            
        # пробегаем по всему облаку точек и формируем облако точек соотвествующее
        #    определенной ячейке 
        subcloud_x = []
        subcloud_y = []
        borderOfCell = []
        for xi in range(int(x_parts)):
    #        print("xi: ", xi)
            for yi in range(int(y_parts)):
    #            print("yi: ", yi)
                cloud_sub_x = []
                cloud_sub_y = []
                borders = [[x_min+(cellSize*(xi)), x_min+(cellSize*(xi+1))],
                           [y_min+(cellSize*(yi)), y_min+(cellSize*(yi+1))]]
                for i in range(len(self.target_cloud)):
                    x_temp = self.target_cloud[i,0]
                    y_temp = self.target_cloud[i,1]
                    if x_temp >= borders[0][0] and x_temp < borders[0][1]:
                        if y_temp >= borders[1][0] and y_temp < borders[1][1]: 
    #                        print("Point(", i, "): X =", x_temp, "; Y=", y_temp)
                            cloud_sub_x.append(x_temp)
                            cloud_sub_y.append(y_temp)
    #            print("Len_cloud_sub: ", len(cloud_sub_x))
                if len(cloud_sub_x) > 2:
                    borderOfCell.append(borders)
                    subcloud_x.append(cloud_sub_x)
                    subcloud_y.append(cloud_sub_y)
    #    cuttedScan = [subcloud_x, subcloud_x]   
#        print("borderOfCell: ", borderOfCell)
            
        return subcloud_x, subcloud_y, x_line, y_line, borderOfCell
        
    def align(self, init_guess):
        #Initialisation
        x0 = init_guess[0]
        y0 = init_guess[1]
        yaw0 = init_guess[3]
        
        original_p = [x0, y0, yaw0]
        
        p = original_p
        
        x_min, x_max, y_min, y_max = -25, 25, 0, 50
        cellSize = self.resolution
        
        # ширина и длина облака точек
        x_range = abs(x_min) + abs(x_max)
        y_range = abs(y_min) + abs(y_max)
        
        NX = x_range // cellSize
        NY = y_range // cellSize
        
        mu = []
        sigma = [[],[]]
        subcloud_x, subcloud_y, x_line, y_line , borderOfCell= self.allocateCellStructure()
        parametres = []
        for i in range(len(subcloud_x)):
            cloud = np.array([subcloud_x[i], subcloud_y[i]])
            mu, sigma = self.calcDistributionParameters(cloud)
            parametres.append([sigma, mu])
#            print("mu: ", mu, "\nsigma: ", sigma)
        
        #Registration
        self.init_guess = init_guess
#        score = 0
#        g = [0,0]
#        H = [[0,0], [0,0]]
        self.transformFilteredCloud()
        for i in range(len(self.filtered_cloud[0,:])):
            x_temp = self.filtered_cloud[0][i]
            y_temp = self.filtered_cloud[1][i]
            for bi in range(len(borderOfCell)):
                if x_temp >= borderOfCell[bi][0][0] and x_temp < borderOfCell[bi][0][1]:
                    if y_temp >= borderOfCell[bi][1][0] and y_temp < borderOfCell[bi][1][1]:
                        sigma = parametres[bi][0]
                        mu = parametres[bi][1]
                        self.filtered_cloud[:,i] = Newton(self.filtered_cloud[:,i], self.epsilon, sigma, mu, True)
                        print("")
        return parametres, x_line, y_line
            
       
        
        