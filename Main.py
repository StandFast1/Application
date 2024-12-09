
# 
import os

# Creation des produits 
class produit:
    def __init__(self, nom, prix, quantite, disponible=True):
        self.nom = nom
        self.prix = float(prix)          # Valeur à virgules
        self.quantite = int(quantite)
        self.disponible = disponible     # Par default disponible

    def __str__(self):
        return f"Produit: {self.nom}, Prix: {self.prix}€, Quantite: {self.quantite}, Disponible : {self.disponible}"  #Indication par produit
    


# Affichage des produits 
def afficher_produits(produits):
    if not produits:
        print("Produit introuvable")
    else:
        print(produits)
    

# Trier les fichiers

# Gestion liste produit
def lire_produits(fichier):
    produits = []
    if os.path.exists(fichier): # verification existance fichier
        with open(fichier, 'r') as f: #ouvir et fermer les fichiers
            for ligne in f: # parcours ligne par ligne
                parts = ligne.strip().split(',') #Suppression espace
                if len(parts) == 4:
                    produits.append(produit(parts[0], parts[1], parts[2, parts[3]])) #verification ligne contien bien 4 valeurs
            produits

# Recherche

# Ajouter/supprimer des produits
def ajouter_produits(fichier, produit):
    with open(fichier, 'a') as f:  # 'a' permet de si fichier deja cree modifier la valeur 
        f.write(f"{produit.nom}, {produit.prix}, {produit.quantite}")

# Menu interactif 
while True : 
     print("Menu")
     print("Voir Liste Produits")
     print("Trier produits")
     print("Rechercher Produits")
     print("Ajouter/supprimer des produits")

