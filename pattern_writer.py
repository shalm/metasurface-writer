#pattern_writer.py
"""This file holds the core engine for the metasurface writer, and associated helper functions"""
import gdspy

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
