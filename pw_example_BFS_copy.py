#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 00:40:28 2021

@author: marilynmeyers
"""

import gdspy
import numpy as np
import math
import sys

baseUnit = 1 #layout scale(microns)
m=baseUnit*1e6 
nm = m*1E-9
sys.setrecursionlimit(10**5)

gdspy.current_library = gdspy.GdsLibrary()
geometry1 = gdspy.Cell("CIRCLE")
geometry1.add(gdspy.Round((0, 0), 72*nm, tolerance=0.001))
geometry2 = gdspy.Cell("OVAL")
geometry2.add(gdspy.Round((0, 0), [72*nm, 64*nm], tolerance=1e-4))
def p_f(point):
    return np.sqrt(point[0]**2 + point[1]**2)
def g_f(distance):
    if distance < 25:
        return geometry1
    else:
        return geometry2

def posArrayGen(a,b,dim, generator_function, placement_function, pos=(0,0), prevDir= (0,0), arr=[], prev_pos=[]):
    '''
    

    Parameters
    ----------
    a : tuple 
        First vector 
    b : tuple 
        Second vector
    dim : tuple 
        dimensions of the layout 
    generator_function : function that takes in the output 
        of the placement function and returns a gdspy shape
    placement_function : function that takes in the point coordinates 
        and returns a value that the generator_function takes in
    pos : tuple of the starting coordinates, optional
        The default is (0,0).
    prevDir : tuple of the previous direction unit vector, optional
        The default is (0,0).
    arr : an array of the placed geometries, optional
        The default is [].
    prev_pos : a list of the previously used coordinates, optional
        The default is [].

    Returns
    -------
    arr : an array of all geometries that have 
        been placed on the layout
        

    '''
    #BFS or DP
    [dimX, dimY] = dim

    past_pos= np.array([(pos[0],pos[1])])
    queue =[]
    queue.append((pos[0],pos[1]))
    dict1={pos[0]:[pos[1]]}
    geometry_cell= generator_function(placement_function((pos[0], pos[1])))
    arr.append(gdspy.CellReference(geometry_cell, (pos[0], pos[1]), magnification=1))
    
    while (len(queue)>0):
        current_pos = queue[0]
        # if current_pos not in past_pos:
        #     past_pos.append(current_pos)
            
            # print(len(past_pos))
            
        pax=(a[0]+current_pos[0])<=dimX/2 and (a[0] + current_pos[0])>=-dimX/2
        pay=(a[1]+current_pos[1])<=dimY/2 and (a[1] + current_pos[1])>=-dimY/2
        pa=bool(pax*pay)
        nax=(-a[0]+current_pos[0])<=dimX/2 and (-a[0] + current_pos[0])>=-dimX/2
        nay=(-a[1]+current_pos[1])<=dimY/2 and (-a[1] + current_pos[1])>=-dimY/2
        na=bool(nax*nay)
        
        pbx=(b[0]+current_pos[0])<=dimX/2 and (b[0] + current_pos[0])>=-dimX/2
        pby=(b[1]+current_pos[1])<=dimY/2 and (b[1] + current_pos[1])>=-dimY/2
        pb=bool(pbx*pby)
        nbx=(-b[0]+current_pos[0])<=dimX/2 and (-b[0] + current_pos[0])>=-dimX/2
        nby=(-b[1]+current_pos[1])<=dimY/2 and (-b[1] +current_pos[1])>=-dimY/2
        nb=bool(nbx*nby)
        
        if pa:
            vec=(a[0] + current_pos[0], a[1]+current_pos[1])
            if vec[0] in dict1.keys():
                if vec[1] not in dict1[vec[0]]:
                    x=dict1[vec[0]]
                    x.append(vec[1])
                    dict1.update({vec[0]:x})
                    queue.append(vec)
                    geometry_cell= generator_function(placement_function(vec))
                    arr.append(gdspy.CellReference(geometry_cell, vec, magnification=1))
            else:
                dict1.update({vec[0]:[vec[1]]})
                queue.append(vec)
                geometry_cell= generator_function(placement_function(vec))
                arr.append(gdspy.CellReference(geometry_cell, vec, magnification=1))
                    
        if na:
            vec=(-a[0] + current_pos[0], -a[1]+current_pos[1])
            if vec[0] in dict1.keys():
                if vec[1] not in dict1[vec[0]]:
                    x=dict1[vec[0]]
                    x.append(vec[1])
                    dict1.update({vec[0]:x})
                    queue.append(vec)
                    geometry_cell= generator_function(placement_function(vec))
                    arr.append(gdspy.CellReference(geometry_cell, vec, magnification=1))
            else:
                dict1.update({vec[0]:[vec[1]]})
                queue.append(vec)
                geometry_cell= generator_function(placement_function(vec))
                arr.append(gdspy.CellReference(geometry_cell, vec, magnification=1))
            
        if pb:
            vec=(b[0] + current_pos[0], b[1]+current_pos[1])
            if vec[0] in dict1.keys():
                if vec[1] not in dict1[vec[0]]:                  
                    x=dict1[vec[0]]
                    x.append(vec[1])
                    dict1.update({vec[0]:x})
                    queue.append(vec)
                    geometry_cell= generator_function(placement_function(vec))
                    arr.append(gdspy.CellReference(geometry_cell, vec, magnification=1))
            else:
                dict1.update({vec[0]:[vec[1]]})
                queue.append(vec)
                geometry_cell= generator_function(placement_function(vec))
                arr.append(gdspy.CellReference(geometry_cell, vec, magnification=1))
            
        if nb:
            vec=(-b[0] + current_pos[0], -b[1]+current_pos[1])
            if vec[0] in dict1.keys():
                if vec[1] not in dict1[vec[0]]:
                    x=dict1[vec[0]]
                    x.append(vec[1])
                    dict1.update({vec[0]:x})
                    queue.append(vec)
                    geometry_cell= generator_function(placement_function(vec))
                    arr.append(gdspy.CellReference(geometry_cell, vec, magnification=1))
                    
            else:
                dict1.update({vec[0]:[vec[1]]})
                queue.append(vec)
                geometry_cell= generator_function(placement_function(vec))
                arr.append(gdspy.CellReference(geometry_cell, vec, magnification=1))
        # print(past_pos)
        queue.pop(0)
    
    return arr
    
a=[1,0]
b=[.5,math.sqrt(3)/2]
dim=(300, 300)
cells=posArrayGen(a,b,dim, g_f, p_f)

gdspy.current_library = gdspy.GdsLibrary()

Lens = gdspy.Cell("LENS")
Lens.add(cells)
gdspy.current_library.add(Lens)
gdspy.write_gds('Testing41.gds')

