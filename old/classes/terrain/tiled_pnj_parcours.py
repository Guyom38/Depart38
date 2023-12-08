import variables as VAR
import fonctions as FCT
from constantes import *


def initialisation_joueurs(moteur_tiled):
    MOTEUR_TILED = moteur_tiled
    parcours = generer_parcours_PNJ(MOTEUR_TILED)
    
    if len(parcours) == 0:
        return
      
    compteurs_parcours = {}
    for pnj in MOTEUR_TILED.MOTEUR.PERSONNAGES.PNJS:
        id_parcours = 'Chemin_' + str(pnj.fonction)
        if not id_parcours in compteurs_parcours: 
            compteurs_parcours[id_parcours] = 0
            
        x, y = parcours[id_parcours]['DEPART'][compteurs_parcours[id_parcours]]
        pnj.x, pnj.y = x ,y 
        pnj.IA.parcours = parcours[id_parcours]['GRILLE']
        compteurs_parcours[id_parcours] += 1
        
            
def generer_parcours_PNJ(moteur_tiled):
    MOTEUR_TILED = moteur_tiled
    
    ID_CHEMIN_DEPART = VAR.C_MECANIQUE + 0
    ID_CHEMIN_PARCOURS = VAR.C_MECANIQUE + 1
    
    parcours = {}
    for layer in MOTEUR_TILED.root.findall('layer'):
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

                    for index in ligne.replace("'", "").split(','):
                        if not index == '':
                            indexInt = int(index)                        
                        
                            grille_parcours[x][y] = {}
                            grille_parcours[x][y]['CHEMIN'] = (indexInt == ID_CHEMIN_PARCOURS)
                            grille_parcours[x][y]['UTILISE'] = 0

                            if indexInt == ID_CHEMIN_DEPART:
                                liste_positions_pnjs.append((x, y))
                        x += 1
                    y += 1

                index_parcours = layer.attrib['name']
                parcours[ index_parcours ] = {}
                parcours[ index_parcours ]['GRILLE'] = grille_parcours
                parcours[ index_parcours ]['DEPART'] = liste_positions_pnjs
    return parcours
