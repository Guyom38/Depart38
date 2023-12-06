import pygame
import variables as VAR
import fonctions as FCT

from classes.joueurs.joueur import *

def niveau_salle_attente(moteur):
    VAR.fichier_map = "depart"
    moteur.PERSONNAGES.JOUEURS.append(CJoueur(moteur, 0, 37.0, 35.0, "Guyom", False))    
        
    