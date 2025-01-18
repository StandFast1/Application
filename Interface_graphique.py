import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utilisateur import Utilisateur
import pandas as pd
import os
import logging
import csv
from Notification_email import NotificationEmail
import json
from Commandes import GestionCommandes



logging.basicConfig(
    filename='application.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')


class AppInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Application Python by Tim")
        self.geometry("900x700")


        self.gestion_utilisateurs = Utilisateur()
        self.utilisateur_connecte = None
        self.notification = NotificationEmail()

        

        self.creer_interface_connexion()

    def creer_interface_connexion(self):
        
        self.frame_connexion = ttk.Frame(self)
        self.frame_connexion.pack(padx=30, pady=20)

    
        ttk.Label(self.frame_connexion, text="Nom d'utilisateur :").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.frame_connexion)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_connexion, text="Mot de passe :").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.frame_connexion, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.frame_connexion, text="Se connecter", command=self.connexion).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.frame_connexion, text="Créer un compte", command=self.afficher_creation_compte).grid(row=3, column=0, columnspan=2)
        ttk.Button(self.frame_connexion, text="Changer de mot de passe", command=self.inferface_changer_mot_de_passe).grid(row=4, column=0, columnspan=2, pady=12)
        ttk.Button(self.frame_connexion, text="Supprimer un compte", command=self.inferface_supression_utilisateur).grid(row=5, column=0, columnspan=2, pady=10)
        

    def inferface_changer_mot_de_passe(self):

        fenetre_new_password = tk.Toplevel(self)
        fenetre_new_password.title("Changement de mot de passe")
        fenetre_new_password.geometry("500x500")

        frame = ttk.Frame(fenetre_new_password, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Identifiant :").pack(pady=5)
        username_entry = ttk.Entry(frame)
        username_entry.pack(pady=5)

        ttk.Label(frame, text="Ancien Password :").pack(pady=5)
        A_password_entry = ttk.Entry(frame)
        A_password_entry.pack(pady=5)

        ttk.Label(frame, text="Nouveau Password :").pack(pady=5)
        password_entry = ttk.Entry(frame)
        password_entry.pack(pady=5)

        ttk.Label(frame, text="Email :").pack(pady=5)  
        email_entry = ttk.Entry(frame)
        email_entry.pack(pady=5)

        frame_boutons = ttk.Frame(frame)
        frame_boutons.pack(pady=20)

        def changer_mot_de_passe():
            nom = username_entry.get()
            ancien_mdp = A_password_entry.get()
            nouveau_mdp = password_entry.get()
            email = email_entry.get()

            if self.gestion_utilisateurs.changement_mdp(nom, ancien_mdp, nouveau_mdp):
                messagebox.showinfo("Succès", "Mot de passe modifié avec succès")
                details_confirmation = "Votre mot de passe a été modifié avec succès"
                self.notification.envoyer_alerte(email, details_confirmation)
                fenetre_new_password.destroy()
            else:
                messagebox.showerror("Erreur", "Échec du changement de mot de passe")

        ttk.Button(frame_boutons, text="Confirmer", command=changer_mot_de_passe).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Annuler", command=fenetre_new_password.destroy).pack(side=tk.LEFT, padx=5)

        # Verification Identifiant et Password
        # Changer le fichier utilisateur.csv pour changer le mot de passe

    def inferface_supression_utilisateur(self):

        fenetre_supression_utilisateur = tk.Toplevel(self)
        fenetre_supression_utilisateur.title("Suppression Utilisateur")
        fenetre_supression_utilisateur.geometry("500x500")

        frame = ttk.Frame(fenetre_supression_utilisateur, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Identifiant :").pack(pady=5)
        username_entry = ttk.Entry(frame)
        username_entry.pack(pady=5)

        ttk.Label(frame, text="Password :").pack(pady=5)
        password_entry = ttk.Entry(frame)
        password_entry.pack(pady=5)

        frame_boutons = ttk.Frame(frame)
        frame_boutons.pack(pady=20)

        def supression_utilisateur():
            nom = username_entry.get()
            mdp = password_entry.get()

            if self.gestion_utilisateurs.connexion(nom, mdp):  
                if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer votre compte?"):
                    if self.gestion_utilisateurs.sup_utilisateur(nom):
                        messagebox.showinfo("Succès", "Compte supprimé avec succès")
                        fenetre_supression_utilisateur.destroy()
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects")

        ttk.Button(frame_boutons, text="Confirmer", command=supression_utilisateur).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Annuler", command=fenetre_supression_utilisateur.destroy).pack(side=tk.LEFT, padx=5)

    



    
        
    def connexion(self):
        nom = self.username_entry.get()
        mdp = self.password_entry.get()
        role = self.gestion_utilisateurs.connexion(nom, mdp)

        if role:
            self.utilisateur_connecte = nom
            messagebox.showinfo("Succès", f"Connexion réussie en tant que {role}")
            logging.info(f'Connexion reussite : {nom}')
            self.afficher_interface_produits()
        else:
            logging.info(f'Connexion echoue : {nom}')
            messagebox.showerror("Erreur", "Identifiants incorrects")

    def afficher_interface_produits(self):
        
        self.frame_connexion.pack_forget()

        # interface principale
        self.frame_principal = ttk.Frame(self)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # recherche
        frame_recherche = ttk.Frame(self.frame_principal)
        frame_recherche.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_recherche, text="Rechercher :").pack(side=tk.LEFT, padx=5)
        self.recherche_entry = ttk.Entry(frame_recherche)
        self.recherche_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
        frame_boutons = ttk.Frame(frame_recherche)
        frame_boutons.pack(side=tk.RIGHT)
    
        ttk.Button(frame_boutons, text="Rechercher", command=self.rechercher_produits).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Réinitialiser", command=self.charger_produits).pack(side=tk.LEFT, padx=5)  
        ttk.Button(frame_boutons, text="Ajouter un produit", command=self.afficher_ajout_produit).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Supprimer un produit", command=self.supprimer_produit_selectionne).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Statistiques", command=self.afficher_statistiques).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Gestion Commandes", command=self.afficher_gestion_commandes).pack(side=tk.LEFT, padx=5)

        
        self.tree = ttk.Treeview(self.frame_principal, columns=('Nom', 'Prix', 'Quantité', 'Disponible'), show='headings')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Prix', text='Prix')
        self.tree.heading('Quantité', text='Quantité')
        self.tree.heading('Disponible', text='Disponible')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        
        ttk.Button(self.frame_principal, text="Déconnexion", command=self.deconnexion).pack(pady=10)

       
        self.charger_produits()


    def supprimer_produit_selectionne(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit à supprimer")
            return
    
        item = self.tree.item(selection[0])
        nom_produit = item['values'][0]  
    
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer le produit '{nom_produit}' ?"):
            try:
                df = pd.read_csv('produits.csv')
               
                df = df.drop(df[(df['nom'] == nom_produit) & (df['proprietaire'] == self.utilisateur_connecte)].index)
                df.to_csv('produits.csv', index=False)
            
                messagebox.showinfo("Succès", "Produit supprimé avec succès")
                logging.info(f'Produit supprimé : {nom_produit} par {self.utilisateur_connecte}')
                self.charger_produits()  
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit : {e}")
                logging.error(f'Erreur de suppression : {nom_produit} par {self.utilisateur_connecte} - {e}')


    def afficher_ajout_produit(self):
        fenetre_ajout = tk.Toplevel(self)
        fenetre_ajout.title("Ajouter un produit")
        fenetre_ajout.geometry("400x400")

        frame = ttk.Frame(fenetre_ajout, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

    
        ttk.Label(frame, text="Nom du produit :").pack(pady=5)
        nom_entry = ttk.Entry(frame)
        nom_entry.pack(pady=5)

        ttk.Label(frame, text="Prix :").pack(pady=5)
        prix_entry = ttk.Entry(frame)
        prix_entry.pack(pady=5)

        ttk.Label(frame, text="Quantité :").pack(pady=5)
        quantite_entry = ttk.Entry(frame)
        quantite_entry.pack(pady=5)

        ttk.Label(frame, text="Disponible :").pack(pady=5)
        disponible_var = tk.BooleanVar()
        ttk.Checkbutton(frame, variable=disponible_var).pack(pady=5)

        frame_boutons = ttk.Frame(frame)
        frame_boutons.pack(pady=20)

        def verifier_donnees():
            try:
                nom = nom_entry.get()
                prix = float(prix_entry.get())
                quantite = int(quantite_entry.get())
                disponible = disponible_var.get()

                if not nom:
                    messagebox.showerror("Erreur", "Le nom est requis")
                    return

                messagebox.showinfo("Verification", f"""
                Détails du produit :
                Nom: {nom}
                Prix: {prix}€
                Quantité: {quantite}
                Disponible: {'Oui' if disponible else 'Non'}
                """)

            except ValueError:
                messagebox.showerror("Erreur", "Prix et quantité doivent être des nombres")
    
        def ajouter_produit():
            try:
                nom = nom_entry.get()
                prix = float(prix_entry.get())
                quantite = int(quantite_entry.get())
                disponible = disponible_var.get()

                if not nom:
                    messagebox.showerror("Erreur", "Le nom est requis")
                    return

                if messagebox.askyesno("Confirmation", "Voulez-vous vraiment ajouter ce produit ?"):
                    nouveau_produit = pd.DataFrame({
                        'nom': [nom],
                        'prix': [prix],
                        'quantite': [quantite],
                        'disponible': [disponible],
                        'proprietaire': [self.utilisateur_connecte]
                    })

                    if os.path.exists('produits.csv'):
                        df = pd.read_csv('produits.csv')
                        df = pd.concat([df, nouveau_produit])
                    else:
                        df = nouveau_produit

                    df.to_csv('produits.csv', index=False)
                    messagebox.showinfo("Succès", "Produit ajouté avec succès!")
                    self.charger_produits()
                    fenetre_ajout.destroy()

            except ValueError:
                messagebox.showerror("Erreur", "Prix et quantité doivent être des nombres")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit : {e}")

    # Boutons
        ttk.Button(frame_boutons, text="Vérifier", command=verifier_donnees).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Ajouter", command=ajouter_produit).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Annuler", command=fenetre_ajout.destroy).pack(side=tk.LEFT, padx=5)

    
    def charger_produits(self):
        try:
            df = pd.read_csv('produits.csv')
            df = df[df['proprietaire'] == self.utilisateur_connecte]
            self.tree.delete(*self.tree.get_children())

            for _, row in df.iterrows():
                self.tree.insert('', tk.END, values=(
                    row['nom'],
                    f"{row['prix']}€",
                    row['quantite'],
                    'Oui' if row['disponible'] else 'Non'
                ))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des produits : {e}")

    def rechercher_produits(self):
        recherche = self.recherche_entry.get().lower()
        self.tree.delete(*self.tree.get_children())
        
        try:
            df = pd.read_csv('produits.csv')
            df_filtree = df[df['nom'].str.lower().str.contains(recherche)]
            df = df[df['proprietaire'] == self.utilisateur_connecte]
            df_filtree = df[df['nom'].str.lower().str.contains(recherche)]
            
            for _, row in df_filtree.iterrows():
                self.tree.insert('', tk.END, values=(
                    row['nom'],
                    f"{row['prix']}€",
                    row['quantite'],
                    'Oui' if row['disponible'] else 'Non'
                ))
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")

    def deconnexion(self):
        self.utilisateur_connecte = None
        self.frame_principal.destroy()
        self.creer_interface_connexion()

    def afficher_creation_compte(self):
        fenetre_creation = tk.Toplevel(self)
        fenetre_creation.title("Création de compte")
        fenetre_creation.geometry("400x300")

        frame = ttk.Frame(fenetre_creation, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Champs
        ttk.Label(frame, text="Nom d'utilisateur :").pack(pady=5)
        username_entry = ttk.Entry(frame)
        username_entry.pack(pady=5)

        ttk.Label(frame, text="Mot de passe :").pack(pady=5)
        password_entry = ttk.Entry(frame, show="*")
        password_entry.pack(pady=5)

        ttk.Label(frame, text="Email :").pack(pady=5)
        email_entry = ttk.Entry(frame)
        email_entry.pack(pady=5)

        def creer_compte():
            nom = username_entry.get()
            mdp = password_entry.get()
            email = email_entry.get()

            if not nom or not mdp or not email:
                messagebox.showerror("Erreur", "Tous les champs sont requis")
                return

            if self.gestion_utilisateurs.verif_mot_de_passe_compromis(mdp):
                logging.warning(f'Mot de passe compromis : {username_entry}')
                details_compromis = "Votre mot de passe a été détecté comme potentiellement compromis lors de la création de compte."
                self.notification.envoyer_alerte(email, details_compromis)
                messagebox.showwarning("Attention", "Ce mot de passe est compromis!")
                return

            if self.gestion_utilisateurs.nouveau_utilisateur(nom, mdp, email, role='utilisateur'):
                logging.info(f'Nouveau compte : {username_entry}')
                messagebox.showinfo("Succès", "Compte créé avec succès!")
                fenetre_creation.destroy()
            else:
                logging.error(f'Connexion reussite : {username_entry}')
                messagebox.showerror("Erreur", "Erreur lors de la création du compte")

        ttk.Button(frame, text="Créer le compte", command=creer_compte).pack(pady=20)
    
    def afficher_statistiques(self):
        from stats import Statistiques
        stats = Statistiques()
        stats.generer_graphiques()
    
        fenetre_stats = tk.Toplevel(self)
        fenetre_stats.title("Statistiques")
    
        img = tk.PhotoImage(file='statistiques.png')
        label = tk.Label(fenetre_stats, image=img)
        label.image = img
        label.pack()
    
    def afficher_gestion_commandes(self):
        from Commandes import GestionCommandes
    
        fenetre_commandes = tk.Toplevel(self)
        fenetre_commandes.title("Gestion des Commandes")
        fenetre_commandes.geometry("600x600")

        frame = ttk.Frame(fenetre_commandes, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        
        ttk.Label(frame, text="Client :").pack(pady=5)
        client_entry = ttk.Entry(frame)
        client_entry.pack(pady=5)

        ttk.Label(frame, text="Produit :").pack(pady=5)
        produit_entry = ttk.Entry(frame)
        produit_entry.pack(pady=5)

        ttk.Label(frame, text="Quantité :").pack(pady=5)
        quantite_entry = ttk.Entry(frame)
        quantite_entry.pack(pady=5)

        # afficher les commandes
        tree_commandes = ttk.Treeview(frame, columns=('ID', 'Date', 'Client', 'Produit', 'Quantité', 'Total'), show='headings')
        tree_commandes.heading('ID', text='ID')
        tree_commandes.heading('Date', text='Date')
        tree_commandes.heading('Client', text='Client')
        tree_commandes.heading('Produit', text='Produit')
        tree_commandes.heading('Quantité', text='Quantité')
        tree_commandes.heading('Total', text='Total')
        tree_commandes.pack(fill=tk.BOTH, expand=True, pady=10)

        def traiter_nouvelle_commande():
            try:
                gestionnaire = GestionCommandes()
                client = client_entry.get()
                produit = produit_entry.get()
                quantite = int(quantite_entry.get())
            
                # Récupérer le prix du produit depuis le CSV
                df = pd.read_csv('produits.csv')
                produit_info = df[df['nom'] == produit]
                if produit_info.empty:
                    messagebox.showerror("Erreur", "Produit non trouvé")
                    return
                
                prix_unitaire = float(produit_info['prix'].iloc[0])
            
                succes, commande = gestionnaire.traiter_commande(
                    client=client,
                    vendeur=self.utilisateur_connecte,
                    produit=produit,
                    quantite=quantite,
                    prix_unitaire=prix_unitaire
                )
            
                if succes:
                    messagebox.showinfo("Succès", "Commande traitée avec succès!")
                    charger_commandes()  # Rafraîchir l'affichage
                    # Envoyer notification par email si configuré
                    if hasattr(self, 'notification'):
                        self.notification.envoyer_alerte(
                            client_entry.get(),
                            f"Votre commande {commande['id']} a été traitée avec succès!"
                        )
                else:
                    messagebox.showerror("Erreur", "Impossible de traiter la commande (stock insuffisant)")
                
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez vérifier les données saisies")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du traitement de la commande: {str(e)}")

        def charger_commandes():
            tree_commandes.delete(*tree_commandes.get_children())
            try:
                with open('commandes_acceptees.json', 'r') as f:
                    commandes = json.load(f)
                    for cmd in commandes:
                        if cmd['vendeur'] == self.utilisateur_connecte:
                            tree_commandes.insert('', tk.END, values=(
                                cmd['id'],
                                cmd['date'],
                                cmd['client'],
                                cmd['produit'],
                                cmd['quantite'],
                                f"{cmd['prix_total']}€"
                            ))
            except Exception as e:
                logging.error(f"Erreur chargement commandes: {str(e)}")

        # Boutons de contrôle
        frame_boutons = ttk.Frame(frame)
        frame_boutons.pack(pady=10)
    
        ttk.Button(frame_boutons, text="Traiter Commande", command=traiter_nouvelle_commande).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Rafraîchir", command=charger_commandes).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_boutons, text="Fermer", command=fenetre_commandes.destroy).pack(side=tk.LEFT, padx=5)

        # Charger les commandes existantes
        charger_commandes()
    

if __name__ == "__main__":
    app = AppInterface()
    app.mainloop()