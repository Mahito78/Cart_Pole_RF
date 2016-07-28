#!/usr/bin/env python3
from tkinter import *
from math import * 
import random
import numpy as np
# procédure générale de déplacement : 

NB_ZONES = 162
ALPHA = 1000 #learning rate for actions weights w
BETA = 0.5 #learning rate for critic weights v
GAMMA =0.95 #discount factor for critic (between 0 and 1)
LAMBDAw=0.9 #Decay rate for w 
LAMBDAv=0.8 #Decray rate for v

MAX_FAILS =100
MAX_SUCCES = 1000000
def avance(gd, hb): 
	global x1, y1, xrect1, yrect1, widthrect1, heightrect1 
	x1, y1 = x1 +gd, y1 +hb 
	can1.coords(oval1, x1, y1, x1+30, y1+30)
	can1.coords(line2, x1+15,y1+15,xrect1+(widthrect1/2),yrect1)
	
def avance_all_cartesian(x, theta, length): 
	global x1, y1, xrect1, yrect1, widthrect1, heightrect1 
	x1 = 40*cos(theta)
	y1 = 40*sin(theta)
	can1.coords(oval1, x1, y1, x1+30, y1+30)
	xrect1 += x
	can1.coords(rect1,xrect1, yrect1, xrect1+widthrect1, yrect1+heightrect1)
	can1.coords(line2, x1+15,y1+15,xrect1+(widthrect1/2),yrect1)

def avance_cart(gd, hb):
	global x1, y1, xrect1, yrect1, widthrect1, heightrect1 
	xrect1, yrect1 = xrect1 +gd, yrect1 +hb
	can1.coords(rect1,xrect1, yrect1, xrect1+widthrect1, yrect1+heightrect1)
	can1.coords(line2, x1+15,y1+15,xrect1+(widthrect1/2),yrect1)

def show_info():
	global x, x_dot, theta, theta_dot
	print('cart deplacement : ',x,' stick angle : ',theta,'\n')
	print('x ball : ',x1+15,' y ball : ',y1+15,'\n')
	fen1.after(1000, show_info)

def physic_sim(action):
	g = 9.81
	mass_cart = 1.0
	mass_pole = 0.1
	total_mass = mass_cart+mass_pole
	length_cable = 0.5
	pole_mass_length = mass_pole * length_cable
	force_magnitude = 10.0
	#action = 1 # depend d'une autre fonction
	if action >0:
		force = force_magnitude
	else:
		force = -force_magnitude

	tau = 0.02 # pas d'integration
	global x, x_dot, theta, theta_dot
	temp = (force + pole_mass_length * pow(theta_dot,2) * sin(theta))/total_mass
	theta_accel = (g*sin(theta)-cos(theta)*temp)/(length_cable*(4/3-mass_pole*pow(cos(theta),2)/total_mass))
	x_accel = temp-pole_mass_length*theta_accel*cos(theta)/total_mass
	# --- update_state_variable ---  #
	x += tau*x_dot
	x_dot += tau*x_accel
	theta += tau*theta_dot
	theta_dot += tau*theta_accel
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
def episode():
	global w,v,w_eligibilities,v_eligibilities
	steps = 0
	fails = 0
	zone=states()
	while(steps<20 or fails<MAX_FAILS):
		steps+=1
		y=rand()<random_selection(w[zone]) # y=heuristic = action
		w_eligibilities[zone]+=(1.0- LAMBDAw)*(y-0.5)
		v_eligibilities[zone]+=(1.0- LAMBDAv)
		store=v[zone]
		physic_sim(y)
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
		w+=ALPHA*heuristic_reinforcement*w_eligibilities
		v+=BETA*heuristic_reinforcement*v_eligibilities
		if(v.all()<(-1.0)):
			v=v
		if(failed):
			w_eligibilities=0.0
			v_eligibilities=0.0
		else:
			w_eligibilities*=LAMBDAw
			v_eligibilities*=LAMBDAv



# gestionnaires d'événements : 
def depl_gauche(): 
	avance(-10, 0)
def depl_cart_gauche():
	avance_cart(-10,0)
	physic_sim(-0.2) 
def depl_droite(): 
	avance(10, 0)
def depl_cart_droite():
	avance_cart(10,0)
	physic_sim(0.2)  
def depl_haut(): 
	avance(0, -10) 
def depl_bas(): 
	avance(0, 10)
def clavier(event):
	touche = event.keysym
	if touche == "Left":
	 	depl_cart_gauche()
	elif touche == "Up":
		depl_haut()
	elif touche == "Right":
		depl_cart_droite()
	elif touche == "Down":
		depl_bas()
#------ Programme principal ------- # les variables suivantes seront utilisées de manière globale : 
x1, y1 = 135, 100
xrect1, yrect1 = 110, 200
widthrect1, heightrect1 = 80, 50
x,	 x_dot, theta, theta_dot = 0,0,0,0
w =np.zeros((NB_ZONES,), dtype=np.float)
v =np.zeros((NB_ZONES,), dtype=np.float)
w_eligibilities = np.zeros((NB_ZONES,), dtype=np.float)
v_eligibilities = np.zeros((NB_ZONES,), dtype=np.float)
episode()
  
# coordonnées initiales # Création du widget principal ("maître") : 
fen1 = Tk() 
fen1.title("Pendule inversé v0.1") 
# création des widgets "esclaves" : 
can1 = Canvas(fen1,bg='white',height=300,width=300)
can1.focus_set()
can1.bind("<Key>",clavier)
oval1 = can1.create_oval(x1,y1,x1+30,y1+30,width=1,fill='red')
rect1 = can1.create_rectangle(xrect1, yrect1, xrect1+widthrect1, yrect1+heightrect1, fill="blue")
line1 = can1.create_line(0,270, 300, 270,width=2,fill="black")
line2 = can1.create_line(x1+15,y1+15,xrect1+(widthrect1/2),yrect1,width=3, fill="red") 
can1.pack(side=LEFT) 
Button(fen1,text='Quitter',command=fen1.quit).pack(side=BOTTOM) 
Button(fen1,text='Gauche',command=depl_gauche).pack() 
Button(fen1,text='Droite',command=depl_droite).pack() 
Button(fen1,text='Haut',command=depl_haut).pack() 
Button(fen1,text='Bas',command=depl_bas).pack() 
# démarrage du réceptionnaire d'évènements (boucle principale) : 
fen1.after(100, physic_sim, 0)
fen1.after(1000, show_info)
fen1.mainloop()

