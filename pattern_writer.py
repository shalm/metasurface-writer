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

    if (pos[0], pos[1]) in prev_pos:
        return arr
    
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
    