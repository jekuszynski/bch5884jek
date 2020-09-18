#!/usr/bin/env python3
#
#

import math

x1, y1, x2, y2, x3, y3 = map(float, input("Input three coordinates of a triangle in (x,y) format, separated by spaces (e.g. 0 1 2 3 4 5):\n").split())

a=math.sqrt((x2-x1)**2+(y2-y1)**2)
b=math.sqrt((x3-x1)**2+(y3-y1)**2)
c=math.sqrt((x3-x2)**2+(y3-y2)**2)

alpha=round(math.degrees(math.acos((b**2+c**2-a**2)/(2*b*c))),3)
beta=round(math.degrees(math.acos((a**2+c**2-b**2)/(2*a*c))),3)
gamma=round(math.degrees(math.acos((b**2+a**2-c**2)/(2*b*a))),3)

print("The angles of your triangle are: \u03B1 = " + str(alpha) + "\u00B0, \u03B2 = " + str(beta) + "\u00B0, & \u03B3 = " + str(gamma) + "\u00B0")
