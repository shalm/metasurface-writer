#pattern_writer.py
"""This file holds the core engine for the metasurface writer, and associated helper functions"""
import gdspy
import numpy as np

def array_singleReference(Xs, Ys, reference_geometry):
    '''
    Parameters
    ----------
    Xs : List of x values
    Ys : List of y values
    reference_geometry : a geometry reference cell

    Returns
    -------
    array : an array of the geometry centered at each (x,y) coordinate
    
    '''
    
    array = []
    for x in Xs:
        for y in Ys:  
            array.append(gdspy.CellReference(
                reference_geometry, (x, y), 
                magnification=1))
    return array
      
def array_diffGeometries(Xs, Ys, reference_geometries):
    '''
    Parameters
    ----------
    Xs : List of x values
    Ys : List of y values
    reference_geometries : List of geometry reference cells (of length X*Y)

    Returns
    -------
    array : an array of each geometry centered at each (x,y) coordinate
    
    '''
    
    array = []
    i = 0
    for x in Xs:
        for y in Ys:  
            array.append(gdspy.CellReference(
                reference_geometries[i], (x, y), 
                magnification=1))
            i += 1
    return array

def posArrayGenerator(a, b, numA, numB, xlimit, ylimit, generator_function, placement_function):
    
    arr=[]
    new_x=0
    new_y=0
    for x in range(-numA,numA):
        for y in range(-numB,numB):
            vec=[(x*a[0]+y*b[0], x*a[1]+y*b[1])]
            if vec[0][0]<= xlimit and vec[0][0]>= -xlimit and vec[0][1] <= ylimit and vec[0][1] >= -ylimit:
                geometry_cell= generator_function(placement_function(vec[0][0], vec[0][1]))
                arr.append(gdspy.CellReference(geometry_cell, (vec[0][0], vec[0][1]), magnification=1))
            elif vec[0][0]>= xlimit:
                new_x=vec[0][0]- (2*xlimit)
                geometry_cell= generator_function(placement_function(new_x, vec[0][1]))
                arr.append(gdspy.CellReference(geometry_cell, (new_x, vec[0][1]), magnification=1))
            elif vec[0][0]<= -xlimit:
                new_x=vec[0][0]+ (2*xlimit)
                geometry_cell= generator_function(placement_function(new_x, vec[0][1]))
                arr.append(gdspy.CellReference(geometry_cell, (new_x, vec[0][1]), magnification=1))
            elif vec[0][1]>= ylimit:
                new_y=vec[0][1]- (2*ylimit)
                geometry_cell= generator_function(placement_function(vec[0][0], new_y))
                arr.append(gdspy.CellReference(geometry_cell, (vec[0][0], new_y), magnification=1))
            elif vec[0][1]<= -ylimit:
                new_y=vec[0][1]+ (2*ylimit)
                geometry_cell= generator_function(placement_function(vec[0][0], new_y))
                arr.append(gdspy.CellReference(geometry_cell, (vec[0][0], new_y), magnification=1))
    return arr