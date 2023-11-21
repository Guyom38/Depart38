import variables as VAR
import objet as OBJ
import pygame

OBJ_EXTINCTEUR = 5213

LISTE_OBJ_DOUBLE_HAUTEUR = [OBJ_EXTINCTEUR]

class CObjets:        
    def __init__(self, moteur):
        self.MOTEUR = moteur
        self.liste = {}        
        
    def traitement_objet(self, index, x, y, c):
        objet = None
        indexOrigine, image = VAR.images[index]  
        
        if indexOrigine == OBJ_EXTINCTEUR:                       
            objet = OBJ.CObjet(x, y, 0, 0, image)
        
        if not objet == None:
            key = "{:04d}{:04d}{:01d}".format(y*32, x*32, 0)
            self.liste[key] = objet
            
    def image_double(self, index_haut, index_bas):
        image = pygame.Surface((32, 64)).convert_alpha()
        image.blit(VAR.images[index_haut], (0, 0))
        image.blit(VAR.images[index_bas], (0, 32))
        return image