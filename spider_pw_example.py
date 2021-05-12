#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 09:06:20 2021

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
    pax=(a[0]+pos[0])<=dimX/2 and (a[0] + pos[0])>=-dimX/2
    pay=(a[1]+pos[1])<=dimY/2 and (a[1] + pos[1])>=-dimY/2
    pa=bool(pax*pay)
    nax=(-a[0]+pos[0])<=dimX/2 and (-a[0] + pos[0])>=-dimX/2
    nay=(-a[1]+pos[1])<=dimY/2 and (-a[1] + pos[1])>=-dimY/2
    na=bool(nax*nay)
    
    pbx=(b[0]+pos[0])<=dimX/2 and (b[0] + pos[0])>=-dimX/2
    pby=(b[1]+pos[1])<=dimY/2 and (b[1] + pos[1])>=-dimY/2
    pb=bool(pbx*pby)
    nbx=(-b[0]+pos[0])<=dimX/2 and (-b[0] + pos[0])>=-dimX/2
    nby=(-b[1]+pos[1])<=dimY/2 and (-b[1] + pos[1])>=-dimY/2
    nb=bool(nbx*nby)

    while (pos[0], pos[1]) not in prev_pos:
        prev_pos.append((pos[0], pos[1]))
        geometry_cell= generator_function(placement_function((pos[0], pos[1])))
        arr.append(gdspy.CellReference(geometry_cell, (pos[0], pos[1]), magnification=1))
        if pa:
            vec=(a[0] + pos[0], a[1]+pos[1])
            posArrayGen(a,b,dim, generator_function, placement_function, pos=vec, prevDir=(1,0), arr=arr, prev_pos=prev_pos)
        
        if na:
            vec=(-a[0] + pos[0], -a[1]+pos[1])
            posArrayGen(a,b,dim, generator_function, placement_function, pos=vec, prevDir=(-1,0), arr=arr, prev_pos=prev_pos)
    
        if pb:
            vec=(b[0] + pos[0], b[1]+pos[1])
            posArrayGen(a,b,dim, generator_function, placement_function, pos=vec, prevDir=(0,1), arr=arr, prev_pos=prev_pos)
        
        if nb:
            vec=(-b[0] + pos[0], -b[1]+pos[1])
            posArrayGen(a,b,dim, generator_function, placement_function, pos=vec, prevDir=(0,-1), arr=arr, prev_pos=prev_pos)
   

    return arr
    
a=[1,0]
b=[.5,math.sqrt(3)/2]
dim=(125, 125)
cells=posArrayGen(a,b,dim, g_f, p_f)

gdspy.current_library = gdspy.GdsLibrary()

Lens = gdspy.Cell("LENS")
Lens.add(cells)
gdspy.current_library.add(Lens)
gdspy.write_gds('Testing40.gds')
