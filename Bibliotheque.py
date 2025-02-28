# Guillaume Pinat

from Abonne import Abonne
from Documents import Livre, BandeDessinee
from BaseDeDonnees import BaseDeDonnees

class Bibliotheque:
    """Gestion des abonnés et des documents avec SQLite"""
    def __init__(self):
        self.db = BaseDeDonnees()

    # 🔹 Ajouter un abonné
    def ajouter_abonne(self, prenom, nom):
        # Vérifier si l'abonné existe déjà dans la base de données
        self.db.cur.execute("SELECT id FROM Abonnes WHERE prenom = ? AND nom = ?", (prenom, nom))
        if self.db.cur.fetchone():  # Si un résultat est trouvé, l'abonné existe déjà
            print("Abonné déjà existant.")
            return False

        # Ajouter l'abonné s'il n'existe pas encore
        self.db.cur.execute("INSERT INTO Abonnes (prenom, nom) VALUES (?, ?)", (prenom, nom))
        self.db.conn.commit()
        print(f"Abonné {prenom} {nom} ajouté avec succès.")
        return True

    # 🔹 Supprimer un abonné
    def supprimer_abonne(self, prenom, nom):
        # Suppression directe de l'abonné sans vérification préalable
        self.db.cur.execute("DELETE FROM Abonnes WHERE prenom = ? AND nom = ?", (prenom, nom))
        self.db.conn.commit()
        print(f"Abonné {prenom} {nom} supprimé avec succès.")

    # 🔹 Afficher tous les abonnés
    def afficher_abonnes(self):
        self.db.cur.execute("SELECT prenom, nom FROM Abonnes")
        abonnes = self.db.cur.fetchall()

        if not abonnes:
            print("Aucun abonné enregistré.")
            return

        for prenom, nom in abonnes:
            print(f"{prenom} {nom}")

    # 🔹 Ajouter un document
    def ajouter_document(self, document):
        type_doc = "Livre" if isinstance(document, Livre) else "Bande Dessinee"

        # Vérifier si le document existe déjà
        self.db.cur.execute("SELECT id FROM Documents WHERE titre = ?", (document.titre,))
        if self.db.cur.fetchone():
            print(f"Document '{document.titre}' déjà existant.")
            return False

        # Ajouter le document à la base de données
        self.db.cur.execute(
            "INSERT INTO Documents (titre, auteur, type, dessinateur) VALUES (?, ?, ?, ?)",
            (document.titre, document.auteur, type_doc, getattr(document, 'dessinateur', None))
        )
        self.db.conn.commit()
        print(f"Document '{document.titre}' ajouté avec succès.")
        return True

    # 🔹 Supprimer un document
    def supprimer_document(self, titre):
        self.db.cur.execute("DELETE FROM Documents WHERE titre = ?", (titre,))
        self.db.conn.commit()
        print(f"Document '{titre}' supprimé avec succès.")

    # 🔹 Afficher tous les documents
    def afficher_documents(self):
        self.db.cur.execute("SELECT titre, auteur, type FROM Documents")
        documents = self.db.cur.fetchall()

        if not documents:
            print("Aucun document enregistré.")
            return

        for titre, auteur, type_doc in documents:
            print(f"{titre} ({type_doc}) - {auteur}")