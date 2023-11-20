import pygame
import xml.etree.ElementTree as XML

import fonctions as FCT
import variables as VAR

class map_tiled:
    def __init__(self, fichier):
        tree = XML.parse(fichier)
        self.root = tree.getroot()
        
        self.fichiers_image = []
        
        # --- Charge les fichiers contenant les images du jeu
        self.chargement_des_fichiers_images()
    
        # --- Cree le terrain pour connaitre les sprites a recuperer
        self.chargement_des_calques()   
        
        self.initialisation_terrain()
        
        
               
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
                                print(index)
                         
    
    
    
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
            
            
    def retourne_images_index(self, index):
        for debut, nombre, colonnes, image in self.fichiers_image:
            if debut <= index < debut+nombre:   
                indexN = index - debut
                y = indexN // colonnes
                x = indexN % colonnes                

                return image.subsurface( (x * 32, y * 32, 32, 32))
        
        image_none = pygame.Surface((32,32))
        pygame.draw.rect(image_none, (255,255,255), (0, 0, 32, 32), 4)
        return image_none
        
           
            
    def initialisation_terrain(self):
        VAR.dimension_x = int(self.root.attrib['width'].replace("'","")) 
        VAR.dimension_y = int(self.root.attrib['height'].replace("'","")) 
        
        self.MAP =  FCT.GenereMat2D(VAR.dimension_x, VAR.dimension_y, 0)
        
        self.planche = pygame.image.load(".ressources/maps.png")
       
    def generer_map(self):
        planche = pygame.Surface((1920, 1080))
 
        for layer in self.root.findall('layer'):
            if not layer.attrib['name'] == "Bloqué":
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
                                    image = VAR.images[index]                                    
                                    planche.blit(image, (x*32, y*32))   
                            x += 1                             
                        y+=1
        
        return planche
    
    def generer_blocage(self):
        bloquage = pygame.Surface((1920, 1080))
 
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
                                    image = VAR.images[index]                                    
                                    bloquage.blit(image, (x*32, y*32))   
                            x += 1                             
                        y+=1
        
        return bloquage