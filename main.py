import pandas as pd
import time
import bs4
import random
import requests
import itertools as it
import json


def getSiteList():
    with open('Assets/site_list.json') as siteList:
        return json.load(siteList)


def get_pages(base_url, arg_page, filters, nb):
    pages = []
    pages.append(base_url + filters)
    for i in range(2, nb+1):
        j = base_url + arg_page + str(i) + filters
        pages.append(j)
    return pages


def main():

    urls = getSiteList()

    pages_ldlc = get_pages(urls["sites"]["ldlc"]["base_url"], urls["sites"]["ldlc"]["arg_page"], urls["sites"]["ldlc"]["filter"], 3)
    pages_electro_depot = get_pages(urls["sites"]["electro_depot"]["base_url"], urls["sites"]["ldlc"]["arg_page"], urls["sites"]["ldlc"]["filter"], 3)

    # https://www.proxy-list.download/HTTPS
    proxies = pd.read_csv('Assets/proxy_list.txt', header=None)
    proxies = proxies.values.tolist()
    proxies = list(it.chain.from_iterable(proxies))


    # https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
    useragents = pd.read_csv('Assets/useragents_list.txt', header=None, sep='-')
    useragents = useragents.values.tolist()
    useragents = list(it.chain.from_iterable(useragents))

    data_frame = pd.DataFrame()
    parameters = ['data-nom', 'data-connectivite', 'data-processeur', 'data-ram', 'data-ecran', 'data-stockage', 'data-reseau', 'data-batterie', 'data-os', 'data-prix', 'data-note', 'data-nb_avis']

    # Creation de la liste iterative en boucle pour le proxy et l'user agent
    proxy_pool = it.cycle(proxies)
    ua_pool = it.cycle(useragents)

    tab = []

    while len(pages_ldlc) > 0:
        for i in pages_ldlc:
            # print(i)

            data_frame_page = pd.DataFrame()
            parameters = ['data-nom', 'data-connectivite', 'data-processeur', 'data-ram', 'data-ecran', 'data-stockage', 'data-reseau', 'data-batterie', 'data-os', 'data-prix', 'data-note', 'data-nb_avis']

            # itération dans un liste de proxies et de useragents
            proxy = next(proxy_pool)
            useragent = next(ua_pool)

            # essai d'ouverture d'une page
            try:
                # Requete au site web et retourne dans la variable 'response.text' le texte html
                response = requests.get(i, proxies={"http": proxy, "https": proxy}, headers={'User-Agent': useragent}, timeout=7)
                time.sleep(random.randrange(1, 5))

                html = response.text
                
                # parse the html using beautiful soup and store in variable 'soup'
                soup = bs4.BeautifulSoup(html, 'html.parser')

                html = html[html.index("dataLayer.push("):]
                html = html[:html.index("</script>")]
                html = html.replace("dataLayer.push(", "")
                html = html.replace(");", "")
                html = html.replace("'", "\"")

                # Conversion en json
                json_Prix = json.loads(html)

                extract_nom = soup.find_all('h3', {'class': 'title-3'})
                extract_desc = soup.find_all('p', {'class': 'desc'})
                extract_avis = soup.find_all('div', {'class': 'ratingClient'})
                
                

                for j in range(0,len(extract_desc)-1):
                    tab_page = []
                    tab_page.append(extract_nom[j].text)
                    tab_page.extend(extract_desc[j].text.split(' - '))
                    tab_page.append(json_Prix["ecommerce"]["impressions"][j+1]["price"])
                    note = extract_avis[j].find('span')
                    if note is None:
                        tab_page.append(None)
                        tab_page.append("0")
                    else:
                        tab_page.append(note["class"][0].lstrip("star-"))
                        tab_page.append(extract_avis[j].text.strip("\n ").rstrip(" avis"))
                    tab.append(tab_page)
                
                # on supprime de la liste la page scrapper
                pages_ldlc.remove(i)
            except:
                print("Skipping proxy. Connnection error")
    print(*tab, sep = "\n")

main()
