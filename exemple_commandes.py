from Commandes import GestionCommandes

def test_commande():
    try:
        gestionnaire = GestionCommandes()
        succes, commande = gestionnaire.traiter_commande(
            client="J'aimelespatates",
            vendeur="J'aimelespatates",
            produit="patates",
            quantite=900,
            prix_unitaire=90.0
        )
        print(f"Statut: {'Acceptée' if succes else 'Refusée'}")
        print(f"ID Commande: {commande['id']}")
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    test_commande()