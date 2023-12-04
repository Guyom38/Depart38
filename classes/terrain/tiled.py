import pygame
import xml.etree.ElementTree as XML

import fonctions as FCT
import variables as VAR
from objets import *
import os

import classes.terrain.tiled_images as TI

class map_tiled:
    def __init__(self, moteur):
        self.MOTEUR = moteur
        
        self.root = None     
          
        # --- couche primaire a afficher a l'écran
        self.planche = None
        
        # --- bitmap de collision
        self.bloquage = None
    
    
     
    def lecture_du_fichier_Tiled(self, fichier):
        
        donnees_xml = XML.parse(fichier)
        self.root = donnees_xml.getroot()   
        
        TI.etape1_chargement_des_fichiers_images(self)  
        TI.etape2_chargement_des_images_necessaires_a_la_map(self)   
        
        VAR.dimension_x = int(self.root.attrib['width'].replace("'","")  )
        VAR.dimension_y = int(self.root.attrib['height'].replace("'","")  )
        
        self.initialisation_des_bitmaps()
        
        c = 0
        for layer in self.root.findall('layer'): 
        
            data = layer.find('data')
            if data is not None:               
                csv_text = data.text.strip()
                lignes = csv_text.split('\n')
                y = 0
                for ligne in lignes:
                    x = 0
                    lignes_index = ligne.replace("'","").split(',')   
                    for index in lignes_index: 
                        if not index == "":
                            index = int(index)   
                            if index > 0:
                                objet = None
                                
                                if not layer.attrib['name'] == "Bloqué":
                                    if not index in VAR.LISTE_IMAGES_IGNOREES:                                       
                                        if layer.attrib['name'] in ("Sol"):
                                            self.creation_couche_primaire(index, x, y)
                                        else:
                                            objet = self.analyse_couches_decors(c, layer, index, x, y, ("Decors", "Derriere_Meuble", "Devant_Meuble", "Ordinateur", "Mur"))
                                            
                                else:      
                                    self.creation_couches_collision(index, x, y)
                                            
                                if (not objet == None and objet.etat == C_OBSTACLE):
                                    self.ajouter_objet_a_la_couches_collision(objet)
                        x += 1                             
                    y+=1
            c+=1
        return self.planche, self.bloquage

    
    def initialisation_des_bitmaps(self):
         # --- couche primaire a afficher a l'écran
        self.planche = pygame.Surface((VAR.resolution_x, VAR.resolution_y))
        
        # --- bitmap de collision
        self.bloquage = pygame.Surface((VAR.resolution_x, VAR.resolution_y)).convert_alpha()
        
        
    def creation_couche_primaire(self, index, x, y):        
        image, image_mask, traversable = VAR.images[index]                                                                                                        
        self.planche.blit(image[0], (x * VAR.dim, y * VAR.dim)) 
            
    def analyse_couches_decors(self, c, layer, index, x, y, liste_couches_obstacles):                          
        considere_obstacle = (layer.attrib['name'] in liste_couches_obstacles)
        objet = self.MOTEUR.ELEMENTS_VISUELS.traitement_objet(index, x, y, c, considere_obstacle)           
        return objet
    
    def creation_couches_collision(self, index, x, y):
        image, image_mask, traversable = VAR.images[index] 
        image_a_utilisee = image if image_mask == None else image_mask                                   
        self.bloquage.blit(image_a_utilisee, (x * VAR.dim, y * VAR.dim))   
                                               
    def ajouter_objet_a_la_couches_collision(self, objet):
        image_a_utlisee = objet.image[0] if objet.image_mask == None else objet.image_mask
        self.bloquage.blit(image_a_utlisee, (objet.position_ecran_x(), objet.position_ecran_y()))
                                            

        
   