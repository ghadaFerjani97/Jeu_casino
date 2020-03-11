import tictactoe_etu as ttt
import math 
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Node:
    """
    class qui implemente un noeud de l'arbre de UCT
    """
    # gain := le nb victoires
    # n := le nb de fois l'action est choisi
    # action := l'action de ce noeud
    # state := etat actuel du jeu
    # peres := une liste des noeuds peres
    # fils := une liste des noeuds fils
    # feuille := boolean qui indique si on ne peut plus explorer
    
    def __init__(self,action,state):
        self.action = action
        self.peres = []
        self.fils = []
        self.state = state
        self.gain = 0
        self.n = 0
        self.final = False
    
    def addFils(self,noeud): #ajoute un fils au noeud courant
        noeud.peres.append(self)
        self.fils.append(noeud)
        noeud.final = noeud.state.stop()
    
   
    """
    fonction qui réalise la phase de selection ( les phases de expansion, simulation, 
    propagation sont automatiques après l'appel de cette fonction)
    """
    def selection(self): 
        if self.final==True:
            self.propagation(1,self.state.win())
        elif len(self.state.get_actions())-len(self.fils)>0:
            self.expansion()
        else: 
            
            f_max = None
            crit_max = 0
            for f in self.fils:
                n = f.n
                gain = f.gain
                N = self.n
                c = gain/n+math.sqrt(2*math.log(N)/n) # critere de UCB
                if c>crit_max:
                    crit_max = c
                    f_max = f
            f.selection()
        
    """
    fonction qui réalise la phase expansion ( les phases de simulation et 
    propagation automatiques après l'appel de cette fonction)
    """
    def expansion(self):
        a_dispo = self.state.get_actions()
        actions_fils = []
        for f in self.fils:
            actions_fils.append(f.action)
        
        for a in a_dispo:
            if a not in actions_fils:
                nde = Node(a,self.state.next(a))
                self.addFils(nde)
                nde.simulation()
                
                
    """
    fonction qui réalise la phase de simulation (la simulation est automatique après l'appel de cette fonction)
    """            
    def simulation(self):        self.fils = []
        self.state = state
        self.gain = 0
        self.n = 0
        self.final = False
    
    def addFils(self,noeud): #ajoute un fils au noeud courant
        noeud.peres.append(self)
        self.fils.append(noeud)
        noeud.final = noeud.state.stop()
    
   
    """
    fonction qui réalise la phase de selection ( les phases de expansion, simulation, 
    propagation sont automatiques après l'appel de cette fonction)
    """
    def selection(self): 
        if self.final==True:
            self.propagation(1,self.state.win())
        elif len(self.state.get_actions())-len(self.fils)>0:
            self.expansion()
        else: 
            
            f_max = None
            crit_max = 0
            for f in self.fils:
                n = f.n
                gain = f.gain
                N = self.n
                c = gain/n+math.sqrt(2*math.log(N)/n) # critere de UCB
                if c>crit_max:
                    crit_max = c
                    f_max = f
        j1 = ttt.Joueur_aleatoire()
        j2 = ttt.Joueur_aleatoire()
        jCourant = self.state.courant
        jeu = ttt.Jeu(self.state,j1,j2)
        win, log = jeu.run()
        g = 0
        if win==(-jCourant):
            g=1
        self.propagation(g,win)
        
    """
    fonction qui réalise la phase de propagation des gains.
    la augmente le gain sur le noeud correpondant au joueur gagnant uniquement
    """
    def propagation(self,g,gagnant):
       
        if self.state.courant==(-gagnant):
            self.gain+=g
        self.n+=1
        for dad in self.peres:
            dad.propagation(g,gagnant)
    """
    renvoie le fils avec la meilleure moyenne de récompense
    """
    def fils_optimal(self):
        f_max = None
        m_max = 0 
        for f in self.fils:
            m = f.gain/f.n
            if m>m_max:
                f_max = f
                m = m_max
        return f_max

class Arbre:
    N = 18 # 2 fois la taille de la grille
    def __init__(self,racine):
        self.racine = racine
        
    """
    l'arbre sera remplacé par le sous arbre du noeud fils dont l'état est l'état state
    """
    def update_racine(self,state):
        act_state = state.get_actions()
        for f in self.racine.fils:
            act_f = f.state.get_actions()
            equal = True
            for a in act_f:
                if a not in act_state:
                    equal=False
            if equal==True:
                self.racine = f
                break
            
    """
    renvoie le fils de la racine ayant la mailleure moyenne de récompense
    """
    def get_fils_optimal(self):
        for i in range(self.N):
            self.racine.selection()
        return self.racine.fils_optimal()

class Joueur_UCT(ttt.Agent):
    def __init__(self):
        self.tree = Arbre(Node(None,None)) # Arbre avec une racine vide.
    def get_action(self,state):
#        
        if self.tree.racine.state==None: # initialise la racine de l'arbre au début du jeu
            self.tree.racine.state = state
        else:
            self.tree.update_racine(state)
        f_max = self.tree.get_fils_optimal()
        if f_max==None:
            return None
        action = f_max.action
        self.tree.update_racine(state.next(action))
        return action
            
