from classes.joueurs.joueur import *
from classes.joueurs.raytracing import *
from classes.joueurs.pathfinding import *

import variables as VAR

class CPersonnages:
    def __init__(self, moteur):
        self.moteur = moteur
        
        self.RAYS = CRaytracing(moteur)
        self.PATHFINDING = CPathfinding(moteur)
                
        self.JOUEURS = []
        self.PNJS = []
    
    
    def afficher_effets_joueurs(self):
        t = time.time()
        for joueur in self.JOUEURS:
            joueur.afficher_ombre()
            
        for pnj in self.PNJS:
            pnj.afficher_ombre()
            pnj.afficher_champ_vision()
        FCT.Performance('PERSONNAGES.afficher_champs_vision()+ombres', t)    
            
            
    def se_deplacent(self):
        t = time.time()
        for personnage in self.JOUEURS + self.PNJS:
            personnage.se_deplace() 
            
            if personnage.animation == ENUM_ANIMATION.COURIR:                   
                personnage.afficher_fumee()
            
        FCT.Performance('PERSONNAGES.se_deplacent()', t)
            
    

