import pygame
import xml.etree.ElementTree as XML
from fonctions import *


class map_tiled:
    def __init__(self, fichier):
        tree = XML.parse(fichier)
        self.root = tree.getroot()
        
        self.images = {}
        
        # --- Cree le terrain pour connaitre les sprites a recuperer
        self.chargement_des_calques()   
        
        # --- Recupere les sprites utilisés sur le terrain
        self.chargement_des_images()
             
    def chargement_des_calques(self):
        for layer in self.root.findall('layer'):
            
            data = layer.find('data')
            if data is not None:               
                csv_text = data.text.strip()
                lines = csv_text.split('\n')
                
                for line in lines:
                    tile_ids = line.split(',')                    
                    if not tile_ids in self.images:
                        self.images[tile_ids] = None
                    
    def chargement_des_images(self):
        tilesets = self.root.findall('tileset')
        for tileset in tilesets:
            firstgid = tileset.attrib.get('firstgid')
            source = tileset.attrib.get('source')
       
    def initialisation_terrain(self):
        width = self.root.attrib['width']
        height = self.root.attrib['height']
        
        self.MAP =  GenereMat2D(width, height, 0)
        
        
class image_tiled:
    def __init__(self, _fichier, _id):
        self.image = pygame.image.load(_fichier).convert_alpha()
        self.id = _id
        
    def get_image(self, _id):
        y = _id % self.image.get_width() * 32
        x = y - (x * self.image.get_width()) * 32
        return self.image.subsurface( (x, y, 32, 32))