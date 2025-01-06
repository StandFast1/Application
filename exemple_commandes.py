from Commandes import GestionCommandes

def test_commande():
    try:
        gestionnaire = GestionCommandes()
        
        # Tester une commande
        succes, commande = gestionnaire.traiter_commande(
            client="Test Client",
            vendeur="Test Vendeur", 
            produit="Ordinateur",  # Assurez-vous que ce produit existe dans produits.csv
            quantite=1,
            prix_unitaire=799.99
        )
        
        print(f"Statut: {'Acceptée' if succes else 'Refusée'}")
        print(f"ID Commande: {commande['id']}")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    test_commande()