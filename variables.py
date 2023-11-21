from fonctions import *

dimension_x = 10
dimension_y = 10

images = {}

       
fenetre = None
boucle = True

pas = 0.2
dim = 32

t_ray = 0


urlWss = "wss://ws.ladnet.net"
web_socket = False
web_socket_id_partie = generate_short_id()