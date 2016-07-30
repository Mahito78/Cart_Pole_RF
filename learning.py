#!/usr/bin/env python3
import numpy as np
import random
from math import *
from cart_pole import * 
from settings import *
	# avance_all_cartesian(x,theta, length_cable)
	# fen1.after(100, physic_sim,0)

for i in range(0, NB_ZONES):
	w.append(0)
	v.append(0)
	w_eligibilities.append(0)
	v_eligibilities.append(0)

def reset():
	global x,x_dot,theta,theta_dot
	x,x_dot,theta,theta_dot = (0.0,0.0,0.0,0.0)

def random_selection(state): # to modify to include biased weight of current state
	return (1/(1+exp(-max(-50,min(state,50)))))
def rand():
	return random.random()
def states():
	global x,x_dot,theta,theta_dot
	one_degree = 0.0174532
	six_degrees = 0.1047192
	twelve_degrees = 0.2094384
	fifty_degrees = 0.87266

	if (not -2.4 < x < 2.4) or (not -twelve_degrees < theta < twelve_degrees): return -1

	zone = 0 
	if x < -0.8:
   		zone = 0
	elif x < 0.8:
   		zone = 1
	else:
		zone=2

	if x_dot < -0.5:
		pass
	elif x_dot < 0.5:
		zone += 3
	else:
		zone+= 6

	if theta < -six_degrees:
		pass
	elif theta < -one_degree:
		zone += 9
	elif theta < 0:
		zone += 18
	elif theta < one_degree:
		zone += 27
	elif theta < six_degrees:
		zone += 36
	else:
		zone += 45

	if theta_dot < -fifty_degrees:
		pass
	elif theta_dot < fifty_degrees:
		zone += 54
	else:
		zone += 108

	return zone;


# if action >0:
# 	force = force_magnitude
# else:
# 	force = -force_magnitude

def episode():
	global w,v,w_eligibilities,v_eligibilities
	global action
	steps = 0
	fails = 0
	zone=states()
	while(steps<10 or fails<MAX_FAILS):
		steps+=1
		y=rand()<random_selection(w[zone]) # y=heuristic = action
		action =y 
		w_eligibilities[zone]+=(1.0- LAMBDAw)*(y-0.5)
		v_eligibilities[zone]+=(1.0- LAMBDAv)
		store=v[zone]
		#cart_pole.physic_sim()#call cart pole
		zone=states()
		if(zone<0):
			fails+=1 ;
			failed = True
			reset()
			zone=states()
			r=-1.0
			p=0.0
		else:
			failed=False 
			r=0 ;
			p=v[zone]

		#Heuristic reinforcement
		heuristic_reinforcement=r+GAMMA*p-store

		#Weights updating
		for i in range(0, NB_ZONES,1):
			w[i]+=ALPHA*heuristic_reinforcement*w_eligibilities[i]
			v[i]+=BETA*heuristic_reinforcement*v_eligibilities[i]
		#if(v[i]<(-1.0)):
			#v[i]=v
			if(failed):
				w_eligibilities[i]=0.0
				v_eligibilities[i]=0.0
			else:
				w_eligibilities[i]*=LAMBDAw
				v_eligibilities[i]*=LAMBDAv
				
		return y



for i in range(0,1000,1):
	episode()
