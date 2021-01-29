#pattern_writer.py
"""This file holds the core engine for the metasurface writer, and associated helper functions"""
import gdspy

def array_singleReference(Xs, Ys, reference_geometry):
    #set up date for file name
    #outputFileName= str(max(Xs)-min(Xs))+'by'+ str(max(Ys)-min(Ys))+ 'map of geometries'
    # Create a cell with a component that is used repeatedly
    array=[]

    #center a reference of the geometry at each (x,y) coordinate
    for x in Xs:
        for y in Ys:  
            array.append(gdspy.CellReference(reference_geometry, (x, y), magnification=1))
    return array
      
def array_diffGeometries(Xs, Ys, reference_geometries):
    array=[]
    i=0
    for x in Xs:
        for y in Ys:  
            array.append(gdspy.CellReference(reference_geometries[i], (x, y), magnification=1))
            i+=1
    return array
