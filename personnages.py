from joueur import *
from raytracing import *
import variables as VAR

class CPersonnages:
    def __init__(self, moteur):
        self.moteur = moteur
        
        self.JOUEURS = []
        self.PNJS = []
        
        self.rays = {}
    
    def se_deplacent(self):
        for personnage in self.JOUEURS + self.PNJS:
            personnage.se_deplace()
    
    def afficher_visions(self):
        VAR.timer_ray = time.time()
        for pnj in self.PNJS:
            self.rays[pnj.fonction].afficher(pnj) 
        VAR.timer_ray = time.time() - VAR.timer_ray    
        
