import os
from utilisateur import Utilisateur
import pandas as pd
import logging



logging.basicConfig(
    filename='application.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')




# Fonction principale :
def gestion():
    fichier = 'produits.csv'
    if not os.path.exists(fichier):
        df = pd.DataFrame(columns=['nom', 'prix', 'quantite', 'disponible', 'proprietaire'])
        df.to_csv(fichier, index=False)
        return [] 
    return lecture_produits(fichier)

    

# Classe Produit 
class Produit:
    def __init__(self, nom, prix, quantite, disponible):
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
        try:
            df = pd.read_csv(fichier)
            df = df[df['proprietaire'] == proprietaire]
            for _, row in df.iterrows():
                produits.append(Produit(
                    str(row['nom']),
                    float(row['prix']),
                    int(row['quantite']),
                    bool(row['disponible'])
                ))
        except Exception as e:
            print(f"Erreur de lecture du fichier : {e}")
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
    nouveau_produit = pd.DataFrame({
        'nom': [produit.nom],
        'prix': [produit.prix],
        'quantite': [produit.quantite],
        'disponible': [produit.disponible],
        'proprietaire': [proprietaire]
    })
    
    if os.path.exists(fichier):
        df = pd.read_csv(fichier)
        df = pd.concat([df, nouveau_produit])
    else:
        df = nouveau_produit
    
    df.to_csv(fichier, index=False)
    print("Produit ajouté dans votre réserve")





# Supprimer produit
def supprim_produit(fichier, produits, nom_produit):
    df = pd.DataFrame([{'nom': p.nom, 'prix': p.prix, 'quantite': p.quantite, 'disponible': p.disponible} 
                      for p in produits if p.nom.lower() != nom_produit.lower()])
    df.to_csv(fichier, index=False)
    return [p for p in produits if p.nom.lower() != nom_produit.lower()]




# Afficher liste produit
def afficher_produits(produits):
    if not produits:
        print("\nAucun Produit\n")
    else:
        for produit in produits:
            print(produit)





# Menu interactif 
def menu_interactif():
    fichier = 'produits.csv'
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
                logging.info(f'Connexion reussite : {nom}')
                print(f"Connexion réussie au compte {nom} Rôle : {role}")
                menu_interactif(nom)
            else:
                logging.error(f'Connexion echouee : {nom}')
                print(f"Connexion échouée  {nom}")
                
        elif choix == '2':
            while True:
                nom = input("Nom d'utilisateur : ")
                mdp = input("Mot de passe : ")
                email = input("Email : ")
                
                if gestion_utilisateurs.verif_mot_de_passe_compromis(mdp, nom):
                    logging.warning(f'MDP compromis pour le compte {nom}')
                    print("\nCe mot de passe est compromis!")
                    continue
                
                if gestion_utilisateurs.nouveau_utilisateur(nom, mdp, email, role='utilisateur'):
                    logging.info(f'Nouvel utilisateur : {nom}')
                    break
                
        elif choix == '3':
            nom = input("Nom d'utilisateur : ")
            ancien_mdp = input("Ancien mot de passe : ")
            nouveau_mdp = input("Nouveau mot de passe : ")
            
            if gestion_utilisateurs.verif_mot_de_passe_compromis(nouveau_mdp):
                logging.warning(f'MDP compromis pour le compte {nom} ')
                print("\nLe nouveau mot de passe est compromis!")
                print("Le mot de passe doit faire au moins 12 caractères")
                print("Ajouter au moins une lettre majuscule")
                print("Ajouter au moins une lettre minuscule")
                print("Ajouter au moins un chiffre")
                print("Ajouter au moins un caractère spécial (!@#$%^&*)")
                continue
                
            gestion_utilisateurs.changement_mdp(nom, ancien_mdp, nouveau_mdp, email)
            logging.info(f'Changement de mot de passe pour le compte {nom}')

        elif choix == '4':
            nom = input("Nom d'utilisateur : ")
            mdp = input("Mot de passe : ")
            
            if gestion_utilisateurs.connexion(nom, mdp):
                gestion_utilisateurs.sup_utilisateur(nom)
            else:
                logging.warning(f'Identifiants incorrects : {nom}')
                print("Identifiants incorrects")
                
            
        elif choix == '5':
            print("Au revoir!")
            break
            
        else:
            print("Option invalide")

if __name__ == "__main__":
    main()