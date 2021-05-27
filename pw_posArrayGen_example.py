#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:00:39 2021

@author: marilynmeyers
"""

import gdspy
import numpy as np
import math
import pattern_writer as pw

baseUnit = 1 #layout scale(microns)
m=baseUnit*1e6 
nm = m*1E-9

gdspy.current_library = gdspy.GdsLibrary()
geometry1 = gdspy.Cell("CIRCLE")
geometry1.add(gdspy.Round((0, 0), 72*nm, tolerance=0.001))

geometry2 = gdspy.Cell("RECTANGLE")
geometry2.add(gdspy.Rectangle((0, 0), (200*nm, 400*nm)))

def p_f(point):
    return np.sqrt(point[0]**2 + point[1]**2)
def g_f(distance):
    if distance < 25:
        return geometry1
    else:
        return geometry2
    
a=[1,0]
b=[.5,math.sqrt(3)/2]
dim=(250, 250)
cells=pw.posArrayGen(a,b,dim, g_f, p_f)

gdspy.current_library = gdspy.GdsLibrary()

Lens = gdspy.Cell("LENS")
Lens.add(cells)
gdspy.current_library.add(Lens)
gdspy.write_gds('Testing47.gds')