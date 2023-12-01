import math
import pygame
import variables as VAR
import time
from classes.joueurs.joueur import *
from classes.actions.pourchasser import *


class CRaytracing: 
    def __init__(self, moteur):
        self.MOTEUR = moteur
        self.rayons = []
        
        self.distance_max_ref = 300 
        self.amplitude_balancement_ref = 20
        
        self.generation_du_champ_de_vision360()    

        
    def generation_du_champ_de_vision360(self):         
        for angle in range(0, 360): 
            ligne = []               
            for rayon in range(0, self.distance_max_ref):                
                angle2 = (angle*math.pi/180)
                ligne.append( ( int(rayon*math.cos(angle2)), int(rayon*math.sin(angle2))) )
            self.rayons.append(ligne)
            
            
    def afficher(self, personnage):
        if personnage.direction == None : return
        couleur_champ_vision = personnage.couleur_vision
        
        # --- rect de la forme a creer
        
        precision = VAR.precision_champs
        plages = self.calculer_plage_angles(personnage, self.amplitude_balancement_ref, precision) 
        liste_joueurs_detectes, forme, rect_forme = self.generation_du_champs_de_vision(plages, personnage)
        
        if len(liste_joueurs_detectes) > 0:
            couleur_champ_vision = (255, 0, 0, VAR.ray_alpha)            
            personnage.MECANIQUE_ACTION.demarrer(CPourchasser(personnage, liste_joueurs_detectes[0]))
            
                 
        self.dessiner_vision(forme, couleur_champ_vision, rect_forme)
    
    
    
    
    def calculer_plage_angles(self, personnage, amplitude_balancement, precision):        
        
        angle_champs = personnage.direction
        champ_vision = personnage.IA.champ_vision   
        tempo_champ = personnage.tempo
        
        # Calcul du balancement basé sur le tempo et l'amplitude
        balancement = int(amplitude_balancement * math.sin(tempo_champ * math.pi / 10))

        champsDIV2 = (champ_vision // 2)
        plage1 = list(range((angle_champs - champsDIV2 - balancement) , angle_champs, precision))
        plage2 = list(range(angle_champs, (angle_champs + champsDIV2 - balancement), precision))       
        return  [angle % 360 for angle in (plage1 + plage2)]
    

    def detection_joueurs_dans_le_champ(self, zone_du_champ):
        px2, py2 = zone_du_champ 
        liste_joueurs_detectes_dans_cette_zone = []
        
        for joueur in self.MOTEUR.PERSONNAGES.JOUEURS:
            objet_zone_vision = (px2-2, py2-2, 4, 4)
            objet_joueur = (joueur.position_int_x(), joueur.position_int_y()-5, 20, 6)
            joueur_detecte = collision(objet_zone_vision, objet_joueur)
            
            
                         
            # --- demo --- detection (FACULTATIF)
            if VAR.demo == ENUM_DEMO.CHAMP_VISION: 
                if joueur_detecte:   
                    pygame.draw.circle(VAR.fenetre, (255, 0, 0, 255), zone_du_champ, 2)  
                else:
                    pygame.draw.circle(VAR.fenetre, (255, 255, 255, 255), zone_du_champ, 2)  
                
            if joueur_detecte:
                liste_joueurs_detectes_dans_cette_zone.append(joueur)
        
        return liste_joueurs_detectes_dans_cette_zone

    
    def ajuste_dimension_de_la_forme(self, zone_du_champ, rect_figure):
        px2, py2 = zone_du_champ 
        x1, y1, x2, y2 = rect_figure
        
        if VAR.ray_alpha > 0:
            # --- deduction des dimensions de la forme
            if px2 < x1: x1 = px2
            if py2 < y1: y1 = py2
            if px2 > x2: x2 = px2
            if py2 > y2: y2 = py2     
        
        return x1, y1, x2, y2
    
    def detection_decors(self, zone_du_champ, position, maximum):
        px2, py2 = zone_du_champ 
        
        # --- le champs de vision n'est plus dans les limites du terrain
        # --- la zone est libre n'est pas libre
        # --- c'est le dernier element de la liste
        if px2 > -1 and px2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[0] and py2 > -1 and py2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[1] :                    
            if self.MOTEUR.TERRAIN.arrayBlocage[px2, py2] == 0:                           
                if position == maximum:                               
                    return 1     # figure terminée                           
            else:
                return 2    # collision avec decors
        else:
            return 1   # en dehors du terrain
        
        return 0

    
    
                   
    def generation_du_champs_de_vision(self, plages, personnage):
        liste_joueurs_detectes = []
        
        x, y = personnage.x, personnage.y  
        px2, py2 = int(x * VAR.dim) +15 , int(y * VAR.dim) -4  
              
        x1, y1, x2, y2 = 9999, 9999, 0, 0        
        contour = []  
        
        liste_angles = range(0, personnage.distance_vision, VAR.precision_distance)
        nb_zones = len(liste_angles) -1
        for angle in plages: 
 
            i, bord = 0, False         
            for j in liste_angles:
                xx2, yy2 = self.rayons[angle][j]
                
                zone_du_champ = (px2 - xx2, py2 - yy2)                     
                x1, y1, x2, y2 = self.ajuste_dimension_de_la_forme(zone_du_champ, (x1, y1, x2, y2))    
                            
                joueurs_detectes = self.detection_joueurs_dans_le_champ(zone_du_champ)  
                for joueur in joueurs_detectes:
                    if not joueur == None:
                        liste_joueurs_detectes.append(joueur)
                        
                resultat = self.detection_decors(zone_du_champ, i, nb_zones)
                
                bord = (resultat > 0)
                if resultat == 2:                    
                    break
               
                i += 1
              
            if bord: 
                contour.append(zone_du_champ)
                    
        # --- ajoute la position du joueur comme dernier point de la figure (centre du cercle)        
        contour.append((px2 , py2))            
        
        
        # --- retourne la liste des joueurs dans le champs de vision
        return (liste_joueurs_detectes, contour, (x1, y1, x2, y2))
    
    
    
    def dessiner_vision(self, contour_forme, couleur_vision, rect_forme):
        if len(contour_forme) <3:
            return
        
        x1, y1, x2, y2 = rect_forme
        
        # --- dessine avec la transparence
        if VAR.ray_alpha > 0:
            forme_reajustee = []
            for xxx, yyy in contour_forme:
                forme_reajustee.append((xxx - x1, yyy - y1))
                         
                    
            forme_tmp = pygame.Surface((x2 - x1, y2 - y1), pygame.SRCALPHA).convert_alpha()
            pygame.draw.polygon(forme_tmp, couleur_vision, forme_reajustee, 0)    
            pygame.draw.polygon(forme_tmp, (255, 255, 255, 255), forme_reajustee, 2)                 
            VAR.fenetre.blit(forme_tmp, (x1, y1))       
        
        # --- dessine sans transparence    
        else:
            pygame.draw.polygon(VAR.fenetre, couleur_vision, contour_forme, 0) 