#!/usr/bin/env python3
from tkinter import * 
# procédure générale de déplacement : 
def avance(gd, hb): 
	global x1, y1, xrect1, yrect1, widthrect1, heightrect1 
	x1, y1 = x1 +gd, y1 +hb 
	can1.coords(oval1, x1, y1, x1+30, y1+30)
	can1.coords(line2, x1+15,y1+15,xrect1+(widthrect1/2),yrect1)

def avance_cart(gd, hb):
	global x1, y1, xrect1, yrect1, widthrect1, heightrect1 
	xrect1, yrect1 = xrect1 +gd, yrect1 +hb
	can1.coords(rect1,xrect1, yrect1, xrect1+widthrect1, yrect1+heightrect1)
	can1.coords(line2, x1+15,y1+15,xrect1+(widthrect1/2),yrect1)
# gestionnaires d'événements : 
def depl_gauche(): 
	avance(-10, 0)
def depl_cart_gauche():
	avance_cart(-10,0) 
def depl_droite(): 
	avance(10, 0)
def depl_cart_droite():
	avance_cart(10,0)  
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
x1, y1 = 10, 10
xrect1, yrect1 = 100, 200
widthrect1, heightrect1 = 80, 50  
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
fen1.mainloop()
