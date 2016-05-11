from tkinter import *
from random import random,randint
from math import exp
from time import sleep
from sys import setrecursionlimit

setrecursionlimit(100000)
def g(x):
    return 1/(1+exp(-x))
def modification(x):
    if randint(0,50)!=0:
        return x
    return x+(random()**2*randint(-1,1))/100
pos=0

T=20
DIST=15
nbPasses=0
generation=0
vitesses=[1,33,50,100,500,1000]
v=0
def position(*arg):
    for el in arg:
        yield el*40+10

def jouer():
    global nbPasses
    nbPasses+=1
    C.delete(ALL)
    text=""
    for i in range(nbEl):
        text=text+"J{} : {}\n".format(i+1,Joueurs[i].score)
        
    C.create_text(DIST*40+30,500,text=text,font=(12))
    C.create_text(100,30,text="J1:{} J2:{}\nGénération;{}".
                  format(pos1+1,pos2+1,generation),font=(14))
     
    C.create_rectangle(*position(0, J1.position,1, J1.position+1),fill="red")
    C.create_rectangle(*position(DIST, J2.position,DIST-1,J2.position+1),fill="green")
    if J1.aballe:
        C.create_oval(*position(J1.balleT,J1.balleP,J1.balleT+1,J1.balleP+1))
    if J2.aballe:
        C.create_oval(*position(DIST-J2.balleT,J2.balleP,DIST-J2.balleT-1,J2.balleP+1))
    J1.mouvement(J2)
    J2.mouvement(J1)

    a=J2.update(J1)
    b=J1.update(J2)
    
    if b and not a:
        Joueurs[pos1].score+=3
        Joueurs[pos2].score-=2
        nouveau()

    elif a and not b:
        Joueurs[pos2].score+=3
        Joueurs[pos1].score-=2
        nouveau()
        
    elif nbPasses==DIST*10 or (a and b):
        Joueurs[pos1].score+=1
        Joueurs[pos2].score+=1
        nouveau()
    fen.after(vitesses[v],jouer)
def nouveau():
    global pos1,pos2,nbPasses,Joueurs,generation
    C.update()
    #sleep(.3)
    #print(pos1,pos2)
    nbPasses=0
    pos1+=1
    if pos1==nbEl:
        pos1=0
        pos2+=1
    if pos1==pos2:
        pos1+=1
    if pos1==nbEl:
        print("---fin---")
        text=""
        for i in range(nbEl):
            text=text+"J{} : {}\n".format(i+1,Joueurs[i].score)
        print(text)
        scoreTotal=0
        for jou in Joueurs:
            scoreTotal+=jou.score
        anc=sorted(Joueurs, reverse=True, key= lambda el : el.score)
        Joueurs=[joueur(ReseauNeurone(3,3,5,3)) for i in range(nbEl//5)]
        while len(Joueurs)<20:
            for el in anc:
                if randint(0,max(el.score,1))>scoreTotal//20:
                    Joueurs.append(joueur(el.IA))
                while randint(0,max(el.score,1))>scoreTotal//20:
                    Joueurs.append(joueur(el.IA.mutation()))
        Joueurs=Joueurs[:20]
        pos1=0
        pos2=1
        generation+=1
    genererJoueurs()

class neurone:
    def __init__(self, coucheFils, poid=None):
        global pos
        self.pos=pos
        pos+=1
        self.coucheFils=coucheFils
        self.nbFils=len(coucheFils)
        if poid is None:
            self.poid=[random()*2-1 for i in range(self.nbFils)]
        else:
            self.poid=poid
            
    def valeurUpdate(self):
        self.valeur=0
        for av in range(self.nbFils):
            self.valeur+=g(self.coucheFils[av].valeur)*self.poid[av]
class ReseauNeurone:
    def __init__(self, nbCouches, *arg):
        self.neurones=[[]]
        self.nbCouches=nbCouches
        self.arg=arg
        for i in range(nbCouches):
            self.neurones.append([neurone(self.neurones[-1])for j in range(arg[i])])
        self.neurones.pop(0)
    def sortie(self, entre):
        for i in range(len(self.neurones[0])):
            self.neurones[0][i].valeur=entre[i]
        for couche in range(1,len(self.neurones)):
            for i in range(len(self.neurones[couche])):
                self.neurones[couche][i].valeurUpdate()
        return list(el.valeur for el in self.neurones[-1])
    def mutation(self):
        retour=ReseauNeurone(self.nbCouches, *self.arg)
        for couche in range(1,len(self.neurones)):
            for i in range(len(self.neurones[couche])):
                for fils in range(self.neurones[couche][i].nbFils):
                    retour.neurones[couche][i].poid[fils]=\
                        modification(self.neurones[couche][i].poid[fils])
        return retour

class joueur:
    def __init__(self, IA):
        self.IA=IA
        self.score=0

class J:
    def __init__(self, j):
        self.position=10
        self.aballe=False
        self.balleP=-1
        self.balleT=0
        
        self.IA=j.IA
    def update(self,adv):
        if self.aballe:
            self.balleT+=1
            if self.balleT==DIST:
                if self.balleP==adv.position:
                    #print("Gagné")
                    return True
                self.aballe=False
                self.balleP=-1
                self.balleT=0
        return False
            
    def mouvement(self,adv):
        choix=self.IA.sortie((self.aballe,adv.position==self.position, adv.balleP==self.position))
        if choix[2]>0 and not self.aballe:
            self.aballe=True
            self.balleP=self.position
        if choix[0]>0:
            self.position+=1
            self.position%=T
        if choix[1]>0:
            self.position-=1
            self.position%=T
        #print(choix)
def genererJoueurs():
    global J1,J2
    J1=J(Joueurs[pos1])
    J2=J(Joueurs[pos2])
def changVitesse():
    global v
    v+=1
    if v==len(vitesses):
        v=0
    B.config(text="{} images à la seconde".format(1000//vitesses[v]))
nbEl=20
fen=Tk()
#fen.geometry("800x800+-1300+50")
C=Canvas(fen, width=DIST*40+80, height=T*40+20)
C.pack()
B=Button(fen, text="100 images à la seconde", command=changVitesse)
B.pack()
Joueurs=[joueur(ReseauNeurone(3,3,5,3))for i in range(nbEl)]
pos1=0
pos2=1
genererJoueurs()
jouer()
fen.mainloop()
