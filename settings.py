#!/usr/bin/env python3
action = 0
w = []
v = []
w_eligibilities = []
v_eligibilities = []


NB_ZONES = 162
ALPHA = 1000 #learning rate for actions weights w
BETA = 0.5 #learning rate for critic weights v
GAMMA =0.95 #discount factor for critic (between 0 and 1)
LAMBDAw=0.9 #Decay rate for w 
LAMBDAv=0.8 #Decray rate for v

MAX_FAILS =50
MAX_SUCCES = 1000000

height = 800
width = 1000
widthrect1, heightrect1 = 80, 50
xrect1, yrect1 = (width/2)-(widthrect1/2), 3*(height/4)-(heightrect1/2)
x1, y1 = xrect1 + widthrect1/2, yrect1 - 30
x, x_dot, theta, theta_dot = 0,0,0,0

action = 0