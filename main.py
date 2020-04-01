import pandas as pd
import itertools as it
import json

from src.Scrapper import Scrapper
from src.Analyser import Analyser
from src.Extractor import Extractor

def getSiteList():
    with open('Assets/site_list.json') as siteList:
        return json.load(siteList)


def getPages(base_url, arg_page, filters, nb):
    pages = []
    pages.append(base_url + filters)
    for i in range(2, nb+1):
        j = base_url + arg_page + str(i) + filters
        pages.append(j)
    return pages

def prepareProxy():
    # https://www.proxy-list.download/HTTPS
    proxies = pd.read_csv('Assets/proxy_list.txt', header=None)
    proxies = proxies.values.tolist()
    proxies = list(it.chain.from_iterable(proxies))
    return proxies

def prepareUserAgent():
    # https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
    useragents = pd.read_csv('Assets/useragents_list.txt', header=None, sep='-')
    useragents = useragents.values.tolist()
    useragents = list(it.chain.from_iterable(useragents))
    return useragents

def main():
    # Initialisation des differentes classes
    scrapping = Scrapper()

    extract_ldlc = Extractor('Ldlc')
    extract_electro_depot = Extractor('ElectroDepot')

    analyse = Analyser()


    # Prepartation du dataframe Panda
    parameters = ['data-nom', 'data-connectivite', 'data-processeur', 'data-ram', 'data-ecran', 'data-stockage', 'data-reseau', 'data-batterie', 'data-os', 'data-prix', 'data-note', 'data-nb_avis']
    data_frame_ldlc = pd.DataFrame()
    data_frame_electro_depot = pd.DataFrame()


    # Creation de la liste iterative en boucle pour le proxy et l'user agent
    proxy_pool = it.cycle(prepareProxy())
    ua_pool = it.cycle(prepareUserAgent())


    # Init des sites a parcourir
    urls = getSiteList()

    pages_ldlc = getPages(urls["sites"]["ldlc"]["base_url"], urls["sites"]["ldlc"]["arg_page"], urls["sites"]["ldlc"]["filter"], 3)
    pages_electro_depot = getPages(urls["sites"]["electro_depot"]["base_url"], urls["sites"]["electro_depot"]["arg_page"], urls["sites"]["electro_depot"]["filter"], 3)


    # Tableaux temporaire 
    tab_ldlc = []
    tab_electro_depot = []


    # Scrapping des sites et extraction
    tab_ldlc = scrapping.scrapPage(pages_ldlc,proxy_pool,ua_pool,extract_ldlc)
    tab_electro_depot = scrapping.scrapPage(pages_electro_depot,proxy_pool,ua_pool,extract_electro_depot)


    # Creation des dataframe
    data_frame_electro_depot = pd.DataFrame(tab_electro_depot, )
    data_frame_electro_depot = data_frame_electro_depot.set_axis(parameters, axis=1)
   
    data_frame_ldlc = pd.DataFrame(tab_ldlc)  
    data_frame_ldlc = data_frame_ldlc.set_axis(parameters,axis=1)

    print("Dataframe : " , data_frame_ldlc, sep='\n')
    print("Dataframe : " , data_frame_electro_depot, sep='\n')
    

    # Analyse statistique
    analyse.analyseDF(data_frame_ldlc)
    #analyse.analyseDF(data_frame_electro_depot)

main()
