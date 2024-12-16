import csv
import os
import hashlib
import base64
import pandas as pd



# Class Utilisateur 
class utilisateur:
    def __init__(self, fichier_utilisateur = 'utilisateur.csv') :
        self.fichier_utilisateur = fichier_utilisateur
        self.creation_compte()



    def creation_compte(self):
        if not os.path.exists(self.fichier_utilisateur):

            with open(self.fichier_utilisateur, 'w', newline='') as fichier:
                writer = csv.writer(fichier)
                writer.writerow(['nom_utilisateur', 'mot_de_passe', 'grade'])

 # Verification utilisateur
    def verification_utilisateur(self,nom_utilisateur):
        with open(self.fichier_utilisateur, 'r') as fichier:
            lecture = csv.DictReader(fichier)
            return any(ligne['nom_utilisateur'] == nom_utilisateur for ligne in lecture)


 # Creation d'un utilisateur
    def nouveau_utlisateur(self, nom_utilisateur, mot_de_passe, role='utilisateur'):
        if self.verification_utilisateur(nom_utilisateur):
            print("Nom utilisateur deja reserve")
            return False
    
        with open(self.fichier_utilisateur, 'a') as fichier:
           # Hash mdp
            sel = os.urandom(16)
            mot_de_passe = sel + mot_de_passe.encode()
            hachage = hashlib.sha256(mot_de_passe).hexdigest()
            hachage = base64.b64encode(sel).decode()
            mot_de_passe = f"{hachage}"
            
            
            writer = csv.writer(fichier)
            writer.writerow([nom_utilisateur, mot_de_passe])



        print(f"Utilisateur {nom_utilisateur} à bien été ajoute")
        return True
    
    def changement_mdp(self, nom_utilisateur, A_mot_de_passe, N_mot_de_passe):
        ligne = []
        utilisateur_trouve = False

        with open(self.fichier_utilisateur, 'r') as fichier: 
            lecture = csv.DictReader(fichier)
            ligne = list(lecture)

        for ligne in ligne:
            if ligne['nom_utilisateur'] == nom_utilisateur:
                if ligne['mot_de_passe'] == self.hashage_mdp(A_mot_de_passe):
                    ligne['mot_de_passe_hash'] = self.hashage_mdp(N_mot_de_passe)
                    utilisateur_trouve = True
                    break

        if utilisateur_trouve:
            with open(self.fichier_utilisateur, 'w', newline='') as fichier:
                writer = csv.DictWriter(fichier, nouveau=['nom_utilisateur', 'mot_de_passe_hash', 'role'])
                writer.writeheader()
                writer.writerow(ligne)
            print("Password bien modifie")
            return True
        else:
            print("Password Non change")
            return False

    def hashage_mdp(sel, mot_de_passe): 
        sel = os.urandom(16)
        mot_de_passe = sel + mot_de_passe.encode()
        hachage = hashlib.sha256(mot_de_passe).hexdigest()
        hachage = base64.b64encode(sel).decode()
        mot_de_passe = f"{hachage}"
    
    #def connexion():
        # Rentrer donne utilisateur
        
        # Verification bon user
        # Donner accès
    
        


  
     
     
def menu():
    gestion = utilisateur()

    while True:
        print("\n\nMenu")
        print("1 - Creation compte")
        print("2 - Se connecter")
        print("3 - Changer de password")
        print("4 - Supprimer le compte")
        print("5 - Exit")

        choix = input("Choisir un numero: ")

        if choix == '1':
            nom_utilisateur = input("Indiquer nom utilisateur: ")
            mot_de_passe = input("indiquer mot de passe: ")
            gestion.nouveau_utlisateur(nom_utilisateur, mot_de_passe)
             
        elif choix == '2':
            nom_utilisateur = input("Indiquer nom utilisateur: ")
            mot_de_passe = input("indiquer mot de passe: ")
            role = gestion.verification_utilisateur(nom_utilisateur, mot_de_passe)

            if role :
                print(f"Connexion reussite {role}")
            else:
                print("connexion echoue")

        
        elif choix == '3':
            nom_utilisateur = input("Indiquer nom utilisateur: ")
            mot_de_passe = input("indiquer mot de passe: ")
            gestion.changement_mdp(nom_utilisateur, mot_de_passe)
            
        
        elif choix == '4':
            print("Fonctionnalite en dev")
        
        elif choix == '5':
            print("Exit")
            break

        else:
            print("Numero non referencier")
    




if __name__ == "__main__":
    menu()