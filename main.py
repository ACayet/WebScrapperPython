import pandas as pd
import time
import bs4
import random
import requests
import itertools as it


site = 'https://www.ldlc.com/telephonie/telephonie-portable/mobile-smartphone/c4416/page'

def get_pages(site, nb):
    pages = []
    for i in range(2,nb+1):
        j = site + str(i)
        pages.append(j)
    return pages

pages = get_pages(site,10)
print(pages)


# https://www.proxy-list.download/HTTPS
proxies = pd.read_csv('Assets/proxy_list.txt', header = None)
proxies = proxies.values.tolist()
proxies = list(it.chain.from_iterable(proxies))


# https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
useragents = pd.read_csv('Assets/useragents_list.txt',header = None, sep = '-')
useragents = useragents.values.tolist()
useragents = list(it.chain.from_iterable(useragents))

data_frame = pd.DataFrame()
parameters = ['data-nom','data-connectivite','data-processeur','data-ram','data-ecran','data-stockage','data-surface','data-reseau','data-batterie','data-os','data-prix','data-note','data-nb_avis']

# Creation de la liste iterative en boucle pour le proxy et l'user agent
proxy_pool = it.cycle(proxies)
ua_pool = it.cycle(useragents)


while len(pages) > 0:
    for i in pages:
        #print(i)

        data_frame_page = pd.DataFrame()
        parameters = ['data-nom','data-connectivite','data-processeur','data-ram','data-ecran','data-stockage','data-surface','data-reseau','data-batterie','data-os','data-prix','data-note','data-nb_avis']
        
        # itération dans un liste de proxies et de useragents 
        proxy = next(proxy_pool)
        useragent = next(ua_pool)

        # essai d'ouverture d'une page
        try:
            # Requete au site web et retourne dans la variable 'response.text' le texte html
            response = requests.get(i,proxies={"http": proxy, "https": proxy}, headers={'User-Agent': useragent},timeout=7)
            time.sleep(random.randrange(1,5))
    
            # parse the html using beautiful soup and store in variable 'soup'
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            
            extract_nom = soup.find_all('h3',{'class':'title-3'})
            for j in extract_nom:
                tab = j.text

            extract_desc = soup.find_all('p',{'class':'desc'})
            for j in extract_desc:
                ligne = j.text
                tab = ligne.split(' - ')
                print(tab)
    
            extract_avis = soup.find_all('div',{'class':'ratingClient'})
            for j in extract_avis:
                tab = j.text

            extract_prix = soup.find_all('div',{'class':'price'})
            for j in extract_prix:
                tab = j.text

            # on supprime de la liste la page scrapper    
            pages.remove(i)
        except:
            print("Skipping proxy. Connnection error")
        
#print(tab)


""" 
#extraction des données        
for param in parameters:
    l = []
    for elements in p_box:
        j = elements[param]
        l.append(j)
    l = pd.DataFrame(l, columns = [param])
    df_f = pd.concat([df_f,l], axis = 1)
df = df.append(df_f, ignore_index=True)
                
pages.remove(i)
print(df.shape)
"""
