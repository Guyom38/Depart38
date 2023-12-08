import pickle
import time
from classes.joueurs.algos.algo_dijkstra import *

map_fichier = "map2024"
def zone_cible_a_calculer( ZONES, zoneA, zoneB):
    return ( not zoneA == zoneB and ZONES[zoneA][zoneB] == None )

# ------------------------------------------------------------------------------------
print ("[CHARGEMENT] fichier obstacle.pkl")
with open('.caches/' + map_fichier + "_obstacle.pkl", 'rb') as fichier:
    donnees = pickle.load(fichier)
    zones_libres = donnees['ZONES_LIBRES'] 
    grille_obstacles = donnees['GRILLE_OBSTACLES']   
print ("    + " + str(len(zones_libres)) + " zones libres")
print ("    + " + str(grille_obstacles) )

# ------------------------------------------------------------------------------------
t = time.time()
print("[INITIALISATION] - Zones")
ZONES = {}
ZONES_CPT = {}
        
for indexA, zoneA in enumerate(zones_libres):
    ZONES[zoneA] = {}
    ZONES_CPT[zoneA] = 0
            
    for indexB, zoneB in enumerate(zones_libres):
        ZONES[zoneA][zoneB] = None
print("     + Terminée (" + str(round(time.time() - t, 2)) + "s)")
# ------------------------------------------------------------------------------------

# --- Initialisation des differentes variables
PARCOURS = {}
        
print("[PATHFINDING][GENERER] Initialisation")       
t = time.time() 
duree=time.time()
      
index = 1
ignore_dij = 0
ignore_deduction = 0  
nb_deduction = 0 
maximum = len(zones_libres)**2

pas = 100 / maximum 
taux = 0   
# --- Boucle principale qui compare le premier avec le dernier
for indexA, zoneA in enumerate(zones_libres):
    print("[PATHFINDING][GENERER][ZONEA]" + str(indexA))      
    for indexB, zoneB in enumerate(zones_libres[::-1]): 
                     
        chemin = []

        # vérifie que B n'existe pas dans la dico
        if zone_cible_a_calculer(ZONES, zoneA, zoneB):
            # genere le chemin entre zoneA et zoneB     
            rt = time.time()        
            chemin, _, _ = CDijkstra.algo_dijkstra(zoneA, zoneB, grille_obstacles)          
            # si un chemin a été trouvé
            if len(chemin) > 0:
                            
                # ajoute a la liste ce nouveau chemin
                PARCOURS[index] = chemin  

         
                for depart in range(0, len(chemin)): 
                    zoneC = chemin[depart]     
                    for arrive in range(len(chemin)-1, -1, -1):  
                        zoneD = chemin[arrive]
                                    
                        if zone_cible_a_calculer(ZONES, zoneC, zoneD):                    
                            ZONES[zoneC][zoneD] = index, depart, arrive, 1
                            ZONES[zoneD][zoneC] = index, depart, arrive, -1

                            ZONES_CPT[zoneC] += 1
                            ZONES_CPT[zoneD] += 1
                            nb_deduction += 1
                            taux += pas
                            taux += pas    
                        else:
                            ignore_deduction += 1    

                index += 1
        else:   
            ignore_dij += 1
                
        if time.time() - t > 1:                     
            total_secondes = ((time.time() - duree) / (index+ignore_dij)) * maximum # Exemple: 3665 secondes
            heures = int(total_secondes // 3600)  # Convertit les secondes en heures
            minutes = int((total_secondes % 3600) // 60)  # Convertit le reste en minutes
            secondes = int(total_secondes % 60)  # Le reste sont les secondes

            texte = "{:0.3f}%".format(round(taux,3))
            texte += "  █ IndexA : {:04d} [{:04d}] / IndexB : {:04d} / {:04d}".format(indexA, ZONES_CPT[zoneA], indexB,len(zones_libres)) 
            texte += "  █ Nb Parcours : {:06d} // Chemins deduis : {:06d}".format(index, nb_deduction)
            texte += "  █ Ignore Pathfinding : {:06d}".format(ignore_dij) 
            texte += "  █ Total : {:07d} / {:07d}".format(nb_deduction,maximum)
            texte += "  █ Estimation : {:03d}h {:02d}m {:02d}s".format(heures,minutes,secondes)
            print(str(texte))
            
            t = time.time()
          
with open('.caches/' + map_fichier + '.pkl', 'wb') as fichier:
    pickle.dump({'PARCOURS': PARCOURS, 'ZONES': ZONES}, fichier, protocol=pickle.HIGHEST_PROTOCOL)






# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
  
   
   
   
   
   
   
    

    


