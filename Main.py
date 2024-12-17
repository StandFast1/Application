import os
from utilisateur import Utilisateur

# Fonction principale :
def gestion():
    fichier = 'produits.txt'
    produits = lecture_produits(fichier)

# Classe Produit 
class Produit:
    def __init__(self, nom, prix, quantite, disponible=True):
        self.nom = nom
        self.prix = float(prix)          
        self.quantite = int(quantite)
        self.disponible = disponible     

    def __str__(self):
        return f"Produit: {self.nom}, Prix: {self.prix}€, Quantite: {self.quantite}, Disponible: {self.disponible}"  # Indication par produit
    

# Lecture produits dans les fichiers
def lecture_produits(fichier):
    produits = []
    if os.path.exists(fichier): 
        with open(fichier, 'r') as f:
            for ligne in f: 
                parts = ligne.strip().split(',') 
                if len(parts) == 4:
                    produits.append(Produit(parts[0], parts[1], parts[2], parts[3])) # Vérification 4 valeurs
    return produits

# Tri normal
def triage_produits(produits, choix):

    if choix == 'nom':
        return sorted(produits, key=lambda x: x.nom)
    
    elif choix == 'prix':
        return sorted(produits, key=lambda x: x.prix)
    
    elif choix == 'quantite':
        return sorted(produits, key=lambda x: x.quantite)
    
    elif choix == 'disponible':
        return sorted(produits, key=lambda x: x.disponible)
    
    else:
        return produits
    
# Algo Tri à bulles 
def triage_bulles_produits(produits, choix):
    n = len(produits)
    for i in range(n):
        for j in range(0, n - i-1):  # -1 pcq le dernier element deja verifier dcp plus besoins

            if choix == 'nom':
                if produits[j].nom > produits[j+1].nom : 
                    produits[j], produits[j+1] = produits[j+1], produits[j]

            elif choix == 'prix':
                if produits[j].prix > produits[j+1].prix : 
                    produits[j], produits[j+1] = produits[j+1], produits[j]


            elif choix == 'quantite':
                if produits[j].quantite > produits[j+1].quantite :
                    produits[j], produits[j+1] = produits[j+1], produits[j]

    return produits

# Recherche 
def rechercher_produit(produits, nom):
    resultat = [p for p in produits if nom.lower() in p.nom.lower()]
    return resultat

# Ajouter des produits
def ajouter_produits(fichier, produit):
    with open(fichier, 'a') as f:  # 'a' permet de si fichier déjà créé modifier la valeur 
        f.write(f"{produit.nom},{produit.prix},{produit.quantite},{produit.disponible}\n")

# Supprimer produit
def supprim_produit(fichier, produits, nom_produit):
    produits = [p for p in produits if p.nom.lower() != nom_produit.lower()]
    
    with open(fichier, 'w') as f:
        for produit in produits:
            f.write(f"{produit.nom},{produit.prix},{produit.quantite},{produit.disponible}\n")
    
    return produits

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
        print("4 - Ajouter des produits")
        print("5 - Supprimer des produits")
        print("6 - Exit")

        choix = input("Choisir : ")

        if choix == '1': 
            afficher_produits(produits)
        
        elif choix == '2':
            print("\nQuel modèle de tri ?\n 1- Normal \n 2- A bulles")
            choix2 = input("Choisir : ")
            if choix2 == '1':
                critere = input("Trier par :\nNom\nPrix\nQuantite\nDisponibilite\nChoisir : ")
                produits = triage_produits(produits, critere.lower())
                afficher_produits(produits)

            elif choix2 == '2':
                critere = input("Trier par :\nNom\nPrix\nQuantite\nDisponibilite\nChoisir : ")
                produits = triage_bulles_produits(produits, critere.lower())
                print(f"\nProduits triés par {critere} avec tri à bulles :")
                afficher_produits(produits)
            
            else:
                print("Valeur incorrecte → Exit")
                
        
        elif choix == '3':
            recherche = input("Produit à rechercher : ")
            resultats = rechercher_produit(produits, recherche)
            afficher_produits(resultats)
        
        elif choix == '4':
            nom = input("Nom : ")
            prix = input("Prix : ")
            quantite = input("Quantité : ")
            disponible = input("Disponible Oui / Non : ")
            produit = Produit(nom, prix, quantite, disponible)
            ajouter_produits(fichier, produit)
            produits.append(produit)
            print("Produit ajouté dans votre réserve")

        elif choix == '5':
            nom_produit = input("Nom du produit à supprimer (ecrire en toute lettre): ")
            produits = supprim_produit(fichier, produits, nom_produit)
            print(f"Produit {nom_produit} supprimé")

        elif choix == '6':
            print("Exit")
            break

        else:
            print("Valeur non valide, veuillez recommencer")

def main():
    gestion_utilisateurs = Utilisateur()
    
    while True:
        print("\n Menu Principal ")
        print("1 - Se connecter")
        print("2 - Créer un compte")
        print("3 - Changer de mot de passe")
        print("4 - Supprimer le compte")
        print("5 - Quitter")
        
        choix = input("Choix : ")
        
        if choix == '1':
            nom = input("Nom d'utilisateur : ")
            mdp = input("Mot de passe : ")
            role = gestion_utilisateurs.connexion(nom, mdp)
            
            if role:
                print(f"Connexion réussie! Rôle : {role}")
                menu_interactif()  # Accès au menu produits
            else:
                print("Connexion échouée")
                
        elif choix == '2':
            while True:
                nom = input("Nom d'utilisateur : ")
                mdp = input("Mot de passe : ")
                
                if gestion_utilisateurs.verif_mot_de_passe_compromis(mdp):
                    print("\nCe mot de passe est compromis!")
                    continue
                
                if gestion_utilisateurs.nouveau_utilisateur(nom, mdp):
                    break
                
        elif choix == '3':
            nom = input("Nom d'utilisateur : ")
            ancien_mdp = input("Ancien mot de passe : ")
            nouveau_mdp = input("Nouveau mot de passe : ")
            
            if gestion_utilisateurs.verif_mot_de_passe_compromis(nouveau_mdp):
                print("\nLe nouveau mot de passe est compromis!")
                continue
                
            gestion_utilisateurs.changement_mdp(nom, ancien_mdp, nouveau_mdp)

        elif choix == '4':
            nom = input("Nom d'utilisateur : ")
            mdp = input("Mot de passe : ")
            
            if gestion_utilisateurs.connexion(nom, mdp):
                gestion_utilisateurs.sup_utilisateur(nom)
            else:
                print("Identifiants incorrects")
            
        elif choix == '5':
            print("Au revoir!")
            break
            
        else:
            print("Option invalide")

if __name__ == "__main__":
    main()


    