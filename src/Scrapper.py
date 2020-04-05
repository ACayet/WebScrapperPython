import time
import random
import requests



class Scrapper:
    
    def __init__(self):
        super().__init__()
        

    def scrapPage(self, pages, proxy_pool, user_agent_pool, extract, funcExtract):
        tab_temp = []
        while len(pages) > 0:
            for i in pages:

                # itération dans un liste de proxies et de useragents
                proxy = next(proxy_pool)
                useragent = next(user_agent_pool)

                # essai d'ouverture d'une page
                try:
                    # Requete au site web et retourne dans la variable 'response.text' le texte html
                    response = requests.get(i, proxies={"http": proxy, "https": proxy}, headers={'User-Agent': useragent}, timeout=7)
                    time.sleep(random.randrange(1, 5))
                    
                    # Extraction avec la fonction d'extraction passé en argument
                    tab_temp.extend(funcExtract(response.text))

                    # on supprime de la liste la page scrapper
                    pages.remove(i)
                except:
                    print("Skipping proxy. Connnection error")
        return tab_temp