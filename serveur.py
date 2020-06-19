#-*- coding: utf-8 -*-
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

  #
  # On surcharge la méthode qui traite les requêtes GET
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

  #
  # On surcharge la méthode qui traite les requêtes HEAD
  #
  def do_HEAD(self):
      self.send_static()

  def send_static(self):
    # on modifie le chemin d'accès en insérant un répertoire préfixe
    self.path = self.static_dir + self.path

    # on appelle la méthode parent (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    if (self.command=='HEAD'):
        http.server.SimpleHTTPRequestHandler.do_HEAD(self)
    else:
        http.server.SimpleHTTPRequestHandler.do_GET(self)


  #
  #On envoie des données en format html
  #
  def send_html(self,content):
     headers = [('Content-Type','text/html;charset=utf-8')]
     html = '<!DOCTYPE html><title>{}</title><meta charset="utf-8">{}'.format(self.path_info[0],content)
     self.send(html,headers)

  #
  #On envoie des données qui sont en format json
  #
  def send_json(self,data,headers=[]):
    #On convertit nos données de format utf-8 en bits
    #json.dumps permet de transformer data en str pour le convertir en bits
    body = bytes(json.dumps(data),'utf-8')
    #On envoie la ligne de statut
    self.send_response(200)
    #On envoie les lignes d'entètes
    self.send_header('Content-Type','application/json')
    self.send_header('Content-Length',int(len(body)))
    [self.send_header(*t) for t in headers]
    self.end_headers()
    #On envoie le corps de la réponse
    self.wfile.write(body)


  #
  # on analyse la requête pour initialiser nos paramètres
  #
  def init_params(self):
    #On analyse l'adresse
    info = urlparse(self.path)
    #On récupère l'url sans /
    self.path_info = [unquote(v) for v in info.path.split('/')[1:]]
    #On récupère la requète de l'url
    self.query_string = info.query
    #On analyse la requète
    self.params = parse_qs(info.query)

    #Récupération du corps
    length = self.headers.get('Content-Length')
    ctype = self.headers.get('Content-Type')
    if length:
      self.body = str(self.rfile.read(int(length)),'utf-8')
      if ctype == 'application/x-www-form-urlencoded' :
        self.params = parse_qs(self.body)
    else:
      self.body = ''

    #Traces
    print('info_path =',self.path_info)
    print('body =',length,ctype,self.body)
    print('params =', self.params)


  #
  # Enfin, on renvoie les informations d'un pays au format json
  #
  def send_json_country(self, country) :

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

  #
  #Récupération des données des pays
  #
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
      name = i['nom']
      data.append({'wp': wp, 'lat': lat, 'lon': lon, 'name': name})
    return data


  #
  #On récupère des données d'un pays
  #
  def db_get_country(self,country):
    c = conn.cursor()
    sql = 'SELECT * from countries WHERE wp=?'
    c.execute(sql,(country,))
    return c.fetchone()


#
# Puis on ouvre d'une connexion avec la base de données
#
conn = sqlite3.connect('pays.sqlite')

# Pour accéder au résultat des requêtes sous forme d'un dictionnaire
conn.row_factory = sqlite3.Row

#
# Enfin, on procède à l'nstanciation et lancement du serveur
#
httpd = socketserver.TCPServer(("", 8081), RequestHandler)
httpd.serve_forever()
