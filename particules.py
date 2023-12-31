import pygame
from pygame.locals import *
import variables as VAR
import random

class CParticules:
    def __init__(self, _moteur):
        self.MOTEUR = _moteur    
        self.LISTE = []    
        
    def Cercle_Surface(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def Ajouter_Particule(self, _x, _y, _couleur):
        position = [_x, _y]
        sens_projection = [0, 0] #[random.randint(0, 20) / 10 - 1, -5]
        rayon = 8 #random.randint(0, VAR.dim/4)
        self.LISTE.append([position, sens_projection, rayon, _couleur])
        
    def Afficher_Les_Particules(self):       
        for particle in self.LISTE:
          
            
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]            
            if not particle[1][1] == 0:
                particle[1][1] += 0.15
            particle[2] -= 0.46
            pygame.draw.circle(VAR.fenetre, particle[3], [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

            radius = particle[2] * 1.5
            VAR.fenetre.blit(self.Cercle_Surface(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)

            if particle[2] <= 0:
                self.LISTE.remove(particle)
                
    
