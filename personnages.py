from joueur import *
from raytracing import *
from pathfinding import *

import variables as VAR

class CPersonnages:
    def __init__(self, moteur):
        self.moteur = moteur
        
        self.RAYS = CRaytracing(moteur)
        self.PATHFINDING = CPathfinding(moteur)
                
        self.JOUEURS = []
        self.PNJS = []
    
    def se_deplacent(self):
        t = time.time()
        for personnage in self.JOUEURS + self.PNJS:
            personnage.se_deplace() 
            
            if personnage.action == ENUM_ANIMATION.COURIR:                   
                personnage.afficher_fumee()
            
        FCT.Performance('JOUEURS.se_deplacent()', t)
            
    

