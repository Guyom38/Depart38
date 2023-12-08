from thread_moteur import *
from thread_pathfinding import *
from thread_websocket import *

from constantes import *
import variables as VAR

import asyncio
                            

async def tache3():
    print("[PATHFINDING]     + Initialisation Tache PATHFINDING")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, tache3_pathfinding)        

def tache3_pathfinding():
    print("[PATHFINDING]+ Démarrage du moteur Pathfinding")
    
    while (VAR.MOTEUR == None):   
        print("[PATHFINDING]+ En attente d'initialisation du moteur")     
        time.sleep(1)
        
    PATHFINDING = CThread_Pathfinding(VAR.MOTEUR)
    PATHFINDING.demarrer()
     
async def tache2():
    print("[MOTEUR]     + Initialisation Tache JEU :")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, tache2_jeu)        
                    
def tache2_jeu():
    print("[MOTEUR]+ Démarrage du moteur Espion")
    
    MOTEUR = CMoteur()
    
    VAR.MOTEUR = MOTEUR
    MOTEUR.demarrer()
    
    


    

async def main():
    print("[MAIN]   Initialisation des taches :")
    await asyncio.gather(
        webSocket.tache1_socket(),
        tache2(),
        tache3()
    )    
       
asyncio.run(main())


