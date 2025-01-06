
from Commandes import GestionCommandes

gestionnaire = GestionCommandes()
succes, commande = gestionnaire.traiter_commande(
    client="John Doe",
    vendeur="Tim",
    produit="Ordinateur",
    quantite=1,
    prix_unitaire=799.99
)

print("Commande acceptée" if succes else "Commande refusée")
print(f"ID Commande: {commande['id']}")