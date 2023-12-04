# --- importation des librairies Pygame 
import pygame
from pygame.locals import *

# --- initialisation du moteur Pygame
pygame.init()

# --- création de la fenetre
fenetre = pygame.display.set_mode((1024, 768), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Mon prog Pygame")

# --- création d'un horloge pour limiter le raffraichissement
horloge = pygame.time.Clock()

obstacle_surf = pygame.Surface((32,32))
obstacle_pos = (0 ,0)

moving_surf = pygame.Surface((32,32))
moving_rect = moving_surf.get_rect(center = (300,300))

# mask 
moving_mask = pygame.mask.from_surface(moving_surf)
obstacle_mask = pygame.mask.from_surface(obstacle_surf)

x = 0
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	fenetre.fill('white')
	obstacle_pos =( obstacle_pos[0] + 1, obstacle_pos[1] )
	# obstacle 
	fenetre.blit(obstacle_surf,obstacle_pos)
	
	# moving part
	if pygame.mouse.get_pos(): moving_rect.center = pygame.mouse.get_pos()
	fenetre.blit(moving_surf,moving_rect)

	# offset
	offset_x = obstacle_pos[0] - moving_rect.left
	offset_y = obstacle_pos[1] - moving_rect.top
	
	# collision 1 point
	if moving_mask.overlap(obstacle_mask,(offset_x,offset_y)):
		moving_surf.fill('red')
		print(moving_mask.overlap(obstacle_mask,(offset_x,offset_y)))
	else:
		moving_surf.fill('green')

	
	pygame.display.update()
	horloge.tick(60)