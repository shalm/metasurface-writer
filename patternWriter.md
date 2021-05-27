# patternWriter

patternWriter places gdspy shapes on layouts through points or creates layouts with gdspy shapes based on vectors.

## Installation

Download the package or clone the repository, and then install with:

```bash
python setup.py install
```

### Prerequisites

patternWriter uses gdspy

### Basic Usage

This demo creates a hexagonal layout with circles at a distance less than 25 and rectangles at all further points with the dimension 250 by 250.

```python
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
```
The output layout can be seen in the figures below: 

![Figure [layout]: An example of a layout](layout_example.png)
![Figure [layout2]: A zoomed in image of the layout above](layout_example_zoom.png))

For more details on using gdspy on this see the gdspy documentation: https://github.com/heitzmann/gdspy

The code example shown above can be found as a Jupyter notebook in the Demos folder.

## Authors

Mmeyers3, Trezitorul, Shalm

## License

This project is licensed under the MIT License