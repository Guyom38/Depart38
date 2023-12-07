
import pygame
import variables as VAR
from fonctions import *
import time

from classes.joueurs.ia.ia import *
from classes.joueurs.action import *
            
class CJoueur:
    def __init__(self, moteur, index, x, y, nom, is_IA, fonction = -1):
        self.MOTEUR = moteur
        self.MECANIQUE_ACTION = CAction(self)
        
        self.MECANIQUE_OBJET = CAction(self) 
        self.pression_bouton_activer_objet = False
             
        self.index = index
        self.nom = nom
        self.equipe = 0
        
        self.x, self.y = x, y + 0.5
        self.direction = ENUM_DIR.AUCUN
        
        #
        self.direction_image = ENUM_DIR.AUCUN
        
        self.en_mouvement = True
        
        self.animation = ENUM_ANIMATION.MARCHER
        
        self.fonction = fonction        
        self.offsetX, self.offsetY = -VAR.dimDiv2, -VAR.dimOffY     
        
        self.champ_vision = 60
        
        if is_IA:
            
            self.IA = CIA(moteur, self)            

            if fonction == 0:
                self.vitesse = 7
                self.distance_vision = 200
                self.image = pygame.image.load(".ressources/32/agent.png").convert_alpha()
                self.couleur_vision = (193,249,153, VAR.ray_alpha)
            elif fonction == 2:
                self.vitesse = 4
                self.distance_vision = 120
                self.image = pygame.image.load(".ressources/32/basile.png").convert_alpha()
                self.couleur_vision = (255,255,255, VAR.ray_alpha)
            else:
                self.vitesse = 4
                self.distance_vision = 120
                self.image = pygame.image.load(".ressources/32/chef.png").convert_alpha()
                self.couleur_vision = (239,231,129, VAR.ray_alpha)
            
            
   
        else:
            self.image = pygame.image.load(".ressources/32/agent2.png").convert_alpha()
            self.IA = None
            self.vitesse = 20

        dimension_image = (56 * VAR.dim, 40 * VAR.dim)
        
        self.image = pygame.transform.smoothscale(self.image, dimension_image)
        self.generer_image_nom()
        self.ombre_joueur = self.generer_ombre_joueur()
        
        self.directionPrecedente = ENUM_DIR.AUCUN
        self.seTourne = 0  
        
        self.tempo,self.tempoTimer = 0, time.time()        
        self.timer_particules = time.time()        
        
        # --- Gestion du mask pour les collisions
        self.image_mask = pygame.Surface((VAR.dimMask, 4)) # 32 pixel => 20
        self.mask = pygame.mask.from_surface(self.image_mask)
        self.mask_rect = self.image_mask.get_rect(center = (0,0))

    def changement_equipe(self, equipe):
        self.equipe = equipe
        self.generer_ombre_joueur()
        
    def generer_ombre_joueur(self):
        diametre = VAR.dim * 2
        rayon = diametre // 2
        
        self.ombre = pygame.Surface((diametre, diametre), pygame.SRCALPHA).convert_alpha()
        pygame.draw.circle(self.ombre, VAR.couleurs_equipes[self.equipe], (rayon, rayon), rayon)
        
        
    def generer_image_nom(self):
        ecriture = pygame.font.SysFont('arial', 20) 
        
        #image_ombre = ecriture.render( self.nom , True, (0,0,0)) 
        image_texte = ecriture.render( self.nom , True, (255,255,255)) 
        
        image_nom = pygame.Surface( (image_texte.get_width()+4, image_texte.get_height()-4) ).convert_alpha()
        image_nom.fill( (0, 0, 0, 255) )
        
        #image_nom.blit(image_ombre, (0, -4))
        image_nom.blit(image_texte, (2, -2))
        
        self.image_nom = image_nom  
          
    def get_position(self):
        return (int((self.x * VAR.dim) + VAR.dimDiv2), int((self.y * VAR.dim)))    
               
    def position_int_x(self):
        return round((self.x * VAR.dim))
    def position_int_y(self):
        return round((self.y * VAR.dim))
        
    def toujours_sur_le_terrain(self):
        return (    self.position_int_x() > -1 and self.position_int_x() < self.MOTEUR.TERRAIN.arrayBlocage.shape[0] \
                    and self.position_int_y() > -1 and self.position_int_y() < self.MOTEUR.TERRAIN.arrayBlocage.shape[1]    )            
    
    
    
    def collision_avec_decors(self): 
        self.mask_rect.center = self.position_int_x()+VAR.dimDiv2, self.position_int_y() 
       
        offset_x = 0 - self.mask_rect.left 
        offset_y = 0 - self.mask_rect.top 
     
        collision = self.mask.overlap(self.MOTEUR.TERRAIN.maskBlocage, (offset_x, offset_y))
        if collision:
            if ENUM_DEMO.BLOCAGE in VAR.demo :
                pygame.draw.rect(VAR.fenetre, (255,0,0), self.mask_rect, 0)  
            return True
        return False
        
     
    
    
                                         
    def afficher_fumee(self):
        # --- particules
        if time.time() - self.timer_particules > (2 / self.vitesse) and self.vitesse > 5:            
            self.MOTEUR.PARTICULES.Ajouter_Particule(self.position_int_x() + VAR.dimDiv2, self.position_int_y(), (255,255,255))
            self.timer_particules = time.time()
    
    def reflechit(self):
        self.IA.IA_PATHFINDING.traque_calculer_le_chemin_jusqua((int(self.MOTEUR.PERSONNAGES.JOUEURS[0].x), int(self.MOTEUR.PERSONNAGES.JOUEURS[0].y)))    
        if self.direction == ENUM_DIR.AUCUN:
            self.IA.etablir_direction_initiale()                
        self.IA.je_reflechis()        
                     
    
                     
    def se_deplace(self):        
        if not self.en_mouvement :
            return
        
        valeurs = None
        if self.direction == ENUM_DIR.GAUCHE: valeurs = (-VAR.pas, 0, ENUM_DIR.GAUCHE)
        elif self.direction == ENUM_DIR.DROITE: valeurs = (VAR.pas, 0, ENUM_DIR.DROITE)
        elif self.direction == ENUM_DIR.HAUT: valeurs = (0, -VAR.pas, ENUM_DIR.HAUT)
        elif self.direction == ENUM_DIR.BAS: valeurs = (0, VAR.pas, ENUM_DIR.BAS)
        elif self.direction == ENUM_DIR.DIAGONAL1: valeurs = (-VAR.pas, VAR.pas, ENUM_DIR.GAUCHE)
        elif self.direction == ENUM_DIR.DIAGONAL3: valeurs = (VAR.pas, VAR.pas, ENUM_DIR.DROITE)
        elif self.direction == ENUM_DIR.DIAGONAL7: valeurs = (-VAR.pas, -VAR.pas, ENUM_DIR.GAUCHE)
        elif self.direction == ENUM_DIR.DIAGONAL9: valeurs = (VAR.pas, -VAR.pas, ENUM_DIR.DROITE)
         
        
        xo, yo = self.x, self.y        
        for i in range(0, self.vitesse):
            if not valeurs == None:
                xx, yy, direction = valeurs
                self.direction_image = direction
                self.x += xx
                self.y += yy
            
            est_ordinateur = (not self.IA == None)    
            if not est_ordinateur:
                if self.toujours_sur_le_terrain():   
                    if self.collision_avec_decors():
                        if self.reajustement_apres_collision(xo, yo):                            
                            self.x, self.y = xo, yo
                            break
                        
                        else:                            
                            xo, yo = self.x, self.y    

            else:
                self.reflechit()  

                
                
    def reajustement_apres_collision(self, xo, yo):
        if self.direction == ENUM_DIR.DIAGONAL1: liste_directions_primaires_a_tester = [(-VAR.pas, 0), (0,VAR.pas)]
        elif self.direction == ENUM_DIR.DIAGONAL3: liste_directions_primaires_a_tester = [(VAR.pas, 0), (0,VAR.pas)]
        elif self.direction == ENUM_DIR.DIAGONAL7: liste_directions_primaires_a_tester = [(-VAR.pas, 0), (0,-VAR.pas)]
        elif self.direction == ENUM_DIR.DIAGONAL9: liste_directions_primaires_a_tester = [(VAR.pas, 0), (0,-VAR.pas)]
        else:
            return True
                
        for xx, yy in liste_directions_primaires_a_tester:
            self.x, self.y = (xo + xx), (yo + yy)
            if not self.collision_avec_decors():
                return False  
        return True
                
        
    def rythme_animation(self):
        if time.time() - self.tempoTimer > 0.1: 
            self.tempo += 1
            self.tempoTimer = time.time()
                
    def coordonnees_image_animee(self):
        self.rythme_animation()
        
        
        position_x, position_y, nombre_images = 0, 8, 6
        if self.direction_image == ENUM_DIR.HAUT: position_x = 1
        elif self.direction_image == ENUM_DIR.BAS: position_x = 3
        elif self.direction_image == ENUM_DIR.GAUCHE: position_x = 2
        elif self.direction_image == ENUM_DIR.DROITE: position_x = 0
        else: position_y, nombre_images = 7, 12
        
        if self.en_mouvement:
            animation = self.animation
        else:
            animation = ENUM_ANIMATION.ARRETER
            
        position_y = animation[0]
        nombre_images = animation[1]          
            
        return ( ((position_x * nombre_images)+(self.tempo % nombre_images)) * VAR.dim, (position_y * (VAR.dim *2)), VAR.dim, (VAR.dim *2) )
    
    def afficher_ombre(self):
        x, y = self.get_position()
        centre_ombrex, centre_ombrey = x - (self.ombre.get_width() // 2), y - (self.ombre.get_height() // 2)
        VAR.fenetre.blit(self.ombre, (centre_ombrex, centre_ombrey))
        
    def afficher_champ_vision(self):
        self.MOTEUR.PERSONNAGES.RAYS.afficher(self)
    
    def verifie_changement_nom(self):
        if self.index in VAR.DICO_NAMES_WEBSOCKET:
            nouveau_nom = VAR.DICO_NAMES_WEBSOCKET[self.index]
            if not self.nom == nouveau_nom:
                self.nom = nouveau_nom
                self.generer_image_nom()
                
    # --- affiche joueur
    def afficher(self):  
        self.verifie_changement_nom()        
      
        x, y = self.get_position()
          
        # --- affiche sprite joueur
        xImg, yImg = x+self.offsetX, y+self.offsetY
        VAR.fenetre.blit(self.image, (xImg, yImg), self.coordonnees_image_animee())
                   
        # --- affiche nom
        VAR.fenetre.blit(self.image_nom, (xImg, yImg))
        
        # --- affiche la barre de temps (PROGRESSION)
        self.MECANIQUE_ACTION.afficher(xImg, yImg)
        
        
    