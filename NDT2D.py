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
    
    def calcDistributionParameters(self, cloud):
        sigma = np.cov(cloud.T)
        mu = np.mean(cloud, axis=0)
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
        return self.target_cloud
        
    def align(self, init_guess):
        #Initialisation
        mu = []
        sigma = [[],[]]
        cloud = self.allocateCellStructure()
        if len(cloud) > 2:
            mu, sigma = self.calcDistributionParameters(cloud)
        print("mu: ", mu, "\nsigma: ", sigma)
        
        #Registration
        self.init_guess = init_guess
#        score = 0
#        g = [0,0]
#        H = [[0,0], [0,0]]
        self.transformFilteredCloud()
        for i in range(len(self.filtered_cloud[0,:])):
            self.filtered_cloud[:,i] = Newton(self.filtered_cloud[:,i], self.epsilon, sigma, mu, True)
            
            
       
        
        