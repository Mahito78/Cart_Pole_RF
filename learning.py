#!/usr/bin/env python3
import numpy as np
import random
from math import *
from cart_pole import *
	# avance_all_cartesian(x,theta, length_cable)
	# fen1.after(100, physic_sim,0)
NB_ZONES = 162
ALPHA = 1000 #learning rate for actions weights w
BETA = 0.5 #learning rate for critic weights v
GAMMA =0.95 #discount factor for critic (between 0 and 1)
LAMBDAw=0.9 #Decay rate for w 
LAMBDAv=0.8 #Decray rate for v

MAX_FAILS =200
MAX_SUCCES = 1000000
w = []
v = []
w_eligibilities = []
v_eligibilities = []
NB_ZONES=162
for i in range(0, NB_ZONES):
	w.append(0)
	v.append(0)
	w_eligibilities.append(0)
	v_eligibilities.append(0)


def reset():
	x,x_dot,theta,theta_dot = (0.0,0.0,0.0,0.0)
	return [x,x_dot,theta,theta_dot]

def random_selection(state): # to modify to include biased weight of current state
	return (1/(1+exp(-max(-50,min(state,50)))))
def rand():
	return random.random()
def states(x,x_dot,theta,theta_dot):
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


def episode():
	global w,v,w_eligibilities,v_eligibilities
	steps = 0
	fails = 0
	nb_presentation=1
	[x,x_dot,theta,theta_dot]=reset()
	zone=states(x,x_dot,theta,theta_dot)
	while(fails<MAX_FAILS):
		#fen1.after(50, episode(x,x_dot,theta,theta_dot))
		y=rand()<random_selection(w[zone]) # y=heuristic = action
		if(y==True) : 
			action = 1
		else: 
			action = -1
		w_eligibilities[zone]+=(1.0- LAMBDAw)*(y-0.5)
		v_eligibilities[zone]+=(1.0- LAMBDAv)
		store=v[zone]
		[x,x_dot,theta,theta_dot]=physic_sim(action,x, x_dot, theta, theta_dot)#call cart pole
		zone=states(x,x_dot,theta,theta_dot)
		if(zone<0):
			fails+=1 ;
			failed = True
			print(steps)
			fichier = open("toto.txt", "a")
			a=str(nb_presentation)+'\t'+str(steps)+'\n'
			fichier.write(a)
			steps=0
			nb_presentation+=1
			[x,x_dot,theta,theta_dot]=reset()
			zone=states(x,x_dot,theta,theta_dot)
			r=-1.0
			p=0.0
		else:
			failed=False 
			steps+=1
			r=0
			p=v[zone]

		#Heuristic reinforcement
		heuristic_reinforcement=r+GAMMA*p-store

		#Weights updating
		for i in range(0, NB_ZONES,1):
			w[i]+=ALPHA*heuristic_reinforcement*w_eligibilities[i]
			v[i]+=BETA*heuristic_reinforcement*v_eligibilities[i]
			# if(v[i]<(-1.0)):
			# 	v[i]=v[i]
			if(failed):
				w_eligibilities[i]=0.0
				v_eligibilities[i]=0.0
			else:
				w_eligibilities[i]*=LAMBDAw
				v_eligibilities[i]*=LAMBDAv
	fichier.close()