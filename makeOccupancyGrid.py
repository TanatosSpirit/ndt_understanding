# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 14:50:06 2019

@author: lytov
"""
import numpy as np

def makeOccupancyGrid(scan, PARAM):
    # makeOccupancyGrid returns an occupancy grid out of a range finder
    #scan. The grid size is dynamic and depends on the cartesian area covered
    #by the points in Scan. We suppose the points to be ordered by angle.
    #Adjacent points are neighbours. The grid has a probabilistic fashion, each
    #cell is filled with its occupancy probability modeled by a gaussian
    #derivied by the number of n points which fall inside it. 

    # SUBGRIDS is a set of 4 occupancy grid maps defined using a small shift
    # over the original center of the grid. 
    cellSize = PARAM["L"]
    xmin = PARAM["xmin"]
    xmax = PARAM["xmax"]
    ymin = PARAM["ymin"]
    ymax = PARAM["ymax"]
    
    sizeScan = len(scan)
    
    # ширина и длина облака точек
    xWide = abs(xmin) + abs(xmax)
    yWide = abs(ymin) + abs(ymax)
    
    # остаток от деления на размер блока
    x_remainder = xWide % cellSize
    y_remainder = yWide % cellSize

    NX = xWide // cellSize
    NY = yWide // cellSize
    
    # количество блоков по X и Y размером cellSize
    if x_remainder!=0: 
        NX = NX + 1
    if y_remainder!=0: 
        NY = NY + 1
    
    #  we create the occupancy grid structures, each cell is defined by a mean
    # and covariance pdf
    ogrid1 = []                                                             
    for i in range (NY):
        new = []                  
        for j in range (NX):   
            new.append([0, [[0,0],[0,0]]])      
        ogrid1.append(new)
    
    ogrid2 = []                                                             
    for i in range (NY):  
        new = []                
        for j in range (NX):   
            new.append([0, [[0,0],[0,0]]])       
        ogrid2.append(new)
    
    ogrid3 = []                                                             
    for i in range (NY): 
        new = []                 
        for j in range (NX):   
            new.append([0, [[0,0],[0,0]]])     
        ogrid3.append(new)
        
    ogrid4 = []                                                             
    for i in range (NY): 
        new = []                  
        for j in range (NX):   
            new.append([0, [[0,0],[0,0]]])      
        ogrid4.append(new)
    
    
    # Initialize the cells to group the points togheter
    pgrid1 = []                                                             
    for i in range (NY):        
        new = []                  
        for j in range (NX):   
            new.append([])      
        pgrid1.append(new)
        
    pgrid2 = []                                                             
    for i in range (NY):        
        new = []                  
        for j in range (NX):   
            new.append([])      
        pgrid2.append(new)
    
    pgrid3 = []                                                             
    for i in range (NY):        
        new = []                  
        for j in range (NX):   
            new.append([])      
        pgrid3.append(new)
        
    pgrid4 = []                                                             
    for i in range (NY):        
        new = []                  
        for j in range (NX):   
            new.append([])      
        pgrid4.append(new)
    
   
    #Group scans according to the cell they fall in, Calculates 4 grids. The
    #second grid is shifted horizontally of L/2, the third is shifted
    #vertically of the same amount, and the last one is shifted both vertically
    #and horizontally of L/2 as well.
    
    for i in range(sizeScan):
        x = scan[i][0]
        y = scan[i][1]
    
        # Calculate the cell where the point (x,y) should fall in.
       
        ix1 = min([((x - xmin) // cellSize) , NX-1])
        iy1 = min([((y - ymin) // cellSize) , NY])
        
        ix2 = min([((x - xmin + cellSize/2) // cellSize) , NX-1])
        iy2 = iy1
        
        ix3 = ix1
        iy3 = min([((y - ymin + cellSize/2) // cellSize) , NY-1])
        
        ix4 = ix2
        iy4 = iy3
        
        # and add it to the respective map
        pgrid1[int(ix1)][int(iy1)].append([x, y])
        
        pgrid2[int(ix2)][int(iy2)].append([x, y])
        
        pgrid3[int(ix3)][int(iy3)].append([x, y])
        
        pgrid4[int(ix4)][int(iy4)].append([x, y])
        
    grids = [pgrid1, pgrid2, pgrid3, pgrid4]
    ogrids= [ogrid1, ogrid2, ogrid3, ogrid4]
    
    # for each cell, calculate its mean and covariance using its containing
    # points. If the number of points is smaller than 3 the cell results
    # unoccupied. 
    
    hh = 0
    tots = 0
    
    for i in range(NX):
        
        for j in range(NY):
            
            #For every cell calculate the four occupancy maps
            for kk in range(len(grids)):
                pgrid = grids[kk]
                
                npg = len(pgrid[i][j])
                mpoints = 0
                covpoints = [[0,0],
                             [0,0]]
                tots = tots + npg;
                
                if npg >= 3:
                    
                    hh = hh + 1
                    
                    # Calculate mean and covariance of all the points in the cell
                    pointsTmp = np.array(pgrid[i][j])
                    tmpNp = np.array(pointsTmp)
                    mpoints = np.mean(tmpNp, axis=0)
                    
                    covpoints = np.cov(tmpNp.T)
                
                ogrids[kk][i][j][0] = mpoints
                ogrids[kk][i][j][1] = covpoints
        
    return ogrids
