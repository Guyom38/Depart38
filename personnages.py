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
        self.PATHFINDING.course_poursuite_contre_le_joueur(1)            
            
        for personnage in self.JOUEURS + self.PNJS:
            personnage.reflechit()            
            personnage.se_deplace()   
            #personnage.PATHFINDING.afficher()         
            personnage.afficher_fumee()
            
    

