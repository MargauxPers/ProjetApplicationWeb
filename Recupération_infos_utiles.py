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
        

        # faire densité, long et lat capitale, superficie, langues, leader
