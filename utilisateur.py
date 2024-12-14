import csv
import os
import hashlib
import base64



# Class Utilisateur 
class utilisateur:
    def __init__(self, fichier_utilisateur = 'utilisateur.csv') :
        self.fichier_utilisateur = fichier_utilisateur
        self.creation_compte()



    def creation_compte(self, fichier_utilisateur):
        if not os.path.exists(self.fichier_utilisateur):

            with open(self.fichier_utilisateur, 'w', newline='') as fichier:
                writer = csv.writer(fichier)
                writer.writerow(['nom_utilisateur', 'mot_de_passe', 'grade'])

 # Verification utilisateur
    def verification_utilisateur(nom_utilisateur, fichier_utilisateur):
        with open(self.fichier_utilisateur, 'r') as fichier:
            lecture = csv.Dialect(fichier)
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
            
            
            writer = csv.writer(fichier)
            writer.writerow(nom_utilisateur, mot_de_passe)



        print(f"Utilisateur {nom_utilisateur} à bien été ajoute")
        return True
    
    
        


  
     
     
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

        
        #elif choix == '3':
            
        
        #elif choix == '4':
        
        #elif choix == '5':
           # print("Exit")
            #break

        else:
            print("Numero non referencier")
    




if __name__ == "__main__":
    menu()