#!/usr/bin/env python3
"""Script pour mettre à jour le mot de passe admin"""

from app import create_app
from app.models.user import User
from app import db

app = create_app()

with app.app_context():
    # Trouver l'utilisateur admin
    admin_user = User.query.filter_by(email='admin@hbnb.io').first()
    
    if admin_user:
        print(f"Utilisateur trouvé: {admin_user.email}")
        
        # Mettre à jour le mot de passe avec "admin123"
        new_hash = "$2b$12$nIZw6ve3r5xGDXzRdtjzFuqABEK4pBpJ65ry3IvEWoWnNG86Asq4m"
        admin_user.password = new_hash
        
        try:
            db.session.commit()
            print("✅ Mot de passe admin mis à jour avec succès!")
            print("Nouveau mot de passe: admin123")
            
            # Vérifier que ça fonctionne
            if admin_user.verify_password("admin123"):
                print("✅ Vérification réussie: 'admin123' fonctionne!")
            else:
                print("❌ Erreur: la vérification a échoué")
                
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour: {e}")
            db.session.rollback()
    else:
        print("❌ Utilisateur admin@hbnb.io non trouvé")
        print("Création d'un nouvel utilisateur admin...")
        
        # Créer un nouvel utilisateur admin
        admin_hash = "$2b$12$nIZw6ve3r5xGDXzRdtjzFuqABEK4pBpJ65ry3IvEWoWnNG86Asq4m"
        new_admin = User(
            email="admin@hbnb.io",
            first_name="Admin",
            last_name="HBnB",
            password=admin_hash,
            is_admin=True
        )
        
        try:
            db.session.add(new_admin)
            db.session.commit()
            print("✅ Nouvel utilisateur admin créé!")
            print("Email: admin@hbnb.io")
            print("Mot de passe: admin123")
        except Exception as e:
            print(f"❌ Erreur lors de la création: {e}")
            db.session.rollback()