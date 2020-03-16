import pandas as pd
import bs4

class Extract:
    
    def __init__(self):
        super.__init__()

    @staticmethod
    def extractLdlc(df, df_f, soup):

        
        parameters = ['data-prix','data-codepostal','data-idagence','data-idannonce','data-nb_chambres','data-nb_pieces','data-surface','data-typebien']

        p_box = soup.find_all("p", {"class":"desc"})
        # extraction des données        
        for param in parameters:
            l = []
            for elements in p_box:
                j = elements[param]
                l.append(j)
            l = pd.DataFrame(l, columns = [param])
            df_f = pd.concat([df_f,l], axis = 1)
        df = df.append(df_f, ignore_index=True)

        return df