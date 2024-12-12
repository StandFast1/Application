import csv
import os



# Class Utilisateur 
class utilisateur:
    def __init__(self, fichier_utilisateur='utilisateur.csv') :
        self.fichier_utilisateur = fichier_utilisateur
    

def creation_compte(self):
        if not os.path.exists(self.fichier_utilisateurs):

            with open(self.fichier_utilisateurs, 'w', newline='') as fichier:
                writer = csv.writer(fichier)
                writer.writerow(['nom_utilisateur', 'mot_de_passe', 'grade'])

# Verification utilisateur
def verification_utilisateur():
    with open(self.fichier_utilisateur, 'r') as fichier:
        lecture = csv.Dialect(fichier)
        return any(ligne['nom_utilisateur'] == nom_utilisateur for ligne in lecture)


# Creation d'un utilisateur
def nouveau_utlisateur():
    if self.

def nom_utilisateur():
    
    
def mot_de_passe():
     
     
     
     
     
     
     
def menu():
    gestion = utilisateur()

    while True:
        print("\n\nMenu")
        print("1 - Creation compte")
        print("2 - Se connecter")
        print("3 - Changer de password")
        print("4 - Supprimer le compte")
        print("5 - Exit")

        choix = int("Choisir un numero: ")

        if choix == '1':
            nom_utilisateur = input("Indiquer nom utilisateur: ")
            mot_de_passe = input("indiquer mot de passe: ")
            gestion.nouveau_utilisateur(nom_utilisateur, mot_de_passe)
             
        elif choix == '2': 
        
        elif choix == '3':
        
        elif choix == '4':
        
        elif choix == '5':
            print("Exit")
            break

        else:
            print("Numero non referencier")
    




if __name__ == "":
    x