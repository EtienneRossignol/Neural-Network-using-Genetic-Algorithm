from pygame.locals import*import pygamefrom neurone import *from sys import setrecursionlimitfrom matplotlib import pyplot as pltfrom time import timefrom os import mkdirROUGE=0BLEU=1COULEURS=[(0,0,255),(0,255,0),(255,0,0),(255,255,0),(255,0,255),(0,255,255),    (255,255,255),(0,0,128),(0,128,0),(128,0,0),(128,128,0),    (128,0,128),(0,128,128),(128,128,128)]nbGeneration=0minInter=[]"""MIN=[]MAX=[]"""maxInter=[]class joueur:    def __init__(self, IA,n):        self.IA=IA        self.score=0        self.strategieScore=0        self.numero=nclass J:    def __init__(self, j, pos):        self.type=pos        self.IA=j.IA        self.couleur=COULEURS[j.numero]    def update(self):        for inters in lesNoeud:            if inters.type==self.type:                inters.updateCombat()    def mouvement(self):        for inters in lesNoeud:            if inters.type==self.type:                sortie=self.IA.sortie(inters.donnerInformations())                inters.alerte=sortie[0]                for i in range(4):                    if sortie[i+1]>0:                        inters.envoyerSoldats(i, int(sortie[i+1]*10))    def score(self):        nbTerritoires=0        qualite=0        for inters in lesNoeud:            if inters.type==self.type:                nbTerritoires+=1                qualite+=max(inters.nbBleu,inters.nbRouge)*(inters.nbPlus+5)        return nbTerritoires, qualitedef fin():    print("END")    pygame.quit()    pygame.display.quit()    plt.plot(minInter)    plt.plot(maxInter)    """plt.plot(MIN,'g--')    plt.plot(MAX,'r--')"""    plt.show()def gererAffichage():    global affichage    pygame.draw.rect(screen, (0,0,0), (0,0,1000,1000))    for i in lesNoeud:        i.updateAff()        i.afficher()    for i in lesNoeud:        i.afficherLiens()    pygame.time.delay(200)    pygame.display.flip()    for ev in pygame.event.get():        if ev.type==QUIT or (ev.type==KEYDOWN and ev.key==K_ESCAPE):            affichage=False            pygame.display.quit()            pygame.quit()    return Falseclass intersection:    def __init__(self, numero,frere,bonus):        self.numero=numero        self.nbBleu=0        self.nbRouge=0        self.type=(numero*2)//nbNoeud        self.alerte=False        self.px=numero%Tdroite*120+50        self.py=numero//Tdroite*120+50        self.vx=randint( 0,1)*2-1        self.vy=randint(0,1)*2-1        self.frere=frere        self.nbPlus=bonus        self.numero=numero    def reInit(self):        self.nbBleu=0        self.nbRouge=0        self.type=self.numero*2//nbNoeud        self.alerte=0        self.px=self.numero%Tdroite*120+50        self.py=self.numero//Tdroite*120+50        self.vx=randint( 0,1)*2-1        self.vy=randint(0,1)*2-1    def afficher(self):        if self.type==ROUGE:            pygame.draw.circle(screen, J1.couleur, (self.px,self.py), 40)        else:            pygame.draw.circle(screen, J2.couleur, (self.px,self.py), 40)        """print str(self.nbBleu)+":"+str(self.nbRouge)"""        text = font.render(str(self.nbBleu)+":"+str(self.nbRouge), 1, (64,128,32))        textpos = text.get_rect()        textpos.centerx = self.px        textpos.centery = self.py        screen.blit(text, textpos)    def afficherLiens(self):        for f in  self.frere:            pygame.draw.line(screen, (128,128,64), (self.px,self.py),            (lesNoeud[f].px,lesNoeud[f].py))    def updateAff(self):        self.px+=self.vx        self.py+=self.vy        if self.px%75==40:            self.vx=1+randint(0,1)        if self.py%75==40:            self.vy=1+randint(0,1)        if self.px%75==74:            self.vx=-1-randint(0,1)        if self.py%75==74:            self.vy=-1-randint(0,1)    @staticmethod    def combat(nbattaquant, nbdefenseur):        nbMort=1        while nbattaquant>0 and nbdefenseur>0:            for i in range(nbdefenseur):                if randint(0,2):                    nbattaquant-=nbMort            nbMort+=1            for i in range(nbattaquant):                if randint(0,3):                    nbdefenseur-=nbMort        return max(nbattaquant,0), max(nbdefenseur,0)    def updateCombat(self):        if self.type==BLEU:            self.nbBleu+=self.nbPlus            self.nbBleu,self.nbRouge=self.combat(self.nbBleu,self.nbRouge)            if self.nbRouge>0:                self.type=ROUGE        else:            self.nbRouge+=self.nbPlus            self.nbRouge,self.nbBleu=self.combat(self.nbRouge,self.nbBleu)            if self.nbBleu>0:                self.type=BLEU    def infoBase(self, couleur):        if self.type==couleur:            if self.type==ROUGE:                return [self.nbPlus, self.nbRouge, self.nbBleu,self.alerte, True]            return [self.nbPlus, self.nbBleu,self.nbRouge, self.alerte, True]        if self.type==ROUGE:            return [self.nbPlus, self.nbBleu,self.nbRouge,0, False]        return [self.nbPlus, self.nbRouge, self.nbBleu, 0, False]    def donnerInformations(self):        if self.type==ROUGE:            entre=[temps, self.nbPlus, self.nbRouge, self.numero]            for voisin in self.frere:                entre.extend(lesNoeud[voisin].infoBase(ROUGE))            return entre        entre=[temps, self.nbPlus, self.nbBleu, self.numero]        for voisin in self.frere:            entre.extend(lesNoeud[voisin].infoBase(BLEU))        return entre    def envoyerSoldats(self, numero, nombre):        if self.type==ROUGE:            lesNoeud[self.frere[numero]].nbRouge+=min(self.nbRouge, nombre)            self.nbRouge-=min(self.nbRouge, nombre)        else:            lesNoeud[self.frere[numero]].nbBleu+=min(self.nbBleu, nombre)            self.nbBleu-=min(self.nbBleu, nombre)pos1=0pos2=1dejaInverse=Falsedef changerJoueur():    global pos1,pos2,dejaInverse,lesNoeud    if not dejaInverse:        pos2,pos1=pos1,pos2        dejaInverse=True    else:        dejaInverse=False        pos2,pos1=pos1,pos2        pos2+=1        if pos1==pos2:            pos2+=1        if pos2==nbJoueurs:            pos1+=1            pos2=0        if pos1==nbJoueurs:            """            pygame.quit()            pygame.display.quit()"""            print(nbGeneration)            for i,el in enumerate(sorted(Joueurs, key= lambda el : (el.score,el.strategieScore))):                print(el.score, el.strategieScore, el.numero)                if el.numero ==2:                    minInter.append(i)                elif el.numero==3:                    maxInter.append(i)            pos1=0            pos2=1            dejaInverse=False            nouvelleGeneration()            lesNoeud=mesGraphes[randint(0,nbGraphes-1)]    creerJoueur(pos1,pos2)def creerJoueur(p1,p2):    global J1,J2    #print (p1,p2)    J1=J(Joueurs[p1],ROUGE)    J2=J(Joueurs[p2],BLEU)texte=r"C:\Users\Etienne\Desktop\IA\{}".format(time())mkdir(texte)def nouvelleGeneration():    global Joueurs,nbGeneration    nbGeneration+=1    Joueurs=[joueur(ReseauNeurone(r"IA\1456264903.211\{}.txt".format(max(i*7-1,1))), i)        for i in range(nbJoueurs)]    return    ancien=sorted(Joueurs, reverse=True, key= lambda el : (el.score,el.strategieScore))    ancien[0].IA.exporter("{}\{}.txt".format(texte,nbGeneration))    """for el in ancien:        if ancienResaux==el.IA:            print(el.numero)"""    nouveau=[el.IA for el in ancien[:nbJoueurs//4]]+[ReseauNeurone(3, 24,15,5) for i in range(2)]    score=0    for el in ancien:        score+=el.score    print(Joueurs[2].score,Joueurs[2].score/score*nbJoueurs)    """maxInter.append(max(Joueurs[2].score, Joueurs[3].score)/score*nbJoueurs)    minInter.append(min(Joueurs[2].score, Joueurs[3].score)/score*nbJoueurs)    MAX.append(ancien[0].score/score*nbJoueurs)    MIN.append(ancien[-1].score/score*nbJoueurs)"""    Joueurs=[]    #print(nouveau, score, [el.IA for el in ancien[:nbJoueurs//4]])    while len(nouveau)<nbJoueurs:        for a, el in enumerate(ancien):            if el.score>=score/nbJoueurs and randint(1,score)<el.score:                nouveau.append(el.IA.mutation())    Joueurs=[joueur(IA, i) for i,IA in enumerate(nouveau[:nbJoueurs])]    if nbGeneration==nbGenerationTotal:        fin()        exit()nbGraphes=10nbGenerationTotal=5nbJoueurs=10affichage=TruenbNoeud=24Tdroite=5if affichage:    pygame.init()    pygame.font.init()    screen =pygame.display.set_mode((120*Tdroite,120*nbNoeud//Tdroite),                                    DOUBLEBUF|HWSURFACE)    font = pygame.font.Font(None, 30)Joueurs=[joueur(ReseauNeurone(3, 24,15,5),i) for i in range(nbJoueurs)]'''Joueurs=[joueur(ReseauNeurone(r"IA\1456264903.211\{}.txt".format(max(i*7-1,1))), i)        for i in range(nbJoueurs)]'''J1=J(Joueurs[0], ROUGE)J2=J(Joueurs[1], BLEU)mesGraphes=[[intersection(i,[(i+j)%nbNoeud for j in (-3,-1,1,3)], randint(0,5))            for i in range(nbNoeud)]for nb in range(nbGraphes)]for a in range(nbGraphes):    for i in range(nbNoeud//2):        mesGraphes[a][-i-1].nbPlus=mesGraphes[a][i].nbPlus+randint(-1,1)lesNoeud=mesGraphes[randint(0,nbGraphes-1)]"""for i in range(nbNoeud//2):    lesNoeud[i].type=1lesNoeud[0].nbPlus=6"""temps=0while True:    if affichage and gererAffichage():        break    if temps==150 or J1.score()[0]==nbNoeud or J2.score()[0]==nbNoeud:        nb1,score1=J1.score()        nb2,score2=J2.score()         #print ("Nouveau", temps, pos1, J1.score(), pos2, J2.score())        if nb1>nb2:            Joueurs[pos1].score+=5            Joueurs[pos2].score+=0        elif nb1==nb2:            if score1>score2:                Joueurs[pos1].score+=2                Joueurs[pos2].score+=1            else:                Joueurs[pos2].score+=2                Joueurs[pos1].score+=1        else:            Joueurs[pos1].score+=0            Joueurs[pos2].score+=5        Joueurs[pos1].strategieScore+=score1        Joueurs[pos2].strategieScore+=score2        temps=0        changerJoueur()        for inters in lesNoeud:            inters.reInit()    J2.update()    J2.mouvement()    J1.update()    J1.mouvement()    temps+=1