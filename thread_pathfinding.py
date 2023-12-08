import variables as VAR
import time

class CThread_Pathfinding:
    def __init__(self, thread_moteur):
        self.MOTEUR = thread_moteur
    
    def demarrer(self):
        
        while VAR.boucle:
            print("thread")
            time.sleep(1)