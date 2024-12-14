import hashlib
import os
import base64

# 1. Hachage simple avec SHA-256
def hachage_simple(mot_de_passe):
    """Hachage basique d'un mot de passe avec SHA-256"""
    # Encode la chaîne en bytes et applique le hachage
    return hashlib.sha256(mot_de_passe.encode()).hexdigest()

# 2. Hachage avec sel
def hachage_avec_sel(mot_de_passe):
    """Hachage d'un mot de passe avec un sel aléatoire"""
    # Génère un sel aléatoire
    sel = os.urandom(16)  # 16 bytes de données aléatoires
    
    # Combine le sel et le mot de passe
    mot_de_passe_sale = sel + mot_de_passe.encode()
    
    # Applique le hachage
    hachage = hashlib.sha256(mot_de_passe_sale).hexdigest()
    
    # Encode le sel en base64 pour le stockage
    sel_base64 = base64.b64encode(sel).decode()
    
    # Retourne le sel et le hachage séparés par $
    return f"{sel_base64}${hachage}"

# 3. Vérification d'un mot de passe avec sel
def verifier_mot_de_passe(mot_de_passe, hachage_stocke):
    """Vérifie si un mot de passe correspond au hachage stocké"""
    # Sépare le sel et le hachage
    sel_base64, hachage = hachage_stocke.split('$')
    
    # Décode le sel
    sel = base64.b64decode(sel_base64)
    
    # Recalcule le hachage avec le même sel
    mot_de_passe_sale = sel + mot_de_passe.encode()
    nouveau_hachage = hashlib.sha256(mot_de_passe_sale).hexdigest()
    
    # Compare les hachages
    return hachage == nouveau_hachage

# 4. Exemple d'utilisation avec plusieurs algorithmes
def demo_algorithmes():
    """Démontre différents algorithmes de hachage disponibles"""
    mot_de_passe = "MonMotDePasse123"
    
    # SHA-256
    sha256 = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    print(f"SHA-256: {sha256}")
    
    # SHA-512
    sha512 = hashlib.sha512(mot_de_passe.encode()).hexdigest()
    print(f"SHA-512: {sha512}")
    
    # MD5 (non recommandé pour la sécurité)
    md5 = hashlib.md5(mot_de_passe.encode()).hexdigest()
    print(f"MD5: {md5}")

# Exemple d'utilisation
if __name__ == "__main__":
    mot_de_passe = "MonMotDePasse123"
    
    # 1. Hachage simple
    hachage = hachage_simple(mot_de_passe)
    print(f"Hachage simple: {hachage}")
    
    # 2. Hachage avec sel
    hachage_sel = hachage_avec_sel(mot_de_passe)
    print(f"Hachage avec sel: {hachage_sel}")
    
    # 3. Vérification
    est_valide = verifier_mot_de_passe(mot_de_passe, hachage_sel)
    print(f"Vérification du mot de passe: {est_valide}")
    
    # 4. Différents algorithmes
    demo_algorithmes()