import wptools

def get_info(country):
    page = wptools.page(country)    #On va chercher la page Wikipédia en question
    page.get_parse(False)
    return page.data['infobox'] 
