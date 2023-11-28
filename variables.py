from fonctions import *
from constantes import *

demo = [ENUM_DEMO.BLOCAGE, ENUM_DEMO.DIJISKRA]

resolution_x = 1920
resolution_y = 1080

dimension_x = 10
dimension_y = 10

images = {}

       
fenetre = None
boucle = True

pas = 0.01
dim = 32


ecriture = None
# ray_alpha = 0 desactive la transparence
ray_alpha = 128

fichier_map = 'map'

urlWss = "wss://ws.ladnet.net"
web_socket = False
web_socket_id_partie = generate_short_id()

precision_distance = 8
precision_champs = 8


boucle = True