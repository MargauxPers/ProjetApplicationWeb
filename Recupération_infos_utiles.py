import wptools

def get_info(country):
    page = wptools.page(country)    #On va chercher la page Wikipédia en question
    page.get_parse(False)
    return page.data['infobox'] 


def get_name(info):
    donnees=info['conventional_long_name']
    nom=donnees.split('{')[0]   #Pour isoler le nom le plus courant en cas de plusieurs noms existants
    return nom

def get_capital(info):
    # cas général
    if 'capital' in info:
        # parfois l'information récupérée comporte plusieurs lignes
        # on remplace les retours à la ligne par un espace
        capital = info['capital'].replace('\n',' ')
        
        # le nom de la capitale peut comporter des lettres, des espaces,
        # ou l'un des caractères ',.()|- compris entre crochets [[...]]
        m = re.match(".*?\[\[([\w\s',(.)|-]+)\]\]", capital)
        
        # on récupère le contenu des [[...]]
        capital = m.group(1)
        return capital      
    # Aveu d'échec, on ne doit jamais se retrouver ici
    print(' Could not fetch country capital {}'.format(info))
    return None

def get_currency(info):
    currency=''
    liste=['currency']
    for elt in liste:
        if elt in info:
            info_currency=info[elt] #chaîne de caractères des données
            liste_currency=info_currency.split('[[')    #extraction de la donnée
            currency=liste_currency[1].split(']]')[0]
            return currency
        if currency=='':
            return 'Data not available'
    
    
    
 def get_population(info):
    population=''
    liste=['population_census','population_estimate']  #différentes possibilités de noms pour le dictionnaire
    for n in range (len(liste)):
        if liste[n] in info:
            if len(info[liste[n]])>12: #il n'y a pas que la population écrite
                return 'Data not available' #Données compliquées à extraire
            else:
                return info[liste[n]]
        if population=='':
            return 'Data not available'%on met la population
        
        
def get_coords(info):    
    liste=['coordinates','largest_city','capital']  #Différents noms possibles pour obtenir des coordonnées
    for elt in liste:
        if elt in info:
                L=info[elt]   #chaîne de caractères des données
                L=L.split('|') #début de l'extraction des données
                i=0
                while L[i] not in ['Coord','{{Coord','{{coord','coord','Coord ','{{Coord ','{{coord ','coord ']: #différentes possibilités de débuts pour les coordonnées
                    i+=1
                
                longueur = None
                
                for symb in ['W','W}}','W}} {{coord','E','E}}']:    ##différentes chaînes de caractères marquant la fin de la chaîne des données utiles
                    if symb in L:
                        longueur=L.index(symb)+1    #position des données dans la chaîne (grossièrement)
                
                    
                if longueur==i+7:   #précision à la minute
                    lat_et_long={}
                    coord=[float(L[i+1]),float(L[i+2]),L[i+3],float(L[i+4]),float(L[i+5]),L[i+6]]
                    coord[1]=coord[1]/60   #conversion des minutes
                    coord[4]=coord[4]/60
                    lat= coord[0]+coord[1]
                    long= coord[3]+coord[4]
                    if coord[2]=='S':   #Conversion depuis le système sexiagésimal
                        lat=-lat
                    if coord[5] in ['W','W}} {{coord']: #Conversion depuis le système sexiagésimal
                        long=-long
                    lat_et_long['latitude']=lat   #Création d'un dictionnaire
                    lat_et_long['longitude']=long
                    return lat_et_long
                
                elif longueur==i+9:     #précision à la seconde
                    lat_et_long={}
                    coord=[float(L[i+1]),float(L[i+2]),L[i+4],float(L[i+5]),float(L[i+6]),L[i+8]]
                    coord[1]=coord[1]/60   #conversion des minutes
                    coord[4]=coord[4]/60
                    lat= coord[0]+coord[1]
                    long= coord[3]+coord[4]
                    if coord[2]=='S':   #Conversion depuis le système sexiagésimal
                        lat=-lat
                    if coord[5]=='O':   #Conversion depuis le système sexiagésimal
                        long=-long
                    lat_et_long['latitude']=lat
                    lat_et_long['longitude']=long
                    return lat_et_long
                else:
                    return {'latitude': -17.7450363, 'longitude': 168.315741}
                
                

def get_superficie(info):
    sup = ''
    area = ['area_km2'] #On crée une liste contenant les différentes possibilités de débuts pour la superficie
    La = len(area)
    for in in range(La):
        if area[i] in info :
            return info[area[i]]
        if sup == '':        #Si la superficie n'est pas disponible
        return "La superficie n'est pas disponible."
    
  
def get_leader(info) :
    leader = ''
    l_leader = ['leader','leader_name1']
    for elt in liste_leader : 
        if elt in info : 
            inf_l = info[elt]
            list_leader = inf_l.split('[[')
            leader = list_leader[1].split(']]')[0]  #On extrait les données
            return leader
        if leader == '':
        return "Le nom du leader n'est pas disponible."
    

def get_langues (info): #ne fonctionne pas encore
    langues = ''

    if 'official_languages' in info :
        langues = info['official_languages']
        # parfois l'information récupérée comporte plusieurs lignes
        # on remplace les retours à la ligne par un espace
        langues = info['official_languages'].replace('\n',' ')
        langues = langues.split(':')[1]
        langues = langues.split('hlist')[1]

        langues.strip('|{}')  

        # le nom de la capitale peut comporter des lettres, des espaces,
        # ou l'un des caractères ',.()|- compris entre crochets [[...]]
        print(langues)
        m = re.match(".*?{}\[\[([\w\s',(.)|-]+)\]\]", langues)
        print(m)
        # on récupère le contenu des [[...]]
        # langues = m.group(1)

        return langues     
                
        
 def get_HDI(info):
    HDI=''
    liste=['HDI']
    for elt in liste:
        if elt in info:
            HDI=info[elt]   #chaîne de caractères des données
            return HDI
        if HDI=='':
        return 'Data not available'
                
            ############ # faire densité, langues
            
##Base de données
    
Afrique=['Algeria','Angola','Benin','Botswana','Burkina_Faso','Burundi','Cameroon',\
         'Cape_Verde','Central_African_Republic','Chad','Comoros','Democratic_Republic_of_the_Congo',\
         'Djibouti','Egypt','Equatorail_Guinea','Eritrea','Eswatini',\
         'Ethiopia','Gabon','Ghana','Guinea','Guinea_Bissau','Ivory_Coast',\
         'Kenya','Lesotho','Liberia','Libya','Madagascar','Malawi','Mali','Mauritania','Mauritus','Morocco',\
         'Mozambique','Namibia','Niger','Nigeria','Republic_of_the_Congo','Rwanda','Sao_Tomé_and_Principe',\
         'Senegal','Seychelles','Sierra_Leone','Somalia','South_Africa','South_Sudan','Sudan','Tanzania',\
         'Tazania','The_Gambia','Togo','Tunisia','Uganda','Zambia','Zimbabwe']

for pays in PAYS:
    
    # ouverture d'une connexion avec la base de données
    conn = sqlite3.connect('pays_final3.sqlite')
    
    # préparation de la commande SQL
    c = conn.cursor()
    sql = 'INSERT INTO countries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    
    # les infos à enregistrer
    info=get_info(pays)
    name = get_name(info)
    capital = get_capital(info)
    lat_et_long = get_coords(info)
    area=get_superficie(info)
    population=get_population(info)
    currency=get_currency(info)
    HDI=get_HDI(info)
    callingcode=get_callingcode(info)
    GINI=get_Gini(info)
    GDP=get_GDP(info)
    titre_leader=get_titre_leader(info)
    leader=get_leader(info)
    image=pays+'.png'  #pour afficher les images côté client
    
    
    # soumission de la commande (noter que le second argument est un tuple)
    c.execute(sql,(pays, name, capital, titre_leader, leader, population, area, GDP, HDI, GINI, currency, callingcode, lat_et_long['latitude'],lat_et_long['longitude'],image))
    conn.commit()
