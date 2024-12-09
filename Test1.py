import os

# Définition d'une classe pour représenter un produit
class Produit:
    def __init__(self, nom, prix, quantite):
        self.nom = nom
        self.prix = float(prix)
        self.quantite = int(quantite)

    def __str__(self):
        return f"{self.nom}, {self.prix:.2f}€, {self.quantite} unités"

# Fonction pour lire les produits à partir du fichier
def lire_produits(fichier):
    produits = []
    if os.path.exists(fichier):
        with open(fichier, 'r') as f:
            for ligne in f:
                parts = ligne.strip().split(',')
                if len(parts) == 3:
                    produits.append(Produit(parts[0], parts[1], parts[2]))
    return produits

# Fonction pour ajouter un produit
def ajouter_produit(fichier, produit):
    with open(fichier, 'a') as f:
        f.write(f"{produit.nom},{produit.prix},{produit.quantite}\n")

# Fonction pour rechercher un produit par son nom
def rechercher_produit(produits, nom):
    resultat = [p for p in produits if nom.lower() in p.nom.lower()]
    return resultat

# Fonction pour trier les produits par nom ou prix
def trier_produits(produits, critere='nom'):
    if critere == 'nom':
        return sorted(produits, key=lambda p: p.nom)
    elif critere == 'prix':
        return sorted(produits, key=lambda p: p.prix)
    elif critere == 'quantite':
        return sorted(produits, key=lambda p: p.quantite)
    else:
        return produits

# Fonction pour afficher les produits
def afficher_produits(produits):
    if not produits:
        print("Aucun produit trouvé.")
    else:
        for produit in produits:
            print(produit)

# Fonction principale qui gère l'application
def gestion_produits():
    fichier = 'produits.txt'
    produits = lire_produits(fichier)

    while True:
        print("\nMenu :")
        print("1. Ajouter un produit")
        print("2. Rechercher un produit")
        print("3. Afficher tous les produits")
        print("4. Trier les produits")
        print("5. Quitter")
        
        choix = input("Votre choix : ")

        if choix == '1':
            nom = input("Nom du produit : ")
            prix = input("Prix du produit : ")
            quantite = input("Quantité du produit : ")
            produit = Produit(nom, prix, quantite)
            ajouter_produit(fichier, produit)
            produits.append(produit)
            print("Produit ajouté avec succès.")

        elif choix == '2':
            recherche = input("Nom du produit à rechercher : ")
            resultats = rechercher_produit(produits, recherche)
            afficher_produits(resultats)

        elif choix == '3':
            afficher_produits(produits)

        elif choix == '4':
            critere = input("Trier par (nom/prix/quantite) : ")
            produits_triees = trier_produits(produits, critere)
            afficher_produits(produits_triees)

        elif choix == '5':
            print("Merci d'avoir utilisé l'application.")
            break

        else:
            print("Choix invalide, veuillez réessayer.")

# Exécution de l'application
if __name__ == "__main__":
    gestion_produits()
