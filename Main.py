import os, time 


# Fonction principal : 
def gestion():
    fichier = 'produits.txt'
    produits = lecture_produits(fichier)


# Class produit 
class Produit:
    def __init__(self, nom, prix, quantite, disponible=True):
        self.nom = nom
        self.prix = float(prix)          # Valeur à virgules
        self.quantite = int(quantite)
        self.disponible = disponible     # Par default disponible

    def __str__(self):
        return f"Produit: {self.nom}, Prix: {self.prix}€, Quantite: {self.quantite}, Disponible : {self.disponible}"  #Indication par produit
    

# Lecture produits dans les fichiers
def lecture_produits(fichier):
    produits = []
    if os.path.exists(fichier): # verification existance fichier
        with open(fichier, 'r') as f: #ouvir et fermer les fichiers
            for ligne in f: # parcours ligne par ligne
                parts = ligne.strip().split(',') #Suppression espace
                if len(parts) == 4:
                    produits.append(Produit(parts[0], parts[1], parts[2, parts[3]])) #verification ligne contien bien 4 valeurs
    return produits





# Tri
def triage_produits(produits, research):
    if research == 'nom':
        return 
    elif research == 'prix':
        return
    elif research == 'quantite':
        return
    elif research == 'disponible':
        return 
    else:
        return produits
    
# Algo Tri à bulles 
def triage_bulles_produits(produits, research):
    if research == 'nom':
        return
    else:
        produits


# Recherche 
def rechercher_produit(produits, nom):
    resultat = [p for p in produits if nom.lower() in p.nom.lower()]
    return resultat

# Ajouter/supprimer des produits
def ajouter_produits(fichier, produit):
    with open(fichier, 'a') as f:  # 'a' permet de si fichier deja cree modifier la valeur 
        f.write(f"{produit.nom},{produit.prix},{produit.quantite}")

# Supprimer produit
def supprim_produit(fichier, produits):
    with open(fichier, 'a') as f:
        produits = supprim_produit(produits)

# Exit 
#def exit(produits):
    
# Afficher liste produit
def afficher_produits(produits):
    if not produits:
        print("\nAucun Produit\n")
    else:
        for produit in produits:
            print(produit)


# Menu interactif 
def menu_interactif():
    fichier = 'produits.txt'
    produits = lecture_produits(fichier)
    
    while True : 
        print("\n\nMenu")
        print("1 - Voir Liste Produits")
        print("2 - Trier produits")
        print("3 - Rechercher Produits")
        print("4 - Ajouter/supprimer des produits")
        print("5 - Exit")

        choix = input("Choisir : ")

        if choix == '1' :
            afficher_produits(produits)
        
        elif choix == '2':
            research = input("Trie par Nom Prix Quantite Disponibilite :")
            produits_tri = produits_tri(produit, research)
            triage_produits(produits_tri)
        
        elif choix == '3':
            rechercher_produit = input("Produit a rechercher :")
            recherche = rechercher_produit(produit, rechercher_produit)
            rechercher_produit(recherche)
        
        elif choix == '4':
            nom = input("Nom : ")
            prix = input("Prix : ")
            quantite = input("Quantité : ")
            produit = Produit(nom, prix, quantite)
            ajouter_produits(fichier, produit)
            produits.append(produit)
            print("Produit ajouter dans votre reserve")

        elif choix == '5':
            print("Exit")
            break

        else:
            print("Valeur non valide veuillez recommencer")

if __name__ == "__main__":
    menu_interactif()