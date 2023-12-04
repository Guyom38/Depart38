import pygame
from pygame.locals import *

import time, random

import variables as VAR
from fonctions import *

from constantes import *
from classes.actions.courrir import *
from classes.joueurs.joueur import *

class CManettes():
    def __init__(self, controlleurs):
        self.MOTEUR = controlleurs.MOTEUR
        self.CONTROLLEURS = controlleurs
        self.PERSONNAGES = self.MOTEUR.PERSONNAGES

        self.MANETTES = {}
        
        pygame.joystick.init()        
        self.nombre_manettes = pygame.joystick.get_count() 
        print(str(self.nombre_manettes) + " manettes trouvées")
        
        if self.nombre_manettes > 0:
            self.CONTROLLEURS.ASSOC_MANETTE_JOUEUR[0] = self.PERSONNAGES.JOUEURS[0] 
            self.MANETTES[0] = pygame.joystick.Joystick(0)
            self.MANETTES[0].init()   
            print("Manette "+str(0)+" :", self.MANETTES[0].get_name())
            
        for i in range(1, self.nombre_manettes):
            self.joueur_derriere_manette(i)
            self.MANETTES[i] = pygame.joystick.Joystick(i)
            self.MANETTES[i].init()            
            print("Manette "+str(i)+" :", self.MANETTES[i].get_name())
    
    
    def joueur_derriere_manette(self, id_manette):        
        if id_manette not in self.CONTROLLEURS.ASSOC_MANETTE_JOUEUR: 
            nouveau_joueur = CJoueur(self.MOTEUR, id_manette, 2.0 + random.randint(0, 6), 6.0 + random.randint(0, 3), "Guyom #"+str(id_manette), False)
            
            self.PERSONNAGES.JOUEURS.append(nouveau_joueur)
            self.CONTROLLEURS.ASSOC_MANETTE_JOUEUR[id_manette] = nouveau_joueur   
                 
        return id_manette, self.CONTROLLEURS.ASSOC_MANETTE_JOUEUR[id_manette]  
      
      
      
    def gestion_des_evenements(self, event):
        joueur_zero_bouge = 0
        
        id_manette, joueur = self.joueur_derriere_manette(event.joy)

        if event.type == pygame.JOYAXISMOTION:  
            print("EVENEMENT CAPTURE : " + str(event))   
                   
            if event.axis == 0:
                if event.value < -0.5: 
                    joueur.direction, joueur.en_mouvement = ENUM_DIR.GAUCHE, True
                elif event.value > 0.5:                     
                    joueur.direction, joueur.en_mouvement = ENUM_DIR.DROITE, True
                else:
                    joueur.en_mouvement = False
                    
            if event.axis == 1:  
                if event.value > 0.5: 
                    joueur.direction, joueur.en_mouvement = ENUM_DIR.BAS, True
                elif event.value < -0.5 :                     
                    joueur.direction, joueur.en_mouvement = ENUM_DIR.HAUT, True
                else:
                    joueur.en_mouvement = False
                        
        elif event.type == pygame.JOYBUTTONDOWN :                    
            if event.button == CBouton.B_A:  pass
            if event.button == CBouton.B_B:  pass
            if event.button == CBouton.B_X:  pass
            if event.button == CBouton.B_Y:  pass
            if event.button == CBouton.B_START:  pass
            if event.button == CBouton.B_SELECT: pass
 
        elif event.type == pygame.JOYBUTTONUP:      
            if event.button == CBouton.B_A:  pass
            if event.button == CBouton.B_B:  pass
            if event.button == CBouton.B_X:  pass
            if event.button == CBouton.B_Y:  pass
            if event.button == CBouton.B_START:   pass
            if event.button == CBouton.B_SELECT:  pass

        if id_manette == 0 and joueur.en_mouvement:
            joueur_zero_bouge += 1
            
        return joueur_zero_bouge
            
