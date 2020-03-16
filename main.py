import pandas as pd
import time
import bs4
import random
import requests
import itertools as it

import Extract

token = 'https://www.ldlc.com/telephonie/telephonie-portable/mobile-smartphone/c4416/page'

def get_pages(token, nb):
    pages = []
    for i in range(1,nb+1):
        j = token + str(i)
        pages.append(j)
    return pages

pages = get_pages(token,10)
print(pages)

# https://www.proxy-list.download/HTTPS
proxies = pd.read_csv('Ressources/proxy_list.txt', header = None)
proxies = proxies.values.tolist()
proxies = list(it.chain.from_iterable(proxies))

# https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
useragents = pd.read_csv('Ressources/useragents_list.txt',header = None, sep = '-')
useragents = useragents.values.tolist()
useragents = list(it.chain.from_iterable(useragents))

def get_data(pages,proxies):
    
    df = pd.DataFrame()
    # Creation de la liste iterative en boucle pour le proxy et l'user agent
    proxy_pool = it.cycle(proxies)
    ua_pool = it.cycle(useragents)

    while len(pages) > 0:
        for i in pages:
        # on lit les pages une par une et on initialise une table vide pour ranger les données d'une page     
            df_page = pd.DataFrame()
        # itération dans un liste de proxies et de useragents 
            proxy = next(proxy_pool)
            useragent = next(ua_pool)
            
        # essai d'ouverture d'une page
            try:
                response = requests.get(i,proxies={"http": proxy, "https": proxy}, headers={'User-Agent': useragent},timeout=5)
                time.sleep(random.randrange(1,5))
        # lecture du code html et la recherche des balises <p>
                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                df = Extract.extractLdlc(df, df_page, soup)
                
                pages.remove(i)
                print(df.shape)
            except:
                print("Skipping. Connnection error")
                
    return df

data = get_data(pages,proxies)
print(data)