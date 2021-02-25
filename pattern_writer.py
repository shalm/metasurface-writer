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

def layout_placement(basisX, basisY, numberX, numberY, generator_function, placement_function):
    '''
    

    Parameters
    ----------
    basisX : a vector, [x,y]
    basisY : a vector, [x,y]
    numberX : integer
        This is the number of desired X values for each vector to generate.
    numberY : integer
        This is the number of desired Y values for each vector to generate.
    generator_function : a function
        This function must take in the value that the placement_function returns.
    placement_function : a function
        This function must take in an (X, Y) coordinate and return the input(s) of the generator_function.

    Returns
    -------
    array : an array of each geometry centered at each (x,y) coordinate in the appropiate layout shape

    '''
    array=[]
    array_X=[]
    array_Y=[]
    lastX=0
    for nX in range(numberX):
        array_X.append(lastX)
        lastY=0
        for nY in range(numberY):
            if len(array_Y)<numberY:
                array_Y.append(lastY)
            geometry_cell= generator_function(placement_function(lastX, lastY))
            array.append(gdspy.CellReference(geometry_cell, (lastX, lastY), magnification=1))
            #pw.array_singleReference(lastX, lastY, geometry_cell)
            lastY+=(basisX[1])
        lastX+=(basisX[0])
    array2_X= np.add(array_X, basisY[0]).tolist()
    array2_Y= np.add(array_Y, basisY[1]).tolist()
    #print(array2_Y)
    for n2X in array2_X:
        for n2Y in array2_Y:
            geometry_cell= generator_function(placement_function(n2X, n2Y))
            array.append(gdspy.CellReference(geometry_cell, (n2X, n2Y), magnification=1))
    return array
