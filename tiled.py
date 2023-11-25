import pygame
import xml.etree.ElementTree as XML

import fonctions as FCT
import variables as VAR
from objets import *

class map_tiled:
    def __init__(self, moteur, fichier):
        self.MOTEUR = moteur
        
        tree = XML.parse(fichier)
        self.root = tree.getroot()
        
        self.fichiers_image = []
        self.objets = {}
        
        self.planche = pygame.Surface((1920, 1080))
        self.bloquage = pygame.Surface((1920, 1080)).convert_alpha()
        
        # --- Charge les fichiers contenant les images du jeu
        self.chargement_des_fichiers_images()    
        # --- Cree le terrain pour connaitre les sprites a recuperer
        self.chargement_des_calques()   
        
        
        
        
    def chargement_des_fichiers_images(self):
        # --- crée une liste de fichier avec l'index de debut et de fin
        tilesets = self.root.findall('tileset')
        for tileset in tilesets:         
            
            source = tileset.attrib.get('source')         
            xml_fichier_tsx = XML.parse(".ressources/"+source)
            root_fichier_tsx = xml_fichier_tsx.getroot()
            
            firstgid = int(tileset.attrib.get('firstgid'))
            nombre_colonnes = int(root_fichier_tsx.attrib['columns'])
            nombre_tiles = int(root_fichier_tsx.attrib['tilecount'])
            fichier = root_fichier_tsx.find('image').get('source')                                    
            image = pygame.image.load(".ressources/"+fichier).convert_alpha()
            
            self.fichiers_image.append((firstgid, nombre_tiles, nombre_colonnes, image))
               
               
               
               
    # --- Parcours les differentes couches et crée une entrée vide dans le dictionnaire contenant la clé de l'image         
    def chargement_des_calques(self):
        
        # --- Parcours chaque calques de la map
        for layer in self.root.findall('layer'):
            
            data = layer.find('data')
            if data is not None:               
                csv_text = data.text.strip()
                lines = csv_text.split('\n')
                
                # --- Parcours chaque ligne du decors
                for line in lines:
                    tile_ids = line.split(',')    
                    
                    # --- Parcours chaque colonne de la ligne du decors
                    for tile in tile_ids:   
                        index = tile.replace("'","")     
                        
                        if not index == "":
                            index = int(index)           
                            if not index in VAR.images:
                                VAR.images[index] = self.retourne_images_index(index)
                              
    
    
    
    
            
            
    def retourne_images_index(self, index):
        for debut, nombre, colonnes, image in self.fichiers_image:
            etat = C_AUCUN
            
            if debut <= index < debut+nombre:   
                indexN = index - debut
                y = (indexN // colonnes)
                x = (indexN % colonnes)   
                dimX, dimY = VAR.dim, VAR.dim
                                
                if index in LISTE_SCALE_OBJET:
                    coeffX, coeffY, etat = LISTE_SCALE_OBJET[index]
                    if coeffX > 1 or coeffY > 1:
                        y -= (coeffY - 1)                        
                        dimX = (coeffX * VAR.dim)
                        dimY = (coeffY * VAR.dim)                             

                return (image.subsurface( (x * VAR.dim, y * VAR.dim, dimX, dimY)), etat)
        
        return "index introuvable"

        
           
            
    
    def generer_parcours_PNJ(self):
        parcours = {}
        for layer in self.root.findall('layer'):
            if layer.attrib['name'].startswith("Chemin"):
                data = layer.find('data')
                if data is not None:              
                  
                    grille_parcours = FCT.GenereMat2D(VAR.dimension_x, VAR.dimension_y, 0)
                    liste_positions_pnjs = []
                    
                    csv_text = data.text.strip()
                    lines = csv_text.split('\n')
                    y = 0
                    for line in lines:
                        x = 0
                        tile_ids = line.split(',')   
                        #print(line)
                        for tile in tile_ids:                              
                            index = tile.replace("'","")     
                            
                            if not index == "":
                                grille_parcours[x][y] = {}
                                grille_parcours[x][y]['CHEMIN'] = ( int(index) > 0 ) 
                                grille_parcours[x][y]['UTILISE'] = 0 
                                
                                if int(index) == 17106: liste_positions_pnjs.append( (x, y) )
                            x += 1
                        y += 1
                    
                    parcours[layer.attrib['name']] = {}
                    parcours[layer.attrib['name']]['GRILLE'] = grille_parcours 
                    parcours[layer.attrib['name']]['DEPART'] = liste_positions_pnjs
        return parcours
                
    def generer_map(self):
        
        
        c = 0
        for layer in self.root.findall('layer'):
            if not layer.attrib['name'] == "Bloqué": # and not layer.attrib['name'].startswith("Chemin"):
                data = layer.find('data')
                if data is not None:               
                    csv_text = data.text.strip()
                    lines = csv_text.split('\n')
                    y = 0
                    for line in lines:
                        x = 0
                        tile_ids = line.split(',')   
                        
                        for tile in tile_ids:                              
                            index = tile.replace("'","")     
                            
                            if not index == "":
                                index = int(index)   
                                if index > 0:  
                                    
                                    if layer.attrib['name'] in ("Sol", "Mur"): 
                                        image, traversable = VAR.images[index]                                                                                                        
                                        self.planche.blit(image, (x * VAR.dim, y * VAR.dim))  
                                         
                                    else:
                                        # --- ajoute a la liste des objets a afficher avec une priorité
                                        objet = self.MOTEUR.ELEMENTS_VISUELS.traitement_objet(index, x, y, c, (layer.attrib['name'] in ("Decors", "Derriere_Meuble", "Devant_Meuble")))
                                        
                                        # --- integration a la zone bloquée
                                        if (not objet == None) and (objet.etat == C_OBSTACLE):
                                            objet.afficher(self.bloquage)
                                            
                            x += 1                             
                        y+=1
            c+=1
        return self.planche
    
    def generer_png_blocage(self):   
        for layer in self.root.findall('layer'):
            if layer.attrib['name'] == "Bloqué":
                data = layer.find('data')
                if data is not None:               
                    csv_text = data.text.strip()
                    lines = csv_text.split('\n')
                    x, y = 0, 0
                    for line in lines:
                        x = 0
                        tile_ids = line.split(',')   
                        
                        for tile in tile_ids:                              
                            index = tile.replace("'","")     
                            
                            if not index == "":
                                index = int(index)   
                                if index > 0:
                                    image, traversable = VAR.images[index]                                    
                                    self.bloquage.blit(image, (x * VAR.dim, y * VAR.dim))   
                            x += 1                             
                        y+=1
        
        return self.bloquage