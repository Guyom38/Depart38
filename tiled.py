import pygame
import xml.etree.ElementTree as XML

import fonctions as FCT
import variables as VAR
from objets import *
import os

class map_tiled:
    def __init__(self, moteur, fichier):
        self.MOTEUR = moteur
        
        tree = XML.parse(fichier)
        self.root = tree.getroot()
        
        self.fichiers_image = []
        self.objets = {}
        
        self.planche = pygame.Surface((VAR.resolution_x, VAR.resolution_y))
        self.bloquage = pygame.Surface((VAR.resolution_x, VAR.resolution_y)).convert_alpha()
        
        # --- Charge les fichiers contenant les images du jeu
        self.etape1_chargement_des_fichiers_images()    
        # --- Cree le terrain pour connaitre les sprites a recuperer
        self.etape2_chargement_des_images_necessaires_a_la_map()   
        
        
        
        
    def etape1_chargement_des_fichiers_images(self):
        # --- crée une liste de fichier avec l'index de debut et de fin
        tilesets = self.root.findall('tileset')
        for tileset in tilesets:         
            
            source = tileset.attrib.get('source')         
            xml_fichier_tsx = XML.parse(".ressources/" + source)
            root_fichier_tsx = xml_fichier_tsx.getroot()
            
            firstgid = int(tileset.attrib.get('firstgid'))
            nombre_colonnes = int(root_fichier_tsx.attrib['columns'])
            nombre_tiles = int(root_fichier_tsx.attrib['tilecount'])
            fichier = root_fichier_tsx.find('image').get('source')                                    
            
            fichier_image = ".ressources/32/" + fichier
            image = pygame.image.load(fichier_image).convert_alpha()
            image_mask = None
            
            fichier_mask = fichier_image.replace(".png", "_mask.png")
            if os.path.exists(fichier_mask):
                image_mask = pygame.image.load(fichier_mask).convert_alpha()
                
            self.fichiers_image.append((firstgid, nombre_tiles, nombre_colonnes, image, image_mask))
               
               
               
               
    # --- Parcours les differentes couches et crée une entrée vide dans le dictionnaire contenant la clé de l'image         
    def etape2_chargement_des_images_necessaires_a_la_map(self):
        
        # --- Parcours chaque calques de la map
        for layer in self.root.findall('layer'):
            
            data = layer.find('data')
            if data is not None:               
                csv_text = data.text.strip()
                lignes = csv_text.replace("'","").split('\n')
                
                # --- Parcours chaque ligne du decors
                for ligne in lignes:

                    # --- Parcours chaque colonne de la ligne du decors
                    for index in ligne.split(','):   
                        
                        if not index == "":
                            index = int(index)           
                            if not index in VAR.images:
                                VAR.images[index] = self.recupere_liste_images_de_l_objet(index)
                              
    
    
    
    
            
            
    def recupere_liste_images_de_l_objet(self, index):
        liste_images = []
        for debut, nombre, colonnes, image_plaquette, image_mask in self.fichiers_image:
            etat = C_AUCUN
            
            if debut <= index < debut+nombre:
                largX = 1
                   
                indexN = index - debut
                y = (indexN // colonnes)
                x = (indexN % colonnes)   
                dimXSrc, dimYSrc = VAR.dimOrigine, VAR.dimOrigine
                dimXDst, dimYDst = VAR.dim, VAR.dim                    
                    
                objet_anime = False
                # --- Traitement si objet particulier
                if index in DICO_OBJETS_PARTICULIERS:                    
                    parametres = DICO_OBJETS_PARTICULIERS[index]
                    index_offset_plaquette, index_sur_plaquette = parametres[0]
                    largX, hautY = parametres[1]                    
                    etat = parametres[2]                    
                    est_ce_une_animation = parametres[3]                    
                  
                        
                    if largX > 1 or hautY > 1:
                        y -= (hautY - 1)                        
                        dimXSrc = (largX * VAR.dimOrigine) # 32
                        dimYSrc = (hautY * VAR.dimOrigine) 
                        
                        dimXDst = (largX * VAR.dim)
                        dimYDst = (hautY * VAR.dim)                             

                        # --- ajout en images ignorées les images qui composent l'objet
                        for y_ign in range(0, hautY):
                            for x_ign in range(0, largX):
                                if not (x_ign == x and y_ign == y):
                                    LISTE_IMAGES_IGNOREES.append( (y_ign * colonnes) + x_ign)
                                
                    fichier_animation = '.ressources/32/animations/' + str(index_sur_plaquette) + '.png'
                    existe_t_il_un_fichier_animation = os.path.exists(fichier_animation)
                    objet_anime = (est_ce_une_animation and existe_t_il_un_fichier_animation)
                    
                # --- traitement si objet animé, depuis un fichier
                if objet_anime:
                    image_animation = pygame.image.load(fichier_animation).convert_alpha()
                    nombre_images = (image_animation.get_width() // dimXSrc)
                    for i in range(0, nombre_images) :
                        image = image_animation.subsurface( (i * VAR.dimOrigine, 0, dimXSrc, dimYSrc))
                        imageDim = pygame.transform.smoothscale(image, (dimXDst, dimYDst))
                        liste_images.append(imageDim)
                        
                # --- traitement, si objet banal
                else:
                    image = image_plaquette.subsurface( (x * VAR.dimOrigine, y * VAR.dimOrigine, dimXSrc, dimYSrc))
                    imageDim = pygame.transform.smoothscale(image, (dimXDst, dimYDst))
                    liste_images.append(imageDim)
                
                # --- creation du mask si c'est un objet
                imageDim_mask = None
                if not image_mask == None:
                    image_mask = image_mask.subsurface( (x * VAR.dimOrigine, y * VAR.dimOrigine, dimXSrc, dimYSrc))
                    imageDim_mask = pygame.transform.smoothscale(image_mask, (dimXDst, dimYDst))
                    
                return (liste_images, imageDim_mask, etat)
        
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
                    lignes = csv_text.split('\n')
                    y = 0
                    for ligne in lignes:
                        x = 0
                        tile_ids = ligne.replace("'","").split(',')   

                        for index in tile_ids:  
                            
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
                    lignes = csv_text.split('\n')
                    y = 0
                    for ligne in lignes:
                        x = 0
                        tile_ids = ligne.replace("'","").split(',')   
                        
                        for index in tile_ids:                              
                            
                            if not index == "":
                                index = int(index)   
                                if index > 0:  
                                    
                                    # --- dessine couche basse (sol et mur)
                                    if layer.attrib['name'] in ("Sol", "Mur"): 
                                        image, image_mask, traversable = VAR.images[index]                                                                                                        
                                        self.planche.blit(image[0], (x * VAR.dim, y * VAR.dim))  
                                    
                                    # --- dessine autre couche
                                    else:
                                        
                                        # --- ajoute a la liste des objets a afficher avec une priorité
                                        considere_obstacle = (layer.attrib['name'] in ("Decors", "Derriere_Meuble", "Devant_Meuble"))
                                        objet = self.MOTEUR.ELEMENTS_VISUELS.traitement_objet(index, x, y, c, considere_obstacle)
                                        
                                        # --- integration a la zone bloquée
                                        if (not objet == None) and (objet.etat == C_OBSTACLE):
                                            objet.afficher(self.bloquage)
                                            
                                            
                            x += 1                             
                        y+=1
            c+=1
        return self.planche
    
    # --- l'objectif est de creer une bitmap contenant tous les obstacles.
    # --- on colle a l'image les images mask si elle existe.
    # --- en cas d'absence on colle images d'origine
    def generer_png_blocage(self):   
        for layer in self.root.findall('layer'):
            if layer.attrib['name'] == "Bloqué":
                data = layer.find('data')
                if data is not None:               
                    csv_text = data.text.strip()
                    lignes = csv_text.split('\n')
                    y = 0
                    for ligne in lignes:
                        x = 0
                        tile_ids = ligne.replace("'","").split(',')   
                        
                        for index in tile_ids:                              
                   
                            if not index == "":
                                index = int(index)   
                                if index > 0:
                                    image, image_mask, traversable = VAR.images[index] 
                                    image_a_utilisee = image if image_mask == None else image_mask                                   
                                    self.bloquage.blit(image_a_utilisee, (x * VAR.dim, y * VAR.dim))   
                                    
                                    #VAR.fenetre.blit(self.bloquage, (0,0))
                                    #pygame.display.update()
                                    #time.sleep(0.01)
                            x += 1                             
                        y+=1
        
        return self.bloquage