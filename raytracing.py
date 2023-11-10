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

        for index, xx, yy in self.cercle_COS(0, 0, distance, precision):
            ligne = bresenham((0, 0), (xx, yy), precision).path
            self.rayons.append(ligne)
            
    def cercle_COS(self, centreX, centreY, rayon, precision):
        tmp = []
        for index in range(0, 360, precision):
            angle = (index*math.pi/180)
            tmp.append( (index, centreX + int(rayon*math.cos(angle)), centreY + int(rayon*math.sin(angle))) )
        return tmp
    
    def plage_angles(angle, champs, precision):
        champsDIV2 = (champs // 2)
        plage1 = list(range((angle - champsDIV2) , angle, precision))
        plage2 = list(range(angle, (angle + champsDIV2), precision))       
        return  [angle % 360 for angle in (plage1 + plage2)]
    
           
    def afficher(self, x, y, mode):
        VAR.t_ray = time.time()
        contour = []
       
        # --- limite au champ de vision
        champs = 60   
        precision = 8
        
        if self.MOTEUR.JOUEURS[0].direction == None : return
        plages = raytracing.plage_angles(self.MOTEUR.JOUEURS[0].direction, champs, precision) 
        
        # --- recupere la zone
        for i in plages: 
            liste = self.rayons[i]

            o = 0
            bord = False     
 
            for xx2, yy2 in liste:
                px2, py2 = int(round((x * VAR.dim) - xx2,0)), int(round((y * VAR.dim) - yy2,0))
                
                # --- le champs de vision n'est plus dans les limites du terrain
                # --- la zone est libre n'est pas libre
                # --- c'est le dernier element de la liste
                if px2 > -1 and px2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[0] and py2 > -1 and py2 < self.MOTEUR.TERRAIN.arrayBlocage.shape[1] :
                    
                    if self.MOTEUR.TERRAIN.arrayBlocage[px2, py2] == 255:                           
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
            px2, py2 = ( x * VAR.dim) + 8 , ( y * VAR.dim ) 
            contour.append((px2 , py2))
            pygame.draw.polygon(VAR.fenetre, (0,0,255, 255), contour, 0)
                    
        VAR.t_ray = time.time() - VAR.t_ray