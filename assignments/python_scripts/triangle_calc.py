#!/usr/bin/env python3
#
#

import math

x1, y1, x2, y2, x3, y3 = map(float, input("Input three coordinates of a triangle in (x,y) format, separated by spaces (e.g. 0 1 2 3 4 5)").split())
a=math.sqrt((x2-x1)**2+(y2-y1)**2)
b=math.sqrt((x3-x1)**2+(y3-y1)**2)
c=math.sqrt((x3-x2)**2+(y3-y2)**2)

alpha= 
beta=
gamma=

print("The angles of your triangle are:" str(alpha))
