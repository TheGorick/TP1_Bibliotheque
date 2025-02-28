# Guillaume Pinat

from Abonne import Abonne
from Documents import Livre, BandeDessinee
from BaseDeDonnees import BaseDeDonnees

class Bibliotheque:
    """Gestion des abonnés et des documents avec SQLite"""
    def __init__(self):
        self.db = BaseDeDonnees()

    #  Ajouter un abonné
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

    #  Supprimer un abonné
    def supprimer_abonne(self, prenom, nom):
        # Récupérer l'ID de l'abonné
        self.db.cur.execute("SELECT id FROM Abonnes WHERE prenom = ? AND nom = ?", (prenom, nom))
        abonne_id = self.db.cur.fetchone()[0]  # L'ID est garanti par la liste déroulante

        # Vérifier si l'abonné a des emprunts en cours
        self.db.cur.execute("SELECT COUNT(*) FROM Emprunts WHERE abonne_id = ?", (abonne_id,))
        emprunts = self.db.cur.fetchone()[0]

        if emprunts > 0:
            message = f"Impossible de supprimer {prenom} {nom}, car il a encore {emprunts} emprunt(s) en cours."
            print(message)
            return False, message  # Retourne aussi le message pour l'affichage en pop-up

        # Supprimer l'abonné
        self.db.cur.execute("DELETE FROM Abonnes WHERE id = ?", (abonne_id,))
        self.db.conn.commit()

        message = f"L'abonné {prenom} {nom} a été supprimé avec succès."
        print(message)
        return True, message  # Retourne True + le message

    #  Afficher tous les abonnés
    def afficher_abonnes(self):
        self.db.cur.execute("SELECT id, prenom, nom FROM Abonnes")
        abonnes = self.db.cur.fetchall()

        if not abonnes:
            print("Aucun abonné enregistré.")
            return

        for id_abonne, prenom, nom in abonnes:
            print(f"ID: {id_abonne} | Prenom: {prenom} | Nom: {nom}")

    #  Ajouter un document
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

    #  Supprimer un document
    def supprimer_document(self, document_id):
        # Récupérer le titre du document avant la suppression
        self.db.cur.execute("SELECT titre FROM Documents WHERE id = ?", (document_id,))
        titre = self.db.cur.fetchone()[0]  # On récupère directement le titre

        # Supprimer les emprunts liés au document
        self.db.cur.execute("DELETE FROM Emprunts WHERE document_id = ?", (document_id,))
        self.db.conn.commit()

        # Supprimer le document de la base de données
        self.db.cur.execute("DELETE FROM Documents WHERE id = ?", (document_id,))
        self.db.conn.commit()

        message = f'Le document "{titre}" a été supprimé avec succès.'
        print(message)
        return True, message  # Retourne True + le message

    #  Afficher tous les documents
    def afficher_documents(self):
        self.db.cur.execute("SELECT id, type, titre, auteur, dessinateur FROM Documents")
        documents = self.db.cur.fetchall()

        if not documents:
            print("Aucun document enregistré.")
            return

        # Définition des largeurs de colonnes (ajout de quelques espaces pour l'alignement)
        col_widths = {"ID": 5, "Classification": 14, "Titre": 30, "Auteur": 22, "Disponibilité": 15, "Dessinateur": 22}

        # Création de l'en-tête
        header = f"| {'ID'.center(col_widths['ID'])} | {'Classification'.center(col_widths['Classification'])} | {'Titre'.center(col_widths['Titre'])} | {'Auteur'.center(col_widths['Auteur'])} | {'Disponibilité'.center(col_widths['Disponibilité'])} | {'Dessinateur'.center(col_widths['Dessinateur'])} |"
        separator = "-" * len(header)

        print(separator)
        print(header)
        print(separator)

        # Affichage des documents avec alignement parfait
        for id_doc, type_doc, titre, auteur, dessinateur in documents:
            classification = "Livre" if type_doc == "Livre" else "BD"

            if type_doc == "Livre":
                disponibilite = \
                self.db.cur.execute("SELECT COUNT(*) FROM Emprunts WHERE document_id = ?", (id_doc,)).fetchone()[0]
                disponibilite = "Non" if disponibilite > 0 else "Oui"
                row = f"| {str(id_doc).center(col_widths['ID'])} | {classification.center(col_widths['Classification'])} | {titre.center(col_widths['Titre'])} | {auteur.center(col_widths['Auteur'])} | {disponibilite.center(col_widths['Disponibilité'])} | {'-'.center(col_widths['Dessinateur'])} |"
            else:
                row = f"| {str(id_doc).center(col_widths['ID'])} | {classification.center(col_widths['Classification'])} | {titre.center(col_widths['Titre'])} | {auteur.center(col_widths['Auteur'])} | {'-'.center(col_widths['Disponibilité'])} | {dessinateur.center(col_widths['Dessinateur'])} |"

            print(row)

        print(separator)  # Ligne de fin