import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
import logging

logging.basicConfig(
    filename='application.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')

class NotificationEmail:
    def __init__(self):
        self.email_expediteur = "applicationpython129@gmail.com"
        self.mot_de_passe = "dadm qqmn gwmg gsiq"
        self.serveur_smtp = "smtp.gmail.com"
        self.port_smtp = 587

    def envoyer_alerte(self, email_utilisateur, details_compromis):
        message = MIMEMultipart()
        message["From"] = self.email_expediteur.encode('utf-8').decode('ascii', 'ignore')
        message["To"] = email_utilisateur.encode('utf-8').decode('ascii', 'ignore')
        message["Subject"] = "Alerte de sécurite - Compromission detectee"

       
        contenu = f"""
        ALERTE DE SECURITE

        Une compromission a ete detectee pour votre compte :
        {details_compromis}

        Actions recommandees :
        1. Changez immediatement votre mot de passe
        2. Activez l'authentification à deux facteurs si disponible
        3. Ne réutilisez pas ce mot de passe sur d'autres sites

        Cordialement,
        Votre systeme de securite
        """.encode('utf-8').decode('ascii', 'ignore')

        message.attach(MIMEText(contenu, "plain", "utf-8"))

        try:
            with smtplib.SMTP(self.serveur_smtp, self.port_smtp) as serveur:
                logging.info(f'email envoye : {email_utilisateur}')
                serveur.starttls()
                serveur.login(self.email_expediteur, self.mot_de_passe)
                serveur.send_message(message)
            return True
        except Exception as e:
            print(f"Erreur d'envoi d'email: {e}")
            return False

      