import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utilisateur import Utilisateur
import pandas as pd
import os

class AppInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestion de Produits")
        self.geometry("800x600")
        
        # Initialisation des objets
        self.gestion_utilisateurs = Utilisateur()
        self.utilisateur_connecte = None

        # Création de l'interface de connexion
        self.creer_interface_connexion()

    def creer_interface_connexion(self):
        # Frame de connexion
        self.frame_connexion = ttk.Frame(self)
        self.frame_connexion.pack(padx=20, pady=20)

        # Champs de connexion
        ttk.Label(self.frame_connexion, text="Nom d'utilisateur :").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.frame_connexion)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_connexion, text="Mot de passe :").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.frame_connexion, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Boutons
        ttk.Button(self.frame_connexion, text="Se connecter", command=self.connexion).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.frame_connexion, text="Créer un compte", command=self.afficher_creation_compte).grid(row=3, column=0, columnspan=2)

    def connexion(self):
        nom = self.username_entry.get()
        mdp = self.password_entry.get()
        role = self.gestion_utilisateurs.connexion(nom, mdp)

        if role:
            self.utilisateur_connecte = nom
            messagebox.showinfo("Succès", f"Connexion réussie en tant que {role}")
            self.afficher_interface_produits()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    def afficher_interface_produits(self):
        # Cacher l'interface de connexion
        self.frame_connexion.pack_forget()

        # Créer l'interface principale
        self.frame_principal = ttk.Frame(self)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Barre de recherche
        frame_recherche = ttk.Frame(self.frame_principal)
        frame_recherche.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_recherche, text="Rechercher :").pack(side=tk.LEFT, padx=5)
        self.recherche_entry = ttk.Entry(frame_recherche)
        self.recherche_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(frame_recherche, text="Rechercher", command=self.rechercher_produits).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_recherche, text="Ajouter un produit", command=self.afficher_ajout_produit).pack(side=tk.LEFT, padx=5)

        # Liste des produits
        self.tree = ttk.Treeview(self.frame_principal, columns=('Nom', 'Prix', 'Quantité', 'Disponible'), show='headings')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Prix', text='Prix')
        self.tree.heading('Quantité', text='Quantité')
        self.tree.heading('Disponible', text='Disponible')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Bouton déconnexion
        ttk.Button(self.frame_principal, text="Déconnexion", command=self.deconnexion).pack(pady=10)

        # Charger les produits
        self.charger_produits()

    def afficher_ajout_produit(self):
        fenetre_ajout = tk.Toplevel(self)
        fenetre_ajout.title("Ajouter un produit")
        fenetre_ajout.geometry("400x300")

        frame = ttk.Frame(fenetre_ajout, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Champs
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

        def ajouter_produit():
            try:
                nom = nom_entry.get()
                prix = float(prix_entry.get())
                quantite = int(quantite_entry.get())
                disponible = disponible_var.get()

                if not nom:
                    messagebox.showerror("Erreur", "Le nom est requis")
                    return

                nouveau_produit = pd.DataFrame({
                    'nom': [nom],
                    'prix': [prix],
                    'quantite': [quantite],
                    'disponible': [disponible]
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

        ttk.Button(frame, text="Ajouter", command=ajouter_produit).pack(pady=20)

    def charger_produits(self):
        try:
            df = pd.read_csv('produits.csv')
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
                messagebox.showwarning("Attention", "Ce mot de passe est compromis!")
                return

            if self.gestion_utilisateurs.nouveau_utilisateur(nom, mdp, email):
                messagebox.showinfo("Succès", "Compte créé avec succès!")
                fenetre_creation.destroy()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la création du compte")

        ttk.Button(frame, text="Créer le compte", command=creer_compte).pack(pady=20)

if __name__ == "__main__":
    app = AppInterface()
    app.mainloop()