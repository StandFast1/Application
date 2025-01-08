import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from datetime import datetime

class Statistiques:
    def generer_graphiques(self):
        try:
            # Données commandes
            with open('commandes_acceptees.json', 'r') as f:
                commandes = json.load(f)
            df_commandes = pd.DataFrame(commandes)
            
            # Données produits
            df_produits = pd.read_csv('produits.csv')

            # Mise en page
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

            # 1. Commandes par produit
            df_commandes.groupby('produit')['quantite'].sum().plot(kind='bar', ax=ax1)
            ax1.set_title('Quantités vendues par produit')

            # 2. Chiffre d'affaires par produit
            df_commandes.groupby('produit')['prix_total'].sum().plot(kind='pie', ax=ax2)
            ax2.set_title('Chiffre d\'affaires par produit')

            # 3. État des stocks
            df_produits.plot(kind='bar', x='nom', y='quantite', ax=ax3)
            ax3.set_title('Stocks disponibles')

            # 4. Evolution temporelle des ventes
            df_commandes['date'] = pd.to_datetime(df_commandes['date'])
            df_commandes.groupby('date')['prix_total'].sum().plot(ax=ax4)
            ax4.set_title('Evolution des ventes')

            plt.tight_layout()
            plt.savefig('statistiques.png')
            plt.close()

        except Exception as e:
            print(f"Erreur génération graphiques: {str(e)}")