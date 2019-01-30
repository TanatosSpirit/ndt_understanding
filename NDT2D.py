# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:41:57 2019

@author: lytov
"""

class NDT2D:
    def __init__(self, cloudRef):
        self.reference_scan = cloudRef
    
    def setTargetCloud(self, cloudTarget, initGuess):
        self.target_scan = cloudTarget
        self.init_guess = initGuess
    
    def calcDistributionParameters(self, cloudRef):
        sigma = [[0,0],[0,0]]
        mu = [0,0]
        return sigma, mu
    
    def transformTargetCloud(self):
        pass
    
    def calcNormalDistributionValue(self, targetPoint):
        pass
    
    def align(self):
        pass