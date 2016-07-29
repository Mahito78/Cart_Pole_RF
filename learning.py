#!/usr/bin/env python3
import numpy as np
	# avance_all_cartesian(x,theta, length_cable)
	# fen1.after(100, physic_sim,0)

def reset():
	global x,x_dot,theta,theta_dot
	x,x_dot,theta,theta_dot = (0.0,0.0,0.0,0.0)
def fail():
	twelve_degree=0.2094384
	if (not -2.4 < self.x < 2.4) or (not -twelve_degrees < theta < twelve_degrees): return True
	else: return False
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

def reward():
	if fail() : return -1
	else: return 0

NB_ZONES = 162
ALPHA = 1000 #learning rate for actions weights w
BETA = 0.5 #learning rate for critic weights v
GAMMA =0.95 #discount factor for critic (between 0 and 1)
LAMBDAw=0.9 #Decay rate for w 
LAMBDAv=0.8 #Decray rate for v

MAX_FAILS =100
MAX_SUCCES = 1000000

	if action >0:
		force = force_magnitude
	else:
		force = -force_magnitude

	tau = 0.02 # pas d'integration

def episode():
	global w,v,w_eligibilities,v_eligibilities
	global action
	steps = 0
	fails = 0
	zone=states()
	while(steps<20 or fails<MAX_FAILS):
		steps+=1
		y=rand()<random_selection(w[zone]) # y=heuristic = action
		w_eligibilities[zone]+=(1.0- LAMBDAw)*(y-0.5)
		v_eligibilities[zone]+=(1.0- LAMBDAv)
		store=v[zone]
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
		for in in range(0, NB_ZONES):
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




#w =np.zeros((NB_ZONES,), dtype=np.float)
#v =np.zeros((NB_ZONES,), dtype=np.float)
#w_eligibilities = np.zeros((NB_ZONES,), dtype=np.float)
#v_eligibilities = np.zeros((NB_ZONES,), dtype=np.float)
episode()
