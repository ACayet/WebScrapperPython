import pandas as pd
import bs4
import json

class Extractor:
    
    site = None

    def __init__(self, site):
        super().__init__()
        self.site = site


    def extractDataLdlc(self, text_reponse):
        html = text_reponse
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
        tab = []

        for j in range(0,len(extract_desc)-1):
            tab_page = []
            tab_page.append(extract_nom[j].text.upper())
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
        return tab

    def extractDataElectroDepot(self, text_reponse):
        html = text_reponse
        soup = bs4.BeautifulSoup(html, 'html.parser')
        extract_product_list = soup.find('div', {'class': 'products wrapper list products-list'})
        extract_nom = extract_product_list.find_all('span', {'class': 'product-item-titre'})
        extract_prix = soup.find_all('div', {'class': 'price-box'})
        extract_avis = soup.find_all('div', {'class': 'rate-vote'})
        tab = []

        for j in range(0,len(extract_nom)):
            tab_page = []
            tab_page.append(extract_nom[j].text.strip().upper().lstrip('SMARTPHONE'))
            for k in range(1, 9):
                tab_page.append(None)
            tab_page.append(extract_prix[j].text.replace('€','.').strip())
            avis = extract_avis[j].text.strip().split('(')
            if avis[1].rstrip(')') == '0':
                tab_page.append(None)
            else:
                tab_page.append(avis[0].rstrip())
            tab_page.append(avis[1].rstrip(')'))   
            tab.append(tab_page)
        return tab