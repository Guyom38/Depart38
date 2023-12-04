from moteur import *
import asyncio
import websockets
import json
import time

import variables as VAR

class webSocket():  
    async def tache1_socket():   
        
        while VAR.boucle:
            print("     + Initialisation Tache Socket :")  
            try:
                async with websockets.connect(VAR.urlWss) as websocket: # ...
                    print("         + boucle thread websocket")
                    VAR.web_socket = True
                    
                    data_to_send = {"game": "EscapeGame",
                                    "id_game": str(VAR.web_socket_id_partie),  
                                    "type_client": "game" }
                    
                    await websocket.send(json.dumps(data_to_send))
                    while VAR.boucle:
                        try:
                            message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                            donnees = json.loads(message)                            
                            
                            print(str(donnees))
                            injecte_event(donnees) 
                            
                        except asyncio.TimeoutError:
                            #print("Timeout: Aucun message reçu pendant 1 seconde. "+str(time.time()))
                            continue
                        
            except (websockets.ConnectionClosed, OSError):
                print("Erreur de connexion. Tentative de reconnexion dans 5 secondes...")
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                print("Tâche annulée. Nettoyage et fermeture.")
                return

def injecte_event(data_events):
    if 'playerId' in data_events:                                            
        #idJoueurWS = int(data_events['playerId'])                        
        #if idJoueurWS not in VAR.JOUEURS_WEBSOCKET:
        #    VAR.JOUEURS_WEBSOCKET[idJoueurWS] = len(VAR.JOUEURS_WEBSOCKET) 
        #    print("Nouveau Joueur #"+str(idJoueurWS)+" => id:" + str(VAR.JOUEURS_WEBSOCKET[idJoueurWS]))       
        #idJoueur = VAR.JOUEURS_WEBSOCKET[idJoueurWS]                        
        idJoueur = int(data_events['playerId'])    
                  
    if 'joystick' in data_events['data']:
        if data_events['data']['joystick']['x'] > 0:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': 1 }))
        elif data_events['data']['joystick']['x'] < 0:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': -1 }))
        else: pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': 0 }))
        
        if data_events['data']['joystick']['y'] > 14:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': 1 }))
        elif data_events['data']['joystick']['y'] < -14:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': -1 }))
        else: pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': 0 }))
  
    elif 'button' in data_events['data']: 
        etat = pygame.JOYBUTTONUP if data_events['data']['state'] == 'pressed' else pygame.JOYBUTTONDOWN
        valeur = 1 if data_events['data']['state'] == 'pressed' else 0
        
        if data_events['data']['button'] == 'RIGHT':  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': valeur }))
        elif data_events['data']['button'] == 'LEFT':  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': -valeur }))
        elif data_events['data']['button'] == 'DOWN':  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': valeur }))
        elif data_events['data']['button'] == 'UP':  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': -valeur }))
        
        elif data_events['data']['button'] == 'A':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 0 }))
        elif data_events['data']['button'] == 'B':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 1 }))
        elif data_events['data']['button'] == 'X':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 2 }))
        elif data_events['data']['button'] == 'Y':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 3 }))
        elif data_events['data']['button'] == 'START':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 9 }))
        elif data_events['data']['button'] == 'SELECT':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 8 }))
        
        


    return "OK"
                            

        
async def tache2():
    print("     + Initialisation Tache JEU :")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, tache2_jeu)        
                    
def tache2_jeu():
    print("+ Démarrage du moteur Espion")
    
    MOTEUR = CMoteur()
    MOTEUR.demarrer()


async def main():
    print("Initialisation des taches :")
    await asyncio.gather(
        webSocket.tache1_socket(),
        tache2()
    )    
       
asyncio.run(main())


