# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:41:57 2019

@author: lytov
"""
import numpy as np

class NDT2D:
    def setTargetCloud(self, target_cloud):
        self.target_cloud = target_cloud
    
    def setEpsilon(self):
        pass
    
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
    
    def transformTargetCloud(self):
        pass
    
    def allocateCellStructure(self):
        return self.target_cloud
        
    def align(self, init_guess):
        self.init_guess = init_guess
        mu = []
        sigma = [[],[]]
        cloud = self.allocateCellStructure()
        if len(cloud) > 2:
            mu, sigma = self.calcDistributionParameters(cloud)
        print("mu: ", mu, "\nsigma: ", sigma)
        self.transformTargetCloud()
        