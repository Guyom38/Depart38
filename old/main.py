from thread_moteur import *
from thread_pathfinding import *
from thread_websocket import *

from constantes import *
import variables as VAR

import asyncio
import threading                            


def thread_pathfinding():
    print("[PATHFINDING]     + Démarrage du moteur Pathfinding")
    
    VAR.THREAD_PATHFINDING = CThread_Pathfinding()
    VAR.THREAD_PATHFINDING.demarrer()
     
     
     
async def tache2():
    print("[MOTEUR]     + Initialisation Tache JEU :")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, tache2_jeu)        
                    
def tache2_jeu():
    print("[MOTEUR]+ Démarrage du moteur Espion")
    
    VAR.MOTEUR = CMoteur()
    VAR.MOTEUR.demarrer()
    
    


    

async def main():
    print("[MAIN]   Initialisation des taches :")
    await asyncio.gather(
        webSocket.tache1_socket(),
        tache2()
    )    
       
t = threading.Thread(target=thread_pathfinding, args=())
t.start()

asyncio.run(main())


