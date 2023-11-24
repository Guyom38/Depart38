from joueur import *
from raytracing import *
import variables as VAR

class CPersonnages:
    def __init__(self, moteur):
        self.moteur = moteur
        self.rays = CRaytracing(moteur)
         
        self.JOUEURS = []
        self.PNJS = []
    
    def se_deplacent(self):
        for personnage in self.JOUEURS + self.PNJS:
            personnage.se_deplace()
    
    def afficher_champs_de_vision(self):
        VAR.timer_ray = time.time()
        for pnj in self.PNJS:
            self.rays.afficher(pnj)  
        VAR.timer_ray = time.time() - VAR.timer_ray    
        
