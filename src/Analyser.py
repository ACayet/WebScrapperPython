import pandas as pd


class Analyser :

    def __init__(self):
        super().__init__()

    def analyseDF(self, data_frame):
        df_analyse = data_frame
        df_analyse['data-ram'] = df_analyse['data-ram'].astype(int)
        df_analyse['data-stockage'] = df_analyse['data-stockage'].astype(int)
        df_analyse['data-batterie'] = df_analyse['data-batterie'].astype(int)
        df_analyse['data-prix'] = df_analyse['data-prix'].astype(float)
        df_analyse['data-note'] = df_analyse['data-note'].astype(float)
        df_analyse['data-nb_avis'] = df_analyse['data-nb_avis'].astype(int)
