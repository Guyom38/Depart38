from fonctions import *
from constantes import *

demo = [ENUM_DEMO.GENERER_PATHFINDING]
phase_dans_le_jeu = ENUM_PHASE.JEU

fichier_map = ''
resolution_x = 1920
resolution_y = 1080

dimension_x = 10
dimension_y = 10

images = {}
dimOrigine = 32 # --- dimension des sprites PNG
       
fenetre = None
boucle = True

pas = 0.01
dim = 24

fps_max = 30

dimDiv2 = dim // 2
dimMul2 = dim * 2

dimOffY = (1.75 * dim)
dimMask = (0.625 * dim)

ecriture = None
ecriture10 = None
# ray_alpha = 0 desactive la transparence
ray_alpha = 128


dossier_dim = str(dim) + "/"

urlQrCode = "https://gamepad.ladnet.net/joystick.html"
urlWss = "wss://ws.ladnet.net"
web_socket = False
web_socket_id_partie = generate_short_id()
JOUEURS_WEBSOCKET = {}
DICO_NAMES_WEBSOCKET = {}

# --- joystiques
nombre_manettes = 0
dico_manettes = {}

precision_distance = 10
precision_champs = 10


boucle = True

FICHIERS_IMAGES_DECORS = []
LISTE_IMAGES_IGNOREES = []
DICO_OBJETS_PARTICULIERS = {}


cellule_image = pygame.Surface((dim, dim)) # 32 pixel => 20
cellule_mask = pygame.mask.from_surface(cellule_image)
cellule_rect = cellule_mask.get_rect(center = (0,0))

cellule_image2 = pygame.Surface((dim, dim)) # 32 pixel => 20
cellule_mask2 = pygame.mask.from_surface(cellule_image2)
cellule_rect2 = cellule_mask2.get_rect(center = (0,0))

image_zone = [[], []]

couleurs_equipes = [
    (0,0,0, 60),
    (255, 0, 0, ray_alpha),    # Rouge
    (0, 0, 255, ray_alpha),    # Bleu
    (0, 255, 0, ray_alpha),    # Vert
    (255, 255, 0, ray_alpha),  # Jaune
    (255, 165, 0, ray_alpha),  # Orange
    (128, 0, 128, ray_alpha),  # Violet
    (0, 0, 0, ray_alpha),      # Noir
    (255, 255, 255, ray_alpha) # Blanc
]

C_MECANIQUE = 0
C_ROOM_BUILDER = 0
C_ROOM_BUILDER_OFFICE = 0
C_MODERN_OFFICE = 0
C_MODERN_EXTERIORS = 0
C_INTERIOR = 0

#http://noproblo.dayjo.org/ZeldaSounds/
#http://noproblo.dayjo.org/ZeldaSounds/
