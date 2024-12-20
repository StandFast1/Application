from Notification_email import NotificationEmail

def test_email():
    notif = NotificationEmail()
    result = notif.envoyer_alerte(
        "timote7464@gmail.com",
        "Test de l'envoi d'email"
    )
    print(f"Résultat de l'envoi : {result}")

test_email()