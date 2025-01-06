# Application de Gestion de Stock & Commandes (Python)
Application bureau développée avec Python et Tkinter pour gérer stocks et commandes avec système authentification.
Fonctionnalités

Authentification

Connexion/Déconnexion
Création de compte
Modification mot de passe
Suppression compte


Gestion Stock

CRUD Produits
Recherche
Tri (normal et bulles)


Commandes

Création/Traitement commandes JSON
Vérification stocks
Distinction commandes acceptées/refusées


Sécurité

Vérification mots de passe compromis
Notifications email
Journalisation (logs)



Installation
bashCopypip install -r requirements.txt
Structure

Interface_graphique.py : Interface utilisateur Tkinter
utilisateur.py : Gestion utilisateurs/authentification
Main.py : Point d'entrée console
Notification_email.py : Système notifications email
products.csv : Base données produits
commandes_*.json : Stockage commandes

Utilisation
bashCopypython Interface_graphique.py
Technologies

Python 3.x
Tkinter
Pandas
JSON
SMTP (Gmail)

Auteur
Tim
Licence
MIT
