import pygame
import variables as VAR
import fonctions as FCT

from classes.joueurs.joueur import *


def niveau_jeu(moteur):
    VAR.fichier_map = "map"
    
    PERSONNAGES = moteur.PERSONNAGES
    PERSONNAGES.JOUEURS.append(CJoueur(moteur, 0, 6.0, 6.0, "Guyom", False)) 
    PERSONNAGES.JOUEURS[0].changement_equipe(2)
    
    PERSONNAGES.PNJS.append(CJoueur(moteur, 1, 1.0, 5.0, "Vincent", True, 0))
    PERSONNAGES.PNJS.append(CJoueur(moteur, 2, 1.0, 5.0, "Basile", True,2))
    PERSONNAGES.PNJS.append(CJoueur(moteur, 3, 1.0, 5.0, "Luc", True, 2))
    PERSONNAGES.PNJS.append(CJoueur(moteur, 4, 1.0, 5.0, "Emmanuel", True, 2))
    PERSONNAGES.PNJS.append(CJoueur(moteur, 5, 1.0, 5.0, "Stevan", True, 2))    