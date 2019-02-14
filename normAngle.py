# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 13:38:08 2019

@author: lytov
"""

import math

def normAngle(angle):
    # Normalize an angle in the range [-pi/2;pi/2]

    out = angle + 2*math.pi*((math.pi-angle)//(2*math.pi))

    return out