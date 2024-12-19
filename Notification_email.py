import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart


class NotificationEmail:
    def __init__(self):
        self.email_expediteur = "votre_email@gmail.com"
        self.mot_de_passe = "votre_mot_de_passe_app"
        self.serveur_smtp = "smtp.gmail.com"
        self.port_smtp = 587

    def envoyer_alerte(self, email_utilisateur, details_compromis):
        message = MIMEMultipart()
        message["From"] = self.email_expediteur
        message["To"] = email_utilisateur
        message["Subject"] = "Alerte de sécurité - Compromission détectée"

        contenu = f"""
        ALERTE DE SÉCURITÉ

        Une compromission a été détectée pour votre compte :
        {details_compromis}

        Actions recommandées :
        1. Changez immédiatement votre mot de passe
        2. Activez l'authentification à deux facteurs si disponible
        3. Ne réutilisez pas ce mot de passe sur d'autres sites

        Cordialement,
        Votre système de sécurité
        """
        message.attach(MIMEText(contenu, "plain"))

        try:
            with smtplib.SMTP(self.serveur_smtp, self.port_smtp) as serveur:
                serveur.starttls()
                serveur.login(self.email_expediteur, self.mot_de_passe)
                serveur.send_message(message)
            return True
        
        except Exception as e:
            print(f"Erreur d'envoi d'email: {e}")
            return False