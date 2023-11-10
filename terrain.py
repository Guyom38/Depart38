from fonctions import *
import variables as VAR
import pygame

class CTerrain:
    def importe_calque(self, donnees):
        bob = ""
        x,y = 0, 0
        for d in donnees:            
            if d>0:
                self.MAP[x][y] = 1

            x += 1
            if x > 59: 
                y+=1
                x=0

                
        
                
    def __init__(self, fichier):
        self.MAP =  GenereMat2D(60,30, 0)

        #file = open(fichier, "r")
        #lines = file.readlines()
        #file.close()

        #x, y = 0,0
        #for ligne in lines:
        #    for m in ligne.strip():
        #        if m == "#": 
        #            self.MAP[x][y] = 1
        #        x+=1
        #    x=0
        #    y+=1
            
        self.importe_calque( [  12,18,18,18,18,18,18,18,18,18,18,139,18,18,18,18,18,18,18,139,18,18,18,18,18,18,18,18,18,18,18,139,18,18,18,18,18,18,18,18,18,18,139,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,10,
                                28,34,34,34,34,34,34,34,34,34,34,93,34,34,34,34,34,34,34,93,34,34,34,34,34,34,34,34,34,34,34,93,34,34,34,34,34,34,34,34,34,34,93,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,26,
                                28,0,0,0,0,0,0,0,0,0,0,93,0,0,0,0,0,0,0,112,0,0,0,0,0,0,0,0,0,0,0,112,0,0,0,0,0,0,0,0,0,0,112,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,0,0,0,48,18,18,18,18,18,18,139,18,18,18,18,18,18,18,18,18,26,
                                28,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,93,16,0,0,0,0,0,0,0,0,0,64,34,34,34,34,34,34,93,34,34,34,34,34,34,34,34,34,26,
                                28,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,93,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,112,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,112,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,140,18,18,18,18,18,18,18,18,18,18,18,138,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,112,34,34,34,34,34,34,34,34,34,34,34,112,0,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,93,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,48,18,139,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,93,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,64,34,112,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,112,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,18,18,18,18,18,18,18,18,18,18,138,0,0,0,0,0,0,0,0,0,0,93,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,34,34,34,34,34,34,34,34,34,34,112,0,0,0,0,0,0,0,48,18,18,18,18,139,18,18,18,18,18,18,18,18,18,18,18,18,18,139,18,18,18,18,18,16,0,0,0,0,77,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,64,34,34,34,34,93,34,34,34,34,34,34,34,34,34,34,34,34,34,93,34,34,34,34,34,32,0,0,0,0,93,18,18,18,18,18,18,18,18,18,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,112,0,0,0,0,0,0,0,0,0,0,0,0,0,112,0,0,0,0,0,0,0,0,0,0,93,34,34,34,34,34,34,34,34,34,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,112,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,48,18,18,18,18,18,18,18,138,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,64,34,34,34,34,34,34,34,112,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,93,0,0,0,0,0,0,0,0,0,0,0,0,0,93,0,0,0,0,0,0,0,0,0,0,77,0,0,0,0,0,0,0,0,0,26,
                                28,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,93,0,0,0,0,0,0,0,0,0,0,0,0,0,93,0,0,0,0,0,0,0,0,0,0,93,0,0,0,0,0,0,0,0,0,26,
                                9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,9346,
                                9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362,9362
                            ] )
        self.importe_calque([   0,0,0,0,0,17269,17270,17269,17270,0,311,0,0,392,393,0,17269,17270,311,0,0,394,395,0,17269,17270,17269,17270,17269,17270,311,0,0,0,0,17269,17270,17269,17270,17269,17270,311,0,0,17269,17270,17269,17270,0,0,0,8805,8806,8807,0,0,0,0,0,0,
                                0,515,516,517,0,17285,17286,17285,17286,0,327,0,0,408,409,0,17285,17286,327,0,0,410,411,0,17285,17286,17285,17286,17285,17286,327,0,6487,0,0,17285,17286,17285,17286,17285,17286,327,0,0,17285,17286,17285,17286,0,0,0,8821,8822,8823,0,0,0,0,0,0,
                                0,531,532,533,0,0,0,0,0,0,343,0,0,424,425,0,0,0,343,0,0,0,0,0,0,0,0,0,0,0,343,0,6503,0,0,0,0,0,0,0,0,343,0,0,0,0,0,0,0,0,0,8837,8838,8839,0,0,0,0,0,0,
                                0,547,548,549,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6519,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,648,649,650,0,648,649,650,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,664,665,666,0,664,665,666,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,360,0,440,441,0,440,441,0,0,
                                0,0,11399,11400,11401,11402,10948,10949,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6462,0,6487,376,0,456,457,0,456,457,0,0,
                                0,0,11415,11416,11417,11418,10964,10965,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6462,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6478,0,6503,0,0,472,473,0,472,473,0,0,
                                0,0,11431,11432,11433,11434,10980,10981,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6478,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6519,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,445,0,311,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,461,0,327,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,477,0,343,0,0,0,0,0,0,0,0,0,311,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,311,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,327,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,327,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,343,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,343,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,323,323,0,0,0,0,0,0,6462,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,394,395,0,311,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,339,339,0,0,0,0,0,0,6478,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6487,0,0,0,0,0,0,0,0,410,411,0,327,0,6462,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6503,0,0,0,0,0,0,0,0,0,0,0,343,0,6478,0,0,0,0,0,0,0,0,0,0,515,516,517,0,18212,18212,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6519,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,531,532,533,0,18228,18228,0,0,0,0,
                                0,0,0,0,0,0,0,392,393,392,393,0,0,311,0,0,0,0,0,0,0,0,0,0,0,0,0,0,651,652,653,0,0,651,652,653,0,0,0,0,0,0,0,0,0,0,0,0,0,0,547,548,549,0,0,0,0,0,0,0,
                                0,740,0,0,0,0,0,408,409,408,409,0,359,327,0,0,0,0,0,0,0,0,0,0,0,0,0,0,667,668,669,0,0,667,668,669,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,756,0,0,0,0,0,424,425,424,425,0,375,343,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,772,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,651,652,653,0,0,651,652,653,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,667,668,669,0,0,667,668,669,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17269,17270,17269,17270,17269,17270,0,0,0,0,0,0,0,0,17269,17270,17269,17270,17269,17270,0,0,0,0,0,17269,17270,17269,17270,17269,17270,0,0,0,0,17269,17270,17269,17270,17269,17270,0,0,
                                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17285,17286,17285,17286,17285,17286,0,0,0,0,0,0,0,0,17285,17286,17285,17286,17285,17286,0,0,0,0,0,17285,17286,17285,17286,17285,17286,0,0,0,0,17285,17286,17285,17286,17285,17286,0,0 
                            ] )


   
            
    def preparer_terrain(self):
      
            
        self.planche = pygame.image.load(".ressources/maps.png")
        self.blocage = pygame.image.load(".ressources/mapb.png").convert_alpha()
        self.arrayBlocage = pygame.surfarray.array_blue(self.blocage)

        return
        #self.planche = pygame.Surface((1920, 1080),pygame.SRCALPHA,32)
      
        pygame.draw.rect(self.planche, (64,64,64), (0, 0, VAR.dim*60, VAR.dim*30), 2)
        
        for yC in range(30):
            for xC in range(60):
                if self.MAP[xC][yC] == 1: pygame.draw.rect(self.planche, (255,0,0), (xC*VAR.dim, yC*VAR.dim, VAR.dim, VAR.dim), 0)
                
        