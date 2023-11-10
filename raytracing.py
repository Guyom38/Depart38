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
    
    def afficher2(self, x, y, mode):
        VAR.t_ray = time.time()
        contour = []
       
        # --- limite au champ de vision
        champs = 60   
        precision = 4
        
        if self.MOTEUR.JOUEURS[0].direction == None : return
        plages = raytracing.plage_angles(self.MOTEUR.JOUEURS[0].direction, champs, precision) 
        
        # --- recupere la zone
        for i in plages: 
            liste = self.rayons[i]

            o = 0
            bord = False
            av = (0, 0)

                
            dim = VAR.dim
            x2, y2 = liste[len(liste)-1]
         
           

           
            d2 = dim //2     
            
            for xx2, yy2 in liste:
                px2, py2 = (( d2 )+( x * dim)) - xx2, ((d2) + ( y * dim )) - yy2
                        
                x2 = int(round(px2 // dim ,0))
                y2 = int(round(py2 // dim, 0))
                
                # --- le champs de vision n'est plus dans les limites du terrain
                # --- la zone est libre n'est pas libre
                # --- c'est le dernier element de la liste
                if x2 > -1 and x2 < len(self.MOTEUR.MAP) and y2 > -1 and y2 < len(self.MOTEUR.MAP[0]):
                    if self.MOTEUR.MAP[x2][y2] == 0:                           
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
            px2, py2 = ( x * dim) + (dim //2), ( y * dim ) + (dim //2)
            contour.append((px2 , py2))
            pygame.draw.polygon(VAR.fenetre, (0,0,255, 255), contour, 0)
                    
        VAR.t_ray = time.time() - VAR.t_ray
        
        
        
        
    def afficher(self, x, y, mode):
        VAR.t_ray = time.time()
        contour = []
       
        # --- limite au champ de vision
        champs = 60   
        
        if self.MOTEUR.JOUEURS[0].direction == None : return
        plages = raytracing.plage_angles(self.MOTEUR.JOUEURS[0].direction, champs, 4) 
        
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
            px2, py2 = ( x * VAR.dim) + (VAR.dim //2), ( y * VAR.dim ) + (VAR.dim //2)
            contour.append((px2 , py2))
            pygame.draw.polygon(VAR.fenetre, (0,0,255, 255), contour, 0)
                    
        VAR.t_ray = time.time() - VAR.t_ray