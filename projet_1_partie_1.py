from random import random,randint
import math
import matplotlib.pyplot as plt
"""
initialise une liste de paramètres de bernoulis aléatoirement
On l'utilise comme la liste des machines
"""
def initmu(n):
    mu = []
    for i in range(n):
        mu.append(random())
    return mu

T = 80 # nb de partie à jouer CONSTANTE
Mu = initmu(1000) # machine initialisé de taille 1000 CONSTANTE

"""
joue une action en réalisant un tirage de bernouli avec le paramètre correspondant
"""
def jouer(action):
    r = random()
    if r<Mu[action]:
        return 1
    else:
        return 0
"""
Lance une parites de temp T avec la machine Mu et l'algorithme algo
"""   
def run(Mu,algo,T):
    Imax = Mu.index(max(Mu)) # argmax du plus grand Mu
    G = 0 # Gain obtenu en jouent à chaque fois la machine Imax
    r = 0 # la récompense totale
    mu = [0 for e in Mu]# mu[i] := le gain obtenu en jouant la machine i
    Nt = [0 for i in range(len(mu))]# Nt[i] := nb de fois qu'on a joué la machine i
    for i in range(T):
        
        a= algo(mu,Nt)
        r+=jouer(a)
        G+=jouer(Imax)
    return G-r
        
"""
algortithme  aléatoire 
"""
def aleatoire(mu,Nt):
    a = randint(0,len(mu)-1)
    Nt[a]+=1
    r = jouer(a)# joue avec l'action tiré et mets à jour mu (utile pour les explorations)
    mu[a]+=r
    return a

"""
algorithme greedy
"""
def greedy(mu,Nt):
    N = len(mu)
    
    
    # exploration
    for i in range(N):
        aleatoire(mu,Nt)
    
    #calcul de argmax mu^(a)
    mu_max = 0
    a_max = 0
    for i in range(N):
        if Nt[i]==0:
            continue
        else:
            
            if (mu[i]/Nt[i])>mu_max:
                mu_max = mu[i]/Nt[i]
                a_max = i
    return a_max

"""
algorithme E greedy on fixe E = 0.2 ici
"""
def E_greedy(mu,Nt):
    
    N = len(mu)
                                
   
      # exploration
    for i in range(N):
        aleatoire(mu,Nt)
    
    e = random()
    E = 0.2 #epsilon
    if e<E:
        return aleatoire(mu,Nt)
    else:
        mu_max = 0
        a_max = 0
        for i in range(N):
            if Nt[i]==0:
                continue
            else:
                
                if (mu[i]/Nt[i])>mu_max:
                    mu_max = mu[i]/Nt[i]
                    a_max = i
    return a_max
"""
algorithme UCB
"""
def UCB(mu,Nt):
    N = len(mu)
    
     # exploration
    for i in range(N):
        aleatoire(mu,Nt)
        
    t = sum(Nt)
    lgt = math.log(t)
    mu_max = 0
    a_max = 0
    
    # explation
    for i in range(N):
        if Nt[i]==0:
            continue
        else:
            k = mu[i]/Nt[i]+math.sqrt(2*lgt/Nt[i])
            if k>mu_max:
                mu_max = k
                a_max = i
    
    return a_max


    
    
    
    