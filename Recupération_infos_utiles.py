import wptools
import re
#----------------------------------------------------Definition des fonctions-------------------------------------------------

def get_information(country):
    page = wptools.page(country)                             #On va chercher la page Wikipédia voulue
    page.get_parse(False)
    return page.data['infobox'] 


def get_nom(info):
    donnees=info['conventional_long_name']
    nom=donnees.split('{')[0]                                #On isole le nom le plus courant en cas de plusieurs noms existants
    return nom


import re
def get_capitale(info):
    # cas général
    if 'capital' in info:                                    # Si l'information récupérée comporte plusieurs lignes
        capitale = info['capital'].replace('\n',' ')         # on remplace les retours à la ligne par un espace
        
        m = re.match(".*?\[\[([\w\s',(.)|-]+)\]\]", capitale) # le nom de la capitale peut comporter des lettres, des espaces,
                                                             # ou l'un des caractères ',.()|- compris entre crochets [[...]]
        
        capitale = m.group(1)                                # on récupère le contenu des [[...]]
        return capitale      
    
    print(' Could not fetch country capital {}'.format(info))# Cas particulier, si impossible à trouver
    return None

def get_monnaie(info):
    monnaie=''
    liste=['currency']
    for elt in liste:
        if elt in info:
            info_monnaie=info[elt]                           #chaîne de caractères des données
            liste_monnaie=info_monnaie.split('[[')           #extraction de la donnée
            monnaie=liste_monnaie[1].split(']]')[0]
            return monnaie
    if monnaie=='':
        return 'Data not available'
    
    
    
def get_population(info):
    population=''
    liste=['population_census','population_estimate']       #différentes possibilités de noms pour le dictionnaire
    for n in range (len(liste)):
        if liste[n] in info:
            if len(info[liste[n]])>12:                      #il n'y a pas que la population écrite??????
                return 'Data not available'                 #Données compliquées à extraire
            else:
                return info[liste[n]]
        if population=='':
            return 'Data not available'                     #on met la population
        
        
def get_coords(info):    
    liste=['coordinates','largest_city','capital']          #Différents noms possibles pour obtenir des coordonnées
    for elt in liste:
        if elt in info:
                L=info[elt]                                 #chaîne de caractères des données
                L=L.split('|')                              #début de l'extraction des données
                i=0
                while i < (len(L)) and  L[i] not in ['Coord','{{Coord','{{coord','coord','Coord ','{{Coord ','{{coord ','coord ']: #différentes possibilités de débuts pour les coordonnées
                    i+=1
                
                longueur = None
                
                for symb in ['W','W}}','W}} {{coord','E','E}}']:    #différentes chaînes de caractères marquant la fin de la chaîne des données utiles
                    if symb in L:
                        longueur=L.index(symb)+1                    #position des données dans la chaîne
                
                    
                if longueur==i+7:                                   #précision à la minute
                    lat_et_long={}
                    coord=[float(L[i+1]),float(L[i+2]),L[i+3],float(L[i+4]),float(L[i+5]),L[i+6]]
                    coord[1]=coord[1]/60                            #conversion des minutes
                    coord[4]=coord[4]/60
                    lat= coord[0]+coord[1]
                    long= coord[3]+coord[4]
                    if coord[2]=='S':                               #Conversion depuis le système sexiagésimal
                        lat=-lat
                    if coord[5] in ['W','W}} {{coord']:             #Conversion depuis le système sexiagésimal
                        long=-long
                    lat_et_long['latitude']=lat                     #Création d'un dictionnaire
                    lat_et_long['longitude']=long
                    return lat_et_long
                
                elif longueur==i+9:                                 #précision à la seconde
                    lat_et_long={}
                    coord=[float(L[i+1]),float(L[i+2]),L[i+4],float(L[i+5]),float(L[i+6]),L[i+8]]
                    coord[1]=coord[1]/60                            #conversion des minutes
                    coord[4]=coord[4]/60
                    lat= coord[0]+coord[1]
                    long= coord[3]+coord[4]
                    if coord[2]=='S':                               #Conversion depuis le système sexiagésimal
                        lat=-lat
                    if coord[5]=='O':                               #Conversion depuis le système sexiagésimal
                        long=-long
                    lat_et_long['latitude']=lat
                    lat_et_long['longitude']=long
                    return lat_et_long
                
                elif get_nom(info) == 'Republic of Benin' :
                    return {'latitude': 6.4833333, 'longitude': 2.6} #pour le Bénin où les données n'existent pas sur la page Wikipédia
               
                elif get_nom(info) == 'Republic of Mauritius' :
                    return {'latitude': 20.2, 'longitude': 57.5}
                
                else : #Pour l'Afrique du Sud
                    return {'latitude' : -25.7333333, 'longitude':28.1833333}
                

def get_superficie(info):
    sup = ''
    aire = ['area_km2']                                             #On crée une liste contenant les différentes 
    La = len(aire)                                                  #possibilités de débuts pour la superficie
    for i in range(La):
        if aire[i] in info :
            return info[aire[i]]
        if sup == '':                                               #Si la superficie n'est pas disponible 
            return "La superficie n'est pas disponible."
    
  
def get_leader(info) :
    leader = ''
    l_leader = ['leader','leader_name1']
    for elt in l_leader : 
        if elt in info : 
            inf_l = info[elt]
            list_leader = inf_l.split('[[')
            leader = list_leader[1].split(']]')[0]                    #On extrait les données
            return leader
     if leader == '':
        return "Le nom du leader n'est pas disponible."               # Si le nom est introuvable


def get_langues (info):
    langues = ''
    
    if get_nom(info) == "State of Eritrea" : 
        langues = info['national_languages']
        
    elif  get_nom(info) == "Republic of Burundi" or get_nom(info) == "United Republic of Tanzania": 
        langues = info['languages']
        
    
    elif 'official_languages' in info :
        langues = info['official_languages']
        # parfois l'information récupérée comporte plusieurs lignes
        # on remplace les retours à la ligne par un espace
        langues = info['official_languages'].replace('\n',' ')
        
    if ':' in langues :
        langues = langues.split(':')[1]
        
    if 'hlist' in langues : 
        langues = langues.split('hlist')[1]
        
    if 'unbulleted list' in langues :
        langues = langues.split('unbulleted list')[1]
        
    if get_nom(info) == 'Republic of Mauritius' :
        langues_bis = langues.split('<br>')[1] + langues.split('<br>')[2]
        langues = langues_bis.split('{{')[0] + (langues_bis.split('}}')[1]).split('{{')[0]
        
    if get_nom(info) == 'Republic of South Africa' :
        langues = langues.split('"constitution"')[1]
        langues = langues.split('<br/>')[0]
        
    
    langues_list = langues.split('[[')
    langues_txt = ''
        
    def aux (chaine_cara) :
        B = False
            
        for x in chaine_cara :
            if x.isalpha() :
                return True
                
        return (B)
         
    for k in range(len(langues_list)-1):
        if not aux(langues_list[k]) :
            del langues_list[k]
             
    for k in range(len(langues_list)):
        
        if '|' in langues_list[k] :
            if aux(langues_list[k].split('|')[1]) :
                langues_list[k] = langues_list[k].split('|')[1]
                
            else : langues_list[k] = langues_list[k].split('|')[0]
                
        if ']]' in langues_list[k] :
            langues_list[k] = langues_list[k].split(']]')[0]
        
        if '{{' in langues_list[k] :
            langues_list[k] = langues_list[k].split('{{')[0]
            
        if 'title=' in langues_list[k] :
            langues_list[k] = langues_list[k].split('title=')[1]
            
        if k < (len(langues_list)-1) :
            langues_txt += langues_list[k] + ', '
                
        else :
            langues_txt += langues_list[k]

        
    return langues_txt
        
def get_HDI(info):
    HDI=''
    liste=['HDI']
    for elt in liste:
        if elt in info:
            HDI=info[elt]                                              #chaîne de caractères des données
            return HDI
        if HDI=='':
            return 'Data not available'
                
            ############ # faire densité, langues
           
#-------------------------------------------------- Base de données --------------------------------------------------------
    
Afrique=['Algeria','Angola','Benin','Botswana','Burkina_Faso','Burundi','Cameroon',\
         'Cape_Verde','Central_African_Republic','Chad','Comoros','Democratic_Republic_of_the_Congo',\
         'Djibouti','Egypt','Equatorial_Guinea','Eritrea','Eswatini',\
         'Ethiopia','Gabon','Ghana','Guinea','Guinea_Bissau','Ivory_Coast',\
         'Kenya','Lesotho','Liberia','Libya','Madagascar','Malawi','Mali','Mauritania','Mauritus','Morocco',\
         'Mozambique','Namibia','Niger','Nigeria','Republic_of_the_Congo','Rwanda','Sao_Tomé_and_Principe',\
         'Senegal','Seychelles','Sierra_Leone','Somalia','South_Africa','South_Sudan','Sudan','Tanzania',\
         'The_Gambia','Togo','Tunisia','Uganda','Zambia','Zimbabwe'] #ensemble des pays d'Afrique

for pays in Afrique:
    
    import sqlite3
    
    # ouverture d'une connexion avec la base de données
    conn = sqlite3.connect('pays_afrique3.sqlite')
    
    # préparation de la commande SQL
    c = conn.cursor()
    sql = 'INSERT INTO countries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    
    # les infos à enregistrer
    info=get_information(pays)
    nom = get_nom(info)
    capitale = get_capitale(info)
    monnaie = get_monnaie(info)
    lat_et_long = get_coords(info)
    superficie = get_superficie(info)
    population =get_population(info)
    leader=get_leader(info)
    langues = get_langues(info)
    HDI=get_HDI(info)   
    image=pays+'.png'  #pour afficher les images côté client
    
    
    # soumission de la commande (noter que le second argument est un tuple)
    c.execute(sql,(pays, nom, capitale, leader, population, superficie, HDI, monnaie, langues, lat_et_long['latitude'],lat_et_long['longitude'],image))
    conn.commit()
