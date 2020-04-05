import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Analyser :

    def __init__(self):
        super().__init__()

    def prepareVarDF(self, df_analyse):
        df_analyse['data-ram'] = df_analyse['data-ram'].astype(int)
        df_analyse['data-stockage'] = df_analyse['data-stockage'].astype(int)
        df_analyse['data-batterie'] = df_analyse['data-batterie'].astype(int)
        df_analyse['data-prix'] = df_analyse['data-prix'].astype(float)
        df_analyse['data-note'] = df_analyse['data-note'].astype(float)
        df_analyse['data-nb_avis'] = df_analyse['data-nb_avis'].astype(int)
        return df_analyse

    def boiteMoustachePrixRam(self, df_analyse):
        #Boite a moustache du prix en fonction des Ram => par GB repartition du prix
        temp_df1 = df_analyse  [["data-prix","data-ram"]]
        ax = temp_df1.boxplot(column='data-prix',by='data-ram')
        ax.set_title("Boite à moustache du prix par Gb de ram")
        ax.set_ylabel('Prix en €')
        ax.set_xlabel('Nb de Gb de RAM')
        plt.show()

    def camembertStockage(self, df_analyse):
        #Repartition du stockage
        temp_df1 = df_analyse  [["data-stockage"]]
        temp_df1['data-stockage'].value_counts().plot.pie().set_title("Repartition du stockage")
        plt.show()

    def camembertRam(self, df_analyse):
        #Repartition Ram
        temp_df1 = df_analyse  [["data-ram"]]
        temp_df1['data-ram'].value_counts().plot.pie().set_title("Repartition de la RAM")
        plt.show()

    def densitePrix(self, df_analyse):
        #Fonction de densité du prix
        temp_df1 = df_analyse  [["data-prix"]]
        sns.distplot(temp_df1['data-prix'], hist=True, kde=True, 
             bins=int(180/5), color = 'darkblue', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4}).set_title("Fonction de densité et histogramme par prix")
        plt.show()

    def densiteBatterie(self, df_analyse):
        #fonction de densité du niveau de batterie
        temp_df1 = df_analyse  [["data-batterie"]]
        sns.distplot(temp_df1['data-batterie'], hist=True, kde=True, 
             bins=int(180/5), color = 'darkblue', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4}).set_title("Fonction de densité et histogramme par niveau de batterie")
        plt.show()

    def evolvePrixMoyenRam(self, df_analyse):
        #Courbe d'évolution du prix moyen en fonction des gb de ram 
        temp_df1 = df_analyse  [["data-prix","data-ram"]]
        temp_df1 = temp_df1.groupby(temp_df1["data-ram"])["data-prix"].mean()
        ax1 = temp_df1.plot()
        ax1.set_title("Courbe d'évolution du prix moyen en fonction des Gb de ram")
        ax1.set_xlabel('Nb de Gb de RAM')
        ax1.set_ylabel('prix moyen en €')
        plt.show()

    def corelation(self, df_analyse):
        #Corélation avec coef de Pearson
        temp_df1 = df_analyse  [["data-prix","data-ram"]]
        pearsoncorr = temp_df1.corr(method='pearson')
        sns.heatmap(pearsoncorr, 
            xticklabels=pearsoncorr.columns,
            yticklabels=pearsoncorr.columns,
            cmap='RdBu_r',
            annot=True,
            linewidth=0.5)
        plt.show()

    def analyseDF(self, data_frame):
        df_analyse = data_frame
        df_analyse = self.prepareVarDF(df_analyse)
        self.camembertStockage(df_analyse)
        self.camembertRam(df_analyse)
        self.densitePrix(df_analyse)
        self.densiteBatterie(df_analyse)
        self.corelation(df_analyse)
        self.boiteMoustachePrixRam(df_analyse)
        self.evolvePrixMoyenRam(df_analyse)