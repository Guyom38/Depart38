import math
import pygame
import variables as VAR
from bresenham import *
import time
from joueur import *

class raytracing: 
    def __init__(self, moteur, distance, precision):
        self.MOTEUR = moteur
        self.rayons = []
        self.distance = distance
        
        for index, xx, yy in self.cercle_COS(0, 0, distance):
            ligne = bresenham((0, 0), (xx, yy), precision).path
            self.rayons.append(ligne)
            
    def cercle_COS(self, centreX, centreY, rayon):
        tmp = []
        for index in range(0, 360):
            angle = (index*math.pi/180)
            tmp.append( (index, centreX + int(rayon*math.cos(angle)), centreY + int(rayon*math.sin(angle))) )
        return tmp
    
    def plage_angles(angle, champs, amplitude_balancement, precision, tempo):        
          
        # Calcul du balancement basé sur le tempo et l'amplitude
        balancement = int(amplitude_balancement * math.sin(tempo * math.pi / 10))

        champsDIV2 = (champs // 2)
        plage1 = list(range((angle - champsDIV2 - balancement) , angle, precision))
        plage2 = list(range(angle, (angle + champsDIV2 - balancement), precision))       
        return  [angle % 360 for angle in (plage1 + plage2)]
    
    

    def afficher(self, personnage):
        x, y = personnage.x, personnage.y
        
        
        contour = []
       
        
        # exemple: 10 degrés de chaque côté
        amplitude_balancement = 20
        # --- limite au champ de vision
        champs = personnage.IA.champs_vision   
        precision = VAR.precision_champs
        
        if personnage.direction == None : return
        plages = raytracing.plage_angles(personnage.direction, champs, amplitude_balancement, precision, personnage.tempo) 
        
        # --- recupere la zone
        for i in plages: 
            liste = self.rayons[i]

            o = 0
            bord = False     
 
            for xx2, yy2 in liste:
                px2, py2 = int(round((x * VAR.dim) - xx2 +15,0)), int(round((y * VAR.dim) - yy2 -4,0))
                
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
                    
        if len(contour) > 2 : 
            px2, py2 = ( x * VAR.dim) +15 , ( y * VAR.dim -4) 
            contour.append((px2 , py2))
            pygame.draw.polygon(VAR.fenetre, personnage.couleur_vision , contour, 0)
                    
       