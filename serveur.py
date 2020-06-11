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
  # on récupère le pays depuis la base de données
    r = self.db_get_country(country)

    # on n'a pas trouvé le pays demandé
    if r == None:
      self.send_error(404,'Country not found')

    # on renvoie un dictionnaire au format JSON
    else :
      #k correspond à la clef primaire de notre base de donnée
      data = {k:r[k] for k in r.keys()}
      headers = [('Content-Type','application/json')]
      self.send_json(data,headers)
  
  
  
def data_loc(self) :
    #Préparation de la requête SQL
    c = conn.cursor()
    sql = 'SELECT * from countries'

    #Récupération de l'information
    c.execute(sql)
    #Sélection des données présentes dans la base de donnée
    r = c.fetchall()
    data = []
    for i in r :
      wp = i['wp']
      lat = i['latitude']
      lon = i['longitude']
      name = i['name']
      data.append({'wp': wp, 'lat': lat, 'lon': lon, 'name': name})
    return data
