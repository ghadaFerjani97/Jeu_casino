import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint

## Constante
OFFSET = 0.2


class State:
    """ Etat generique d'un jeu de plateau. Le plateau est represente par une matrice de taille NX,NY,
    le joueur courant par 1 ou -1. Une case a 0 correspond a une case libre.
    * next(self,coup) : fait jouer le joueur courant le coup.
    * get_actions(self) : renvoie les coups possibles
    * win(self) : rend 1 si le joueur 1 a gagne, -1 si le joueur 2 a gagne, 0 sinon
    * stop(self) : rend vrai si le jeu est fini.
    * fonction de hashage : renvoie un couple (matrice applatie des cases, joueur courant).
    """
    NX,NY = None,None
    def __init__(self,grid=None,courant=None):
        self.grid = copy.deepcopy(grid) if grid is not None else np.zeros((self.NX,self.NY),dtype="int")
        self.courant = courant or 1
    def next(self,coup):
        pass
    def get_actions(self):
        pass
    def win(self):
        pass
    def stop(self):
        pass
    @classmethod
    def fromHash(cls,hash):
        return cls(np.array([int(i)-1 for i in list(hash[0])],dtype="int").reshape((cls.NX,cls.NY)),hash[1])
    def hash(self):
        return ("".join(str(x+1) for x in self.grid.flat),self.courant)
    
            
class Jeu:
    """ Jeu generique, qui prend un etat initial et deux joueurs.
        run(self,draw,pause): permet de joueur une partie, avec ou sans affichage, avec une pause entre chaque coup. 
                Rend le joueur qui a gagne et log de la partie a la fin.
        replay(self,log): permet de rejouer un log
    """
    def __init__(self,init_state = None,j1=None,j2=None):
        self.joueurs = {1:j1,-1:j2}
        self.state = copy.deepcopy(init_state)
        self.log = None
    def run(self,draw=False,pause=0.5):
        log = []
        if draw:
            self.init_graph()
        while not self.state.stop():
            coup = self.joueurs[self.state.courant].get_action(self.state)
            log.append((self.state,coup))
            self.state = self.state.next(coup)
            if draw:
                self.draw(self.state.courant*-1,coup)
                plt.pause(pause)
        return self.state.win(),log
    def init_graph(self):
        self._dx,self._dy  = 1./self.state.NX,1./self.state.NY
        self.fig, self.ax = plt.subplots()
        for i in range(self.state.grid.shape[0]):
            for j in range(self.state.grid.shape[1]):
                self.ax.add_patch(patches.Rectangle((i*self._dx,j*self._dy),self._dx,self._dy,\
                        linewidth=1,fill=False,color="black"))
        plt.show(block=False)
    def draw(self,joueur,coup):
        color = "red" if joueur>0 else "blue"
        self.ax.add_patch(patches.Rectangle(((coup[0]+OFFSET)*self._dx,(coup[1]+OFFSET)*self._dy),\
                        self._dx*(1-2*OFFSET),self._dy*(1-2*OFFSET),linewidth=1,fill=True,color=color))
        plt.draw()
    def replay(self,log,pause=0.5):
        self.init_graph()
        for state,coup in log:
            self.draw(state.courant,coup)
            plt.pause(pause)

class MorpionState(State):
    """ Implementation d'un etat du jeu du Morpion. Grille de 3X3. 
    """
    NX,NY = 3,3
    def __init__(self,grid=None,courant=None):
        super(MorpionState,self).__init__(grid,courant)
    def next(self,coup):
        state =  MorpionState(self.grid,self.courant)
        state.grid[coup]=self.courant
        state.courant *=-1
        return state
    def get_actions(self):
        return list(zip(*np.where(self.grid==0)))
    def win(self):
        for i in [-1,1]:
            if ((i*self.grid.sum(0))).max()==3 or ((i*self.grid.sum(1))).max()==3 or ((i*self.grid)).trace().max()==3 or ((i*np.fliplr(self.grid))).trace().max()==3: return i
        return 0
    def stop(self):
        return self.win()!=0 or (self.grid==0).sum()==0
    def __repr__(self):
        return str(self.hash())

class Agent:
    """ Classe d'agent generique. Necessite une methode get_action qui renvoie l'action correspondant a l'etat du jeu state"""
    def __init__(self):
        pass
    def get_action(self,state):
        pass


class Joueur_aleatoire(Agent):        
    def get_action(self,state):
        cases_vides = state.get_actions()
        n=len(cases_vides)
        action=cases_vides[randint(0,n-1)]
        return action 
    

class Joueur_montecarlo(Agent):
    def get_action(self,state):
        nx=state.NX
        ny=state.NY
        rec=[[0 for j in range(ny)]for i in range(nx)] # matrice de recompense pour chaque cases (actions)
        nt = [[0 for j in range(ny)]for i in range(nx)]# nombre de fois ou chaque case à été choisi
        N = nx*ny # N = la taille de la grille
        cases_vides = state.get_actions()
        for action in cases_vides:# joue N parties aleatoires pour chaque action possible
             joueur_courant = state.courant
             etat_test = state.next(action)
             for i in range(N):
           
                 nt[action[0]][action[1]]+=1
                
                
                 j1 = Joueur_aleatoire()
                 j2 = Joueur_aleatoire()
                 jeu = Jeu(etat_test,j1,j2)
                 win,log=jeu.run()
                 if win==joueur_courant:
                   rec[action[0]][action[1]]+=1
        
        indexMax = (0,0)
        moyMax = 0
        for i in range(nx): # cherche l'action avec la meilleure moyenne de réussite
            for j in range(ny):
                if nt[i][j]==0:
                    continue
                else:
                    k = rec[i][j]/nt[i][j]
                    if k>moyMax:
                        indexMax = (i,j)
                        moyMax = k
        return indexMax
            
            
"""
teste le taux de réussite du joueur 1 après N parties
"""  
def test(j1,j2,N):
    pointsJ1 = 0
    pointsJ2 = 0
    n=1
    
    PJ1_ = []
    PJ2_ = []
    
    for i in range(N):
        morpion = MorpionState()
    
        jeu = Jeu(morpion,j1,j2)
        win,log = jeu.run()
        if win==1:
            pointsJ1+=1
        elif win==-1:
            pointsJ2+=1
        PJ1_.append(pointsJ1/n)
        PJ2_.append(pointsJ2/n)
        n+=1
        
    plt.plot(list(range(N)),PJ1_,label = "joueur 1")
    plt.plot(list(range(N)),PJ2_,label="joueur 2")
    plt.xlabel("le nombre de tests")
    plt.ylabel("la moyenne de réussite")
    plt.legend()


