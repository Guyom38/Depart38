import pygame
import xml.etree.ElementTree as XML

import fonctions as FCT
import variables as VAR
import objets as OBJS

class map_tiled:
    def __init__(self, moteur, fichier):
        self.MOTEUR = moteur
        
        tree = XML.parse(fichier)
        self.root = tree.getroot()
        
        self.fichiers_image = []
        self.objets = {}
        
        # --- Charge les fichiers contenant les images du jeu
        self.chargement_des_fichiers_images()
    
        # --- Cree le terrain pour connaitre les sprites a recuperer
        self.chargement_des_calques()   
        
        
        
               
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
                dimX, dimY = 32, 32
                
                if indexN in OBJS.LISTE_OBJ_DOUBLE_HAUTEUR:
                    y -= 1
                    dimY = 64                             

                return (indexN, image.subsurface( (x * 32, y * 32, dimX, dimY)))
        
        image_none = pygame.Surface((32,32))
        pygame.draw.rect(image_none, (255,255,255), (0, 0, 32, 32), 4)
        return (0, image_none)
        
           
            
   
       
    def generer_map(self):
        planche = pygame.Surface((1920, 1080))
        
        c = 0
        for layer in self.root.findall('layer'):
            if not layer.attrib['name'] == "Bloqué":
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
                                        indexOrigine, image = VAR.images[index]                                                                
                                        planche.blit(image, (x*32, y*32))   
                                    else:
                                        self.MOTEUR.OBJETS.traitement_objet(index, x, y, c)

                            x += 1                             
                        y+=1
            c+=1
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
                                    indexOrigine, image = VAR.images[index]                                    
                                    bloquage.blit(image, (x*32, y*32))   
                            x += 1                             
                        y+=1
        
        return bloquage