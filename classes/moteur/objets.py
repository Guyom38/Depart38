import variables as VAR
import classes.moteur.objet as OBJ
import pygame
import time, os

from constantes import *
import fonctions as FCT

from classes.moteur.liste_objets import *






class CObjets:        
    def __init__(self, moteur):
        self.MOTEUR = moteur
        self.BDD_OBJETS = CListe_Objets()
        
        self.liste = {}  
        self.liste_objets_tries = []
    
    def initialiser_les_objets_particulier(self):
        for objet in self.BDD_OBJETS.objets:
            index_offset_plaquette, index_sur_plaquette = objet[0]
            index = index_offset_plaquette + index_sur_plaquette
            VAR.DICO_OBJETS_PARTICULIERS[index] = objet
    
    
    
    
       
    def traitement_objet(self, index, x, y, couche, force = False):
        objet = None  
        parametres_objet = None
              
        image, image_mask, etat = VAR.images[index]    
        objet_particulier = (index in VAR.DICO_OBJETS_PARTICULIERS) 
        
        if objet_particulier or force:
            if objet_particulier:
                parametres_objet = VAR.DICO_OBJETS_PARTICULIERS[index]
              
            if force: etat = C_OBSTACLE                                     
            objet = OBJ.CObjet(self.MOTEUR, index, x, y, 0, 0, image, image_mask, etat, parametres_objet)  
                      
        if not objet == None:
            key = "{:04d}{:04d}{:01d}".format((y * VAR.dim) + image[0].get_height(), (x * VAR.dim) + image[0].get_width(), couche)
            self.liste[key] = objet 
            
        return objet
    
    
   
    
    def prepare_et_tri_les_objets_a_afficher(self):
        t = time.time()
        # --- genere une liste de joueurs et de pnjs
        liste_personnages = {}
        for personnage in self.MOTEUR.PERSONNAGES.JOUEURS + self.MOTEUR.PERSONNAGES.PNJS:
            x = personnage.position_int_x() 
            y = personnage.position_int_y()+(VAR.dim // 2)
            key = "{:04d}{:04d}{:01d}".format(y, x, 0)
            liste_personnages[key] = personnage
        
        # --- fusionne la liste des objets et des joueurs
        if not ENUM_DEMO.BLOCAGE in VAR.demo:    
            listes_fusionnees = {**self.liste, **liste_personnages}        
        else:
            listes_fusionnees = liste_personnages     
                   
        self.liste_objets_tries = sorted( listes_fusionnees.items(), key=lambda x: x[0])
        FCT.Performance('OBJETS.prepare_et_tri_les_objets_a_afficher()', t)  
     
    
    
        
        
    def controle_proximites(self):
        t = time.time()
        for key, objet in self.liste_objets_tries:   
            if isinstance(objet, OBJ.CObjet):
                if objet.objet_utilisable:
                    objet.afficher_zone_activable()
        FCT.Performance('OBJETS.controle_proximites()', t)  
              
    def afficher(self):  
        t, i = time.time(), 0        
                       
        for key, objet in self.liste_objets_tries:   
            objet.afficher()    
            
            # // --- test  
            if ENUM_DEMO.PRIORITE in VAR.demo:                
                i = self.afficher_test_priorite(i, key, objet)            
        FCT.Performance('OBJETS.afficher()', t)
        
    
    
    
    def afficher_test_priorite(self, i, key, objet):
        if 2 < objet.x < 15 and 10 < objet.y < 16:
            nombre1 = int(key[0:4])  # Convertit "0123" en entier
            nombre2 = int(key[4:8])  # Convertit "4567" en entier
            nombre3 = int(key[8])    # Convertit "0" en entier

            key1 = "y:" + str(nombre1 // VAR.dim)+" x:" + str(nombre2 // VAR.dim)+" c:" + str(nombre3)
            key2 = key
                
            txt = key1 + " (" + str(objet.index) +") " + str(key2)
            image_texte = VAR.ecriture.render( txt , True, (255,0,0))
            VAR.fenetre.blit(image_texte, (1600, (i * 18)))
            i+=1
        return i