import pygame
import variables as VAR
import fonctions as FCT
import os, time
import xml.etree.ElementTree as XML

from constantes import *


# --- liste qui contient le nom du fichier, le debut d'indexage, le nombres d'images ... sur les images de decors


def etape1_chargement_des_fichiers_images(moteur_tiled):
    
        MOTEUR_TILED = moteur_tiled
        
        # --- crée une liste de fichier avec l'index de debut et de fin
        tilesets = MOTEUR_TILED.root.findall('tileset')
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
                
            VAR.FICHIERS_IMAGES_DECORS.append((firstgid, nombre_tiles, nombre_colonnes, image, image_mask))
               
               
               
               
    # --- Parcours les differentes couches et crée une entrée vide dans le dictionnaire contenant la clé de l'image         
def etape2_chargement_des_images_necessaires_a_la_map(moteur_tiled):
        MOTEUR_TILED = moteur_tiled
        
        # --- Parcours chaque calques de la map
        for layer in MOTEUR_TILED.root.findall('layer'):
            
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
                            image_jamais_stockee = ( not index in VAR.images )   
                            image_pas_ignoree = ( not index in VAR.LISTE_IMAGES_IGNOREES )
                            #if not image_pas_ignoree:
                            #    print ("Image ignorée #" + str(index))
                                
                            if image_jamais_stockee and image_pas_ignoree:
                                VAR.images[index] = recupere_liste_images_de_l_objet(index)
                              
    
def recupere_liste_images_de_l_objet(index):
        fichiers_image = VAR.FICHIERS_IMAGES_DECORS
        liste_images = []
        
        for debut, nombre, colonnes, image_plaquette, image_mask in fichiers_image:
            etat = C_AUCUN
            
            if debut <= index < debut+nombre:
                largX = 1
                
                # --- determine position de l'image sur la plaquette PNG   
                indexN = index - debut
                y = (indexN // colonnes)
                x = (indexN % colonnes) 
                  
                dimXSrc, dimYSrc = VAR.dimOrigine, VAR.dimOrigine
                dimXDst, dimYDst = VAR.dim, VAR.dim                    
                    
                objet_anime = False
                # --- Traitement si objet particulier
                if index in VAR.DICO_OBJETS_PARTICULIERS:                    
                    parametres = VAR.DICO_OBJETS_PARTICULIERS[index]
                    index_offset_plaquette, index_sur_plaquette = parametres[0]
                    largX, hautY = parametres[1]                    
                    etat = parametres[2]                    
                    est_ce_une_animation = parametres[3]                    
                  
                        
                    if largX > 1 or hautY > 1:                                             
                        dimXSrc = (largX * VAR.dimOrigine) # 32
                        dimYSrc = (hautY * VAR.dimOrigine) 
                        
                        dimXDst = (largX * VAR.dim)
                        dimYDst = (hautY * VAR.dim)                             


                        # --- ajout en images ignorées les images qui composent l'objet
                        for y_ign in range(0, hautY):
                            for x_ign in range(0, largX):
                                xx = x + x_ign
                                yy = y + y_ign
                                if not (xx == x and yy == y):
                                    index_a_ignore = index_offset_plaquette + (yy * colonnes) + xx
                                    if not index_a_ignore in VAR.LISTE_IMAGES_IGNOREES:
                                        VAR.LISTE_IMAGES_IGNOREES.append( index_a_ignore )                                                           
                          
                    fichier_animation = '.ressources/32/animations/' + str(index_sur_plaquette) + '.png'
                    existe_t_il_un_fichier_animation = os.path.exists(fichier_animation)
                    objet_anime = (est_ce_une_animation and existe_t_il_un_fichier_animation)
                   
                # --- traitement si objet animé, depuis un fichier
                if objet_anime:
                    image_animation = pygame.image.load(fichier_animation).convert_alpha()
                    nombre_images = (image_animation.get_width() // dimXSrc)
                    for i in range(0, nombre_images) :
                        image = image_animation.subsurface( (i * dimXSrc, 0, dimXSrc, dimYSrc))
                        imageDim = pygame.transform.smoothscale(image, (dimXDst, dimYDst))
                        liste_images.append(imageDim)
                        
                        if 1 == 2:
                            print(str((i * dimXSrc, 0, dimXSrc, dimYSrc)))
                            VAR.fenetre.fill((16,16,16))    
                            pygame.draw.rect(VAR.fenetre, (128,128,128), (0,0,dimXDst, dimYDst), 0)
                            VAR.fenetre.blit(liste_images[i], (0,0))
                            pygame.display.update()
                            time.sleep(2)
                        
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