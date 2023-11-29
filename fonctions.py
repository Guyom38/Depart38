import string
import random
import pygame
import os
import time

perfs = {}
def Performance(key, timer, couleur = (255,0,0)):
    valeur = (time.time() - timer)
    if valeur == 0:
        valeur = 0.000001
    if not key in perfs:
        perfs[key] = valeur, 0, 0, 0, couleur
    _ , maximum, somme, compteur, _ = perfs[key]
    
    if valeur > maximum:
        maximum = valeur
        
    perfs[key] = valeur, maximum, (somme + valeur), compteur+1, couleur
    
    return perfs


def GenereMat2D(dimX, dimY, valeurDefaut):
    return [[valeurDefaut for x in range(dimY)] for i in range(dimX)]

def generate_short_id(length=6):
    characters = string.ascii_uppercase + string.digits
    short_id = ''.join(random.choice(characters) for _ in range(length))
    return short_id


def contientDans(objet, objet_conteneur):
    xC, yC, dxC, dyC = objet_conteneur
    x, y, dx, dy = objet
    
    return (xC < x < xC + dxC and xC < x + dx < xC + dxC and
            yC < y < yC + dyC and yC < y + dy < yC + dyC)
    
def collision(objet1, objet2):
    x1, y1, dx1, dy1 = objet1
    x2, y2, dx2, dy2 = objet2
    
    if ((x2 >= x1 + dx1) 
            or (x2 + dx2 <= x1) 
            or (y2 >= y1 + dy1)
            or (y2 + dy2 <= y1)):

        return False
    else:
        return True
    
def existe_fichier(chemin):
    return (os.path.isfile(chemin))