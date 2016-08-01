#!/usr/bin/env python3
from learning import *


height = 800
width = 1000
widthrect1, heightrect1 = 80, 50
xrect1, yrect1 = (width/2)-(widthrect1/2), 3*(height/4)-(heightrect1/2)
x1, y1 = xrect1 + widthrect1/2, yrect1 - 30
x, x_dot, theta, theta_dot = 0,0,0,0

action = 0

episode()
