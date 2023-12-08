import pygame
import xml.etree.ElementTree as XML

import fonctions as FCT
import variables as VAR
from classes.moteur.objets import *
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
    
    
    def initialise_index_fichiers(self):
        
        # <tileset firstgid="289" source="32/Modern_Office_Black_Shadow_32x32.tsx"/>
        for fichier_index in self.root.findall('tileset'):
            index = int(fichier_index.attrib['firstgid'])
            fichier = fichier_index.attrib['source']
            
            print ("   + Fichier tileset : " + fichier + " (" + str(index) + ")")
            if "Interiors" in fichier:
                VAR.C_INTERIOR = index
            elif "mecanique" in fichier:
                VAR.C_MECANIQUE = index
            elif "Exteriors" in fichier:
                VAR.C_MODERN_EXTERIORS = index
            elif "Modern_Office" in fichier:
                VAR.C_MODERN_OFFICE = index
            elif "Builder_Office_32x32" in fichier:
                VAR.C_ROOM_BUILDER_OFFICE = index
            elif "Builder_32x32":
                VAR.C_ROOM_BUILDER = index
            else:
                print ("/!\ Manque fichier tileset " + str(fichier, index))
        
        self.MOTEUR.ELEMENTS_VISUELS.BDD_OBJETS.initialiser_objets()
        self.MOTEUR.ELEMENTS_VISUELS.initialiser_les_objets_particulier()
        
    def lecture_du_fichier_Tiled(self, fichier):
        
        donnees_xml = XML.parse(fichier)
        self.root = donnees_xml.getroot()   
        
        self.initialise_index_fichiers()
        
        
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
                                

                                if not index in VAR.LISTE_IMAGES_IGNOREES:                                       
                                    if layer.attrib['name'] in ("Sol", "Ombre"):
                                        self.creation_couche_primaire(index, x, y)
                                    else:
                                        objet = self.analyse_couches_decors(c, layer, index, x, y, ("0", "1", "2", "3", "4", "5", "6", "7", "Mur"))
    
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
                                               
    def ajouter_objet_a_la_couches_collision(self, objet):
        image_a_utlisee = objet.image[0] if objet.image_mask == None else objet.image_mask
        self.bloquage.blit(image_a_utlisee, (objet.position_pixel_x(), objet.position_pixel_y()))
                                            

        
   