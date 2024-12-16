import csv
import os
import hashlib
import base64




# Class Utilisateur 
class Utilisateur:
    def __init__(self, fichier_utilisateur = 'utilisateur.csv') :
        self.fichier_utilisateur = fichier_utilisateur
        self.creation_compte()



    def creation_compte(self):
        if not os.path.exists(self.fichier_utilisateur):
            with open(self.fichier_utilisateur, 'w', newline='') as fichier:
                writer = csv.writer(fichier)
                writer.writerow(['nom_utilisateur', 'mot_de_passe', 'role'])

 # Verification utilisateur
    def verification_utilisateur(self,nom_utilisateur):
        with open(self.fichier_utilisateur, 'r') as fichier:
            lecture = csv.DictReader(fichier)
            return any(ligne['nom_utilisateur'] == nom_utilisateur for ligne in lecture)


 # Creation d'un utilisateur
    def nouveau_utilisateur(self, nom_utilisateur, mot_de_passe, role='utilisateur'):
        if self.verification_utilisateur(nom_utilisateur):
            print("Nom utilisateur déjà réservé")
            return False
    
        with open(self.fichier_utilisateur, 'a', newline='') as fichier:
        # Hash mdp
            sel = os.urandom(16)
            mot_de_passe_sale = sel + mot_de_passe.encode()
            hachage = hashlib.sha256(mot_de_passe_sale).hexdigest()
            sel_encode = base64.b64encode(sel).decode()
            mot_de_passe_final = f"{sel_encode}${hachage}"  # Format correct sel$hash
        
            writer = csv.writer(fichier)
            writer.writerow([nom_utilisateur, mot_de_passe_final, role])

        print(f"Utilisateur {nom_utilisateur} a bien été ajouté")
        return True
    
# === Changement MDP ===
    def changement_mdp(self, nom_utilisateur, A_mot_de_passe, N_mot_de_passe):
        utilisateur = []
        utilisateur_trouve = False

        with open(self.fichier_utilisateur, 'r') as fichier: 
            lecture = csv.DictReader(fichier)

            for ligne in lecture:
                if ligne['nom_utilisateur'] == nom_utilisateur:
                    if self.verification_mdp(A_mot_de_passe, ligne['mot_de_passe']):
                        ligne['mot_de_passe'] = self.hashage_mdp(N_mot_de_passe)
                        utilisateur_trouve = True
                        break

        if utilisateur_trouve:
            with open(self.fichier_utilisateur, 'w', newline='') as fichier:
                writer = csv.DictWriter(fichier, fieldnames=['nom_utilisateur', 'mot_de_passe_hash', 'role'])
                writer.writeheader()
                writer.writerow(utilisateur)
            print("Password bien modifie")
            return True
        else:
            print("Password Non change")
            return False

# === Hashage MDP ===
    def hashage_mdp(sel, mot_de_passe):
        sel = os.urandom(16)
        mot_de_passe = sel + mot_de_passe.encode()
        hachage = hashlib.sha256(mot_de_passe).hexdigest()
        hachage = base64.b64encode(sel).decode()
        mot_de_passe = f"{hachage}"

# === Verification MDP ===
    def verification_mdp(self, mot_de_passe, hash_stocke):
        try:
            sel_encode, hash_original = hash_stocke.split('$')
            sel = base64.b64decode(sel_encode)
            mot_de_passe_sale = sel + mot_de_passe.encode()
            nouveau_hash = hashlib.sha256(mot_de_passe_sale).hexdigest()
            return nouveau_hash == hash_original
        except:
            return False
        
# === Connexion a un compte existant ===
    def connexion(self, nom_utilisateur, mot_de_passe):
        try:
            with open(self.fichier_utilisateur, 'r') as fichier:
                lecteur = csv.DictReader(fichier)
                for ligne in lecteur:
                    if ligne['nom_utilisateur'] == nom_utilisateur:
                        print(f"Vérification du mot de passe pour {nom_utilisateur}")   
                        if self.verification_mdp(mot_de_passe, ligne['mot_de_passe']):
                            return ligne.get('role', 'utilisateur')
        except Exception as e:
            print(f"Erreur lors de la connexion: {e}")  
        return None
    
# === Supression Utilisateur ===
    def sup_utilisateur(self, nom_utilisateur):
        lignes = []
        utilisateur_trouve = False

        with open(self.fichier_utilisateur, 'r') as fichier:
            lecteur = csv.DictReader(fichier)
            lignes = [ligne for ligne in lecteur if ligne['nom_utilisateur'] != nom_utilisateur]
            utilisateur_trouve = len(lignes) < fichier.tell()

        if utilisateur_trouve:
            with open(self.fichier_utilisateur, 'w', newline='') as fichier:
                writer = csv.DictWriter(fichier, fieldnames=['nom_utilisateur', 'mot_de_passe_hash', 'role'])
                writer.writeheader()
                writer.writerows(lignes)
            print(f"Utilisateur {nom_utilisateur} supprimé avec succès.")
            return True
        else:
            print("Utilisateur non trouvé.")
            return False
        
    def verif_mot_de_passe_compromis(self, mot_de_passe, fichier_rockyou='rockyou.txt'):
    
        try:
            with open(fichier_rockyou, 'r', encoding='utf-8', errors='ignore') as f:
                return mot_de_passe in (ligne.strip() for ligne in f)
        except FileNotFoundError:
            print("Attention: fichier rockyou.txt non trouvé")
            return False
        except Exception as e:
            print(f"Erreur lors de la vérification du mot de passe: {e}")
            return False

        


    
        


  
     
     
def menu():
    gestion = Utilisateur()

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
            gestion.nouveau_utilisateur(nom_utilisateur, mot_de_passe)

            if gestion.verif_mot_de_passe_compromis(mot_de_passe):
                    print("Mot de passe compromis")
                    continue
                
            if gestion.nouveau_utilisateur(nom_utilisateur, mot_de_passe):
                break
             
        elif choix == '2':
            nom_utilisateur = input("Indiquer nom utilisateur: ")
            mot_de_passe = input("indiquer mot de passe: ")
            role = gestion.connexion(nom_utilisateur, mot_de_passe)

            if role :
                print(f"Connexion reussite {role}")
            else:
                print("connexion echoue")

        
        elif choix == '3':
            nom_utilisateur = input("Indiquer nom utilisateur: ")
            mot_de_passe = input("indiquer mot de passe: ")
            gestion.changement_mdp(nom_utilisateur)
            
        
        elif choix == '4':
            nom_utilisateur = input("Indiquer nom utilisateur: ")
            mot_de_passe = input("indiquer mot de passe: ")

            if gestion.verification_utilisateur(nom_utilisateur, mot_de_passe):
                gestion.sup_utilisateur(nom_utilisateur)
                print("Utilisateur Supprimer")
            else:
                print("Faux")
        
        elif choix == '5':
            print("Exit")
            break

        else:
            print("Numero non referencier")
    




if __name__ == "__main__":
    menu()