import json
import os
import pandas as pd
from datetime import datetime
import uuid
import logging

class GestionCommandes:
    def __init__(self):
        self.fichiers = {
            'acceptees': 'commandes_acceptees.json',
            'refusees': 'commandes_refusees.json'
        }
        self.initialiser_fichiers()
        
    def initialiser_fichiers(self):
        for fichier in self.fichiers.values():
            if not os.path.exists(fichier):
                with open(fichier, 'w', encoding='utf-8') as f:
                    json.dump([], f)

    def creer_commande(self, client, vendeur, produit, quantite, prix_unitaire):
        return {
            "id": str(uuid.uuid4()),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "client": client,
            "vendeur": vendeur,
            "produit": produit,
            "quantite": quantite,
            "prix_unitaire": prix_unitaire,
            "prix_total": quantite * prix_unitaire
        }

    def verifier_stock(self, produit, quantite):
        try:
            df = pd.read_csv('produits.csv')
            df['nom'] = df['nom'].str.strip()  # Enlève les espaces
            produit_data = df[df['nom'].str.lower() == produit.lower()]
            if produit_data.empty:
                return False
            stock = produit_data['quantite'].iloc[0]
            return int(stock) >= quantite
        except Exception as e:
            logging.error(f"Erreur: {str(e)}")
            return False

    def sauvegarder_commande(self, commande, acceptee=True):
        fichier = self.fichiers['acceptees'] if acceptee else self.fichiers['refusees']
        commandes = []
    
        try:
            if os.path.exists(fichier) and os.path.getsize(fichier) > 0:
                with open(fichier, 'r', encoding='utf-8') as f:
                    commandes = json.load(f)
        
            commandes.append(commande)
            with open(fichier, 'w', encoding='utf-8') as f:
                json.dump(commandes, f, indent=4, ensure_ascii=False)
            return True
        
        except Exception as e:
            logging.error(f"Erreur sauvegarde commande: {str(e)}")
            return False

    def mettre_a_jour_stock(self, produit, quantite):
        try:
            df = pd.read_csv('produits.csv')
            masque = df['nom'] == produit
            df.loc[masque, 'quantite'] -= quantite
            df.to_csv('produits.csv', index=False)
            return True
        except Exception as e:
            logging.error(f"Erreur mise à jour stock: {str(e)}")
            return False

    def traiter_commande(self, client, vendeur, produit, quantite, prix_unitaire):
        commande = self.creer_commande(client, vendeur, produit, quantite, prix_unitaire)
        
        if self.verifier_stock(produit, quantite):
            if self.sauvegarder_commande(commande, True) and self.mettre_a_jour_stock(produit, quantite):
                logging.info(f"Commande acceptée: {commande['id']}")
                return True, commande
        
        self.sauvegarder_commande(commande, False)
        logging.warning(f"Commande refusée: {commande['id']}")
        return False, commande