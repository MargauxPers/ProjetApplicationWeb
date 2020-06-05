import wptools

def get_info(country):
    page = wptools.page(country)    #On va chercher la page Wikipédia en question
    page.get_parse(False)
    return page.data['infobox'] 

def get_capital(info):
    info_capital=info['capital']                  
    capitale_epuree1 = info_capital.split('[')    
    capitale_epuree2=capitale_epuree1[2].split(']')         
    capitale_epuree3=capitale_epuree2[0].split(',')
    capitale=capitale_epuree3[0]
    return capitale

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
        return 'Data not available'
