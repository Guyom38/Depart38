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
                            
                            if ENUM_DEMO.WEBSOCKET in VAR.demo:
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
        direction = data_events['data']['joystick']['direction']['angle']
        valeur = 1 if data_events['data']['joystick']['state'] == 'move' else 0
        
        VAR.DICO_NAMES_WEBSOCKET[idJoueur] = data_events['data']['joystick']['name'] 
        
        if 1 == 2: 
            if direction == "right":            pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': valeur }))
            elif direction == "left":            pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': -valeur }))
            elif direction == "down":            pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': valeur }))
            elif direction == "up":            pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': -valeur }))
            elif direction == "center":
                pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': 0 }))   
        else: 
            x, y = data_events['data']['joystick']['x'], data_events['data']['joystick']['y']
            angle = -1 if (x, y) == (0, 0) else FCT.get_angle(x, y)
            
            if (337.5 < angle <= 360) or (-1 < angle <= 22.5): pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 2,  'value': 8 }))
            elif (22.5 < angle <= 67.5)   : pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 2,  'value': 9 }))
            elif (67.5 < angle <= 112.5)  : pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 2,  'value': 6 }))
            elif (112.5 < angle <= 157.5) : pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 2,  'value': 3 }))
            elif (157.5 < angle <= 202.5) : pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 2,  'value': 2 }))
            elif (202.5 < angle <= 247.5) : pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 2,  'value': 1 }))
            elif (247.5 < angle <= 292.5) : pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 2,  'value': 4 }))
            elif (292.5 < angle <= 337.5) : pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 2,  'value': 7 }))
            else :
                pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': 0 }))
         
        
        #if data_events['data']['joystick']['x'] > 0:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': 1 }))
        #elif data_events['data']['joystick']['x'] < 0:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': -1 }))
        #else: pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': 0 }))
        
        #if data_events['data']['joystick']['y'] > 14:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': 1 }))
        #elif data_events['data']['joystick']['y'] < -14:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': -1 }))
        #else: pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': 0 }))
  
    elif 'button' in data_events['data']: 
        etat = pygame.JOYBUTTONUP if data_events['data']['state'] == 'pressed' else pygame.JOYBUTTONDOWN
        valeur = 1 if data_events['data']['state'] == 'pressed' else 0
        
        if data_events['data']['button'] == 'RIGHT':  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': valeur }))
        elif data_events['data']['button'] == 'LEFT':  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': -valeur }))
        elif data_events['data']['button'] == 'DOWN':  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': valeur }))
        elif data_events['data']['button'] == 'UP':  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': -valeur }))
        
        elif data_events['data']['button'] == 'A':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': ENUM_PAD.B_A }))
        elif data_events['data']['button'] == 'B':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': ENUM_PAD.B_B }))
        elif data_events['data']['button'] == 'X':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': ENUM_PAD.B_X }))
        elif data_events['data']['button'] == 'Y':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': ENUM_PAD.B_Y }))
        elif data_events['data']['button'] == 'START':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': ENUM_PAD.B_START }))
        elif data_events['data']['button'] == 'SELECT':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': ENUM_PAD.B_SELECT }))
        
        


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


