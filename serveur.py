import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import json
import sqlite3

class RequestHandler(http.server.SimpleHTTPRequestHandler):
  # sous-répertoire racine des documents statiques
  static_dir = '/client'
  # version du serveur
  server_version = 'projet/0.1'

On surcharge la méthode qui traite les requêtes GET
   #
  def do_GET(self):

     # on récupère les paramètres
    self.init_params()

    # le chemin d'accès commence par "location"
    if self.path_info[0] == "location":
      data = self.data_loc()
      self.send_json(data)

    # le chemin d'accès commence par "description"
    elif self.path_info[0] == "description":
      self.send_json_country(self.path_info[1])

    # le chemin d'accès commence par "service"
    elif self.path_info[0] == "service":
      self.send_html('<p>Path info : <code>{}</p><p>Chaîne de requête : <code>{}</code></p>'.format('/'.join(self.path_info),self.query_string));

    # ou pas...
    else:
      self.send_static()
      
      

 #On renvoie désormais les informations de chaque pays au format json

def send_json_country(self,country) :
  
  #On récupère tout d'abord le pays à partir de la base de données
  p = self.db_get_country(country)
  
  #Si on ne trouve pas le pays demandé 
  if p == None
    self.send_error(404,'Pays introuvable')
  
  #On renvoie maintenant un dictionnaire au format JSON
  else : 
