from fonctions import *
from constantes import *

demo = [ENUM_DEMO.DIJISKRA, ENUM_DEMO.CHEMIN_VINCENT]


resolution_x = 1920
resolution_y = 1080

dimension_x = 10
dimension_y = 10

images = {}
dimOrigine = 32 # --- dimension des sprites PNG
       
fenetre = None
boucle = True

pas = 0.010
dim = 24

fps_max = 25

dimDiv2 = dim // 2
dimOffY = (1.75 * dim)
dimMask = (0.625 * dim)

ecriture = None
ecriture10 = None
# ray_alpha = 0 desactive la transparence
ray_alpha = 128

fichier_map = 'map'
dossier_dim = str(dim) + "/"

urlWss = "wss://ws.ladnet.net"
web_socket = False
web_socket_id_partie = generate_short_id()

precision_distance = 10
precision_champs = 10


boucle = True