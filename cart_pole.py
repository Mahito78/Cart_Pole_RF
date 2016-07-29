#!/usr/bin/env python3
from tkinter import *
from math import * 
import random
# procédure générale de déplacement : 

def avance(gd, hb): 
	global x1, y1, xrect1, yrect1, widthrect1, heightrect1 
	x1, y1 = x1 +gd, y1 +hb 
	can1.coords(oval1, x1, y1, x1+30, y1+30)
	can1.coords(line2, x1+15,y1+15,xrect1+(widthrect1/2),yrect1)
	
def avance_all_cartesian(x, theta, length):
	theta -= pi/2 
	global x1, y1, xrect1, yrect1, widthrect1, heightrect1 
	xrect1 += x
	can1.coords(rect1,xrect1, yrect1, xrect1+widthrect1, yrect1+heightrect1)
	x1 = (xrect1 + widthrect1/2)+80*cos(theta)
	y1 = (yrect1)+80*sin(theta)
	can1.coords(oval1, x1-15, y1-15, x1+15, y1+15)
	can1.coords(line2, x1,y1,xrect1+(widthrect1/2),yrect1)

def avance_cart(gd, hb):
	global x1, y1, xrect1, yrect1, widthrect1, heightrect1 
	xrect1, yrect1 = xrect1 +gd, yrect1 +hb
	can1.coords(rect1,xrect1, yrect1, xrect1+widthrect1, yrect1+heightrect1)
	can1.coords(line2, x1+15,y1+15,xrect1+(widthrect1/2),yrect1)

def show_info():
	global x, x_dot, theta, theta_dot, action
	print('cart deplacement : ',x,' stick angle : ',theta,'\n')
	print('x ball : ',x1+15,' y ball : ',y1+15,' action : ', action, '\n')
	fen1.after(1000, show_info)

def physic_sim():
	g = 9.81
	mass_cart = 1.0
	mass_pole = 0.1
	total_mass = mass_cart+mass_pole
	length_cable = 0.5
	pole_mass_length = mass_pole * length_cable
	force_magnitude = 10.0
	global action# depend d'une autre fonction
	force = action * force_magnitude
	tau = 0.03 # pas d'integration
	global x, x_dot, theta, theta_dot
	temp = (force + pole_mass_length * pow(theta_dot,2) * sin(theta))/total_mass
	theta_accel = (g*sin(theta)-cos(theta)*temp)/(length_cable*(4/3-mass_pole*pow(cos(theta),2)/total_mass))
	x_accel = temp-pole_mass_length*theta_accel*cos(theta)/total_mass
	# --- update_state_variable ---  #
	x_dot = x_dot + tau*x_accel
	x += tau*x_dot
	theta_dot += tau*theta_accel
	theta += tau*theta_dot
	avance_all_cartesian(x,theta, length_cable)
	fen1.after(50, physic_sim)
	print('action = ', action, '\n')
	
# gestionnaires d'événements : 
def depl_gauche(): 
	avance(-10, 0)
def depl_cart_gauche():
	global action
	#avance_cart(-10,0)
	action += -0.1
def depl_droite(): 
	avance(10, 0)
def depl_cart_droite():
	global action
	#avance_cart(10,0)
	action += 0.1  
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
action = 0
height = 800
width = 1000
widthrect1, heightrect1 = 80, 50
xrect1, yrect1 = (width/2)-(widthrect1/2), 3*(height/4)-(heightrect1/2)
x1, y1 = xrect1 + widthrect1/2, yrect1 - 30
x, x_dot, theta, theta_dot = 0,0,0,0.001

'''w = []
v = []
w_eligibilities = []
v_eligibilities = []
for i in range(0, NB_ZONES):
	w.append(0)
	v.append(0)
	w_eligibilities.append(0)
	v_eligibilities.append(0)'''

  
# coordonnées initiales # Création du widget principal ("maître") : 
fen1 = Tk() 
fen1.title("Pendule inversé v0.1") 
# création des widgets "esclaves" : 
can1 = Canvas(fen1,bg='white',height=1000,width=1000)
can1.focus_set()
can1.bind("<Key>",clavier)
oval1 = can1.create_oval(x1,y1,x1+30,y1+30,width=1,fill='red')
rect1 = can1.create_rectangle(xrect1, yrect1, xrect1+widthrect1, yrect1+heightrect1, fill="blue")
line1 = can1.create_line(0,3*(height/4)+heightrect1, width, 3*(height/4)+heightrect1,width=2,fill="black")
line2 = can1.create_line(x1+15,y1+15,xrect1+(widthrect1/2),yrect1,width=3, fill="red") 
can1.pack(side=LEFT) 
Button(fen1,text='Quitter',command=fen1.quit).pack(side=BOTTOM) 
Button(fen1,text='Gauche',command=depl_gauche).pack() 
Button(fen1,text='Droite',command=depl_droite).pack() 
Button(fen1,text='Haut',command=depl_haut).pack() 
Button(fen1,text='Bas',command=depl_bas).pack() 
# démarrage du réceptionnaire d'évènements (boucle principale) : 
fen1.after(50, physic_sim)
fen1.after(1000, show_info)
fen1.mainloop()

