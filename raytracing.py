import math
import pygame
import variables as VAR
from bresenham import *
import time
from joueur import *

class CRaytracing: 
    def __init__(self, moteur, distance, precision):
        self.MOTEUR = moteur
        self.rayons = []
        self.distance = distance
        
        for index, xx, yy in self.calculer_points_cercle(0, 0, distance):
            ligne = bresenham((0, 0), (xx, yy), precision).path
            self.rayons.append(ligne)
            
    def calculer_points_cercle(self, centreX, centreY, rayon):
        tmp = []
        for index in range(0, 360):
            angle = (index*math.pi/180)
            tmp.append( (index, centreX + int(rayon*math.cos(angle)), centreY + int(rayon*math.sin(angle))) )
        return tmp
    
    def calculer_plage_angles(self, angle, champs, amplitude_balancement, precision, tempo):        
          
        # Calcul du balancement basé sur le tempo et l'amplitude
        balancement = int(amplitude_balancement * math.sin(tempo * math.pi / 10))

        champsDIV2 = (champs // 2)
        plage1 = list(range((angle - champsDIV2 - balancement) , angle, precision))
        plage2 = list(range(angle, (angle + champsDIV2 - balancement), precision))       
        return  [angle % 360 for angle in (plage1 + plage2)]
    
    

    def afficher(self, personnage):
        # --- rect de la forme a creer
        x1, y1, x2, y2 = 9999, 9999, 0, 0
        
        x, y = personnage.x, personnage.y                
        contour = []       
        liste_joueurs_detectes = []
        
        precision = VAR.precision_champs
        couleur_champ_vision = personnage.couleur_vision
        
        # exemple: 10 degrés de chaque côté
        amplitude_balancement = 20
        champ = personnage.IA.champ_vision   
        
        
        
        if personnage.direction == None : return
        plages = self.calculer_plage_angles(personnage.direction, champ, amplitude_balancement, precision, personnage.tempo) 
        
        # --- recupere la zone
        for i in plages: 
            liste = self.rayons[i]
            o, bord = 0, False              
 
            for xx2, yy2 in liste:
                px2, py2 = int(round((x * VAR.dim) - xx2 +15, 0)), int(round((y * VAR.dim) - yy2 -4, 0))
                     
                if 1 == 1:
                    for joueur in self.MOTEUR.PERSONNAGES.JOUEURS:
                        objet_zone_vision = (px2-2, py2-2, 4, 4)
                        objet_joueur = (joueur.position_int_x(), joueur.position_int_y()-5, 20, 6)
                        if collision(objet_zone_vision, objet_joueur):
                            if not joueur in liste_joueurs_detectes:
                                liste_joueurs_detectes.append(joueur)
                                couleur_champ_vision = (255, 0, 0, VAR.ray_alpha)
                            
                        #    pygame.draw.circle(VAR.fenetre, (255, 0, 0, 255), (px2, py2), 2)  
                        #else:
                        #    pygame.draw.circle(VAR.fenetre, (255, 255, 255, 255), (px2, py2), 2)  
                   
                
                if VAR.ray_alpha > 0:
                    # --- deduction des dimensions de la forme
                    if px2 < x1: x1 = px2
                    if py2 < y1: y1 = py2
                    if px2 > x2: x2 = px2
                    if py2 > y2: y2 = py2
                
                # --- le champs de vision n'est plus dans les limites du terrain
                # --- la zone est libre n'est pas libre
                # --- c'est le dernier element de la liste
                if px2 > -1 and px2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[0] and py2 > -1 and py2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[1] :                    
                    if self.MOTEUR.TERRAIN.arrayBlocage[px2, py2] == 0:                           
                        if o == len(liste)-1:                               
                            bord = True                                
                    else:
                        bord = True
                        break
                else:
                    bord = True

                o=o+1
              
            if bord: 
                contour.append((px2 , py2))
                    
        if len(contour) < 3 : 
            return []
        
        # --- ajoute la position du joueur comme dernier point de la figure (centre du cercle)
        px2, py2 = ( x * VAR.dim) +15 , ( y * VAR.dim -4) 
        contour.append((px2 , py2))
            
        self.dessiner_vision(contour, couleur_champ_vision, x1, y1, x2, y2)
        
        # --- retourne la liste des joueurs dans le champs de vision
        return liste_joueurs_detectes
    
    
    
    def dessiner_vision(self, contour, couleur_vision, x1, y1, x2, y2):
        # --- dessine avec la transparence
        if VAR.ray_alpha > 0:
            forme_reajustee = []
            for xxx, yyy in contour:
                forme_reajustee.append((xxx - x1, yyy - y1))
                         
                    
            forme_tmp = pygame.Surface((x2 - x1, y2 - y1), pygame.SRCALPHA).convert_alpha()
            pygame.draw.polygon(forme_tmp, couleur_vision, forme_reajustee, 0)    
            pygame.draw.polygon(forme_tmp, (255, 255, 255, 255), forme_reajustee, 2)                 
            VAR.fenetre.blit(forme_tmp, (x1, y1))       
        
        # --- dessine sans transparence    
        else:
            pygame.draw.polygon(VAR.fenetre, couleur_vision, contour, 0) 