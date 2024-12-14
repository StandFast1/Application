import csv
import os
import hashlib
import getpass

class GestionUtilisateurs:
    def __init__(self, fichier_utilisateurs='utilisateurs.csv'):
        self.fichier_utilisateurs = fichier_utilisateurs
        self.creer_fichier_si_inexistant()

    def creer_fichier_si_inexistant(self):
        """Créer le fichier CSV s'il n'existe pas"""
        if not os.path.exists(self.fichier_utilisateurs):
            with open(self.fichier_utilisateurs, 'w', newline='') as fichier:
                writer = csv.writer(fichier)
                writer.writerow(['nom_utilisateur', 'mot_de_passe_hash', 'role'])

    def hasher_mot_de_passe(self, mot_de_passe):
        """Hacher le mot de passe avec SHA-256"""
        return hashlib.sha256(mot_de_passe.encode()).hexdigest()

    def verifier_utilisateur_existant(self, nom_utilisateur):
        """Vérifier si un utilisateur existe déjà"""
        with open(self.fichier_utilisateurs, 'r') as fichier:
            lecteur = csv.DictReader(fichier)
            return any(ligne['nom_utilisateur'] == nom_utilisateur for ligne in lecteur)

    def ajouter_utilisateur(self, nom_utilisateur, mot_de_passe, role='utilisateur'):
        """Ajouter un nouvel utilisateur"""
        if self.verifier_utilisateur_existant(nom_utilisateur):
            print("Ce nom d'utilisateur existe déjà.")
            return False

        mot_de_passe_hash = self.hasher_mot_de_passe(mot_de_passe)

        with open(self.fichier_utilisateurs, 'a', newline='') as fichier:
            writer = csv.writer(fichier)
            writer.writerow([nom_utilisateur, mot_de_passe_hash, role])
        
        print(f"Utilisateur {nom_utilisateur} ajouté avec succès.")
        return True

    def authentifier_utilisateur(self, nom_utilisateur, mot_de_passe):
        """Authentifier un utilisateur"""
        mot_de_passe_hash = self.hasher_mot_de_passe(mot_de_passe)

        with open(self.fichier_utilisateurs, 'r') as fichier:
            lecteur = csv.DictReader(fichier)
            for ligne in lecteur:
                if (ligne['nom_utilisateur'] == nom_utilisateur and 
                    ligne['mot_de_passe_hash'] == mot_de_passe_hash):
                    return ligne['role']
        
        return None

    def supprimer_utilisateur(self, nom_utilisateur):
        """Supprimer un utilisateur"""
        lignes = []
        utilisateur_trouve = False

        with open(self.fichier_utilisateurs, 'r') as fichier:
            lecteur = csv.DictReader(fichier)
            lignes = [ligne for ligne in lecteur if ligne['nom_utilisateur'] != nom_utilisateur]
            utilisateur_trouve = len(lignes) < fichier.tell()

        if utilisateur_trouve:
            with open(self.fichier_utilisateurs, 'w', newline='') as fichier:
                writer = csv.DictWriter(fichier, fieldnames=['nom_utilisateur', 'mot_de_passe_hash', 'role'])
                writer.writeheader()
                writer.writerows(lignes)
            print(f"Utilisateur {nom_utilisateur} supprimé avec succès.")
            return True
        else:
            print("Utilisateur non trouvé.")
            return False

    def changer_mot_de_passe(self, nom_utilisateur, ancien_mot_de_passe, nouveau_mot_de_passe):
        """Changer le mot de passe d'un utilisateur"""
        lignes = []
        utilisateur_trouve = False

        with open(self.fichier_utilisateurs, 'r') as fichier:
            lecteur = csv.DictReader(fichier)
            lignes = list(lecteur)

        for ligne in lignes:
            if ligne['nom_utilisateur'] == nom_utilisateur:
                if ligne['mot_de_passe_hash'] == self.hasher_mot_de_passe(ancien_mot_de_passe):
                    ligne['mot_de_passe_hash'] = self.hasher_mot_de_passe(nouveau_mot_de_passe)
                    utilisateur_trouve = True
                    break

        if utilisateur_trouve:
            with open(self.fichier_utilisateurs, 'w', newline='') as fichier:
                writer = csv.DictWriter(fichier, fieldnames=['nom_utilisateur', 'mot_de_passe_hash', 'role'])
                writer.writeheader()
                writer.writerows(lignes)
            print("Mot de passe modifié avec succès.")
            return True
        else:
            print("Authentification échouée.")
            return False

def menu_principal():
    """Menu principal de gestion des utilisateurs"""
    gestion = GestionUtilisateurs()

    while True:
        print("\n--- Gestion des Utilisateurs ---")
        print("1. Créer un compte")
        print("2. Se connecter")
        print("3. Changer de mot de passe")
        print("4. Supprimer un compte")
        print("5. Quitter")

        choix = input("Votre choix : ")

        if choix == '1':
            nom_utilisateur = input("Nom d'utilisateur : ")
            mot_de_passe = getpass.getpass("Mot de passe : ")
            gestion.ajouter_utilisateur(nom_utilisateur, mot_de_passe)

        elif choix == '2':
            nom_utilisateur = input("Nom d'utilisateur : ")
            mot_de_passe = getpass.getpass("Mot de passe : ")
            role = gestion.authentifier_utilisateur(nom_utilisateur, mot_de_passe)
            
            if role:
                print(f"Connexion réussie. Rôle : {role}")
            else:
                print("Échec de connexion.")

        elif choix == '3':
            nom_utilisateur = input("Nom d'utilisateur : ")
            ancien_mot_de_passe = getpass.getpass("Ancien mot de passe : ")
            nouveau_mot_de_passe = getpass.getpass("Nouveau mot de passe : ")
            gestion.changer_mot_de_passe(nom_utilisateur, ancien_mot_de_passe, nouveau_mot_de_passe)

        elif choix == '4':
            nom_utilisateur = input("Nom d'utilisateur à supprimer : ")
            mot_de_passe = getpass.getpass("Mot de passe de confirmation : ")
            
            if gestion.authentifier_utilisateur(nom_utilisateur, mot_de_passe):
                gestion.supprimer_utilisateur(nom_utilisateur)

        elif choix == '5':
            print("Au revoir!")
            break

        else:
            print("Choix invalide. Réessayez.")

if __name__ == "__main__":
    menu_principal()