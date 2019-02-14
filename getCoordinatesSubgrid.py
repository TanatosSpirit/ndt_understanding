# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:54:26 2019

@author: lytov
"""

def getCoordinatesSubgrid(x, y, i, PARAM):
    #   Returns the correct coordinates according to the
    # subgrid I. Every subgrid has an own shift
    
    cellSize = PARAM["L"]
    xmin = PARAM["xmin"]
    xmax = PARAM["xmax"]
    ymin = PARAM["ymin"]
    ymax = PARAM["ymax"]
    
    # ширина и длина облака точек
    xWide = abs(xmin) + abs(xmax)
    yWide = abs(ymin) + abs(ymax)
    
    NX = xWide // cellSize
    NY = yWide // cellSize
    
    # Calculate the cell where the point (x,y) should fall in.
    if i == 1:
        ix = min([((x - xmin) // cellSize) , NX-1])
        iy = min([((y - ymin) // cellSize) , NY-1])
    elif i == 2:
        ix = min([((x - xmin + cellSize/2) // cellSize) , NX-1])
        iy = min([((y - ymin) // cellSize) , NY-1])
    elif i == 3:
        ix = min([((x - xmin) // cellSize) , NX-1])
        iy = min([((y - ymin + cellSize/2) // cellSize) , NY-1])
    else:
        ix = min([((x - xmin + cellSize/2) // cellSize) , NX-1])
        iy = min([((y - ymin + cellSize/2) // cellSize) , NY-1])
    
    return ix, iy
