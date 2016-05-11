from random import random,randint
from math import exp

def g(x):
    if x<-20:
        return 0
    return 1/(1+exp(-x))

def modification(x):
    if randint(0,500)!=0:
        return x
    return x+(randint(-1,1)**3)/3

class neurone:
    def __init__(self, coucheFils, poid=None):
        self.coucheFils=coucheFils
        self.nbFils=len(coucheFils)
        if poid is None:
            self.poid=[random()*2-1 for i in range(self.nbFils)]
        else:
            self.poid=poid

    def valeurUpdate(self):
        self.valeur=self.w0
        for av in range(self.nbFils):
            self.valeur+=self.coucheFils[av].valeur*self.poid[av]
        self.valeur=g(self.valeur)

    def exporter(self, fichier):
        for p in self.poid:
            fichier.write(str(p)+" ")
        fichier.write(str(self.w0)+"\n")
    def importer(self, chaine):
        mesValeurs=list(map(float, chaine.split()))
        self.poid=mesValeurs[:-1]
        self.w0=mesValeurs

class ReseauNeurone:
    def __init__(self, nbCouches, *arg):
        if isinstance(nbCouches, str):
            with open(nbCouches) as f:
                ligne1=list(map(int, f.readline().split()))
                self.__init__(len(ligne1), *ligne1)
                for couche in range(len(self.neurones)):
                    for i in range(len(self.neurones[couche])):
                        self.neurones[couche][i].importer(f.readline())
            return
        self.neurones=[[]]
        self.nbCouches=nbCouches
        self.arg=arg
        for i in range(nbCouches):
            self.neurones.append([neurone(self.neurones[-1])for j in range(arg[i])])
        self.neurones.pop(0)
    def __equal__(self, res):
        for couche in range(1,len(self.neurones)):
            for i in range(len(self.neurones[couche])):
                for fils in range(self.neurones[couche][i].nbFils):
                    if self.neurones[couche][i][fils]!=res.neurones[couche][i][fils]:
                        return False
        return True

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
                retour.neurones[couche][i].w0=modification(self.neurones[couche][i].w0)
        return retour
    def exporter(self, nomFichier):
        fichier=open(nomFichier, "w")
        fichier.write(" ".join(map(str, self.arg)))
        fichier.write("\n")
        for couche in self.neurones:
            for n in couche:
                n.exporter(fichier)