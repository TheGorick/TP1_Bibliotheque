#Guillaume Pinat

class Emprunts:
    """Gestion des emprunts avec SQLite"""

    def __init__(self, bibliotheque):
        self.bibliotheque = bibliotheque
        self.db = bibliotheque.db

    # Emprunter un document
    def emprunter_document(self, document_id, abonne_id):
        # Vérifier si le document est disponible
        self.db.cur.execute("SELECT titre FROM Documents WHERE id = ?", (document_id,))
        document = self.db.cur.fetchone()

        if not document:
            message = "Erreur : Document introuvable."
            print(message)
            return False, message

        titre = document[0]

        # Vérifier si le document est déjà emprunté
        self.db.cur.execute("SELECT COUNT(*) FROM Emprunts WHERE document_id = ?", (document_id,))
        emprunte = self.db.cur.fetchone()[0]

        if emprunte > 0:
            message = f"Le document \"{titre}\" est déjà emprunté."
            print(message)
            return False, message

        # Vérifier si l'abonné existe
        self.db.cur.execute("SELECT prenom, nom FROM Abonnes WHERE id = ?", (abonne_id,))
        abonne = self.db.cur.fetchone()

        if not abonne:
            message = "Erreur : Abonné introuvable."
            print(message)
            return False, message

        prenom, nom = abonne

        # Enregistrer l'emprunt
        self.db.cur.execute("INSERT INTO Emprunts (document_id, abonne_id) VALUES (?, ?)", (document_id, abonne_id))
        self.db.conn.commit()

        message = f"{prenom} {nom} a emprunté \"{titre}\" avec succès."
        print(message)
        return True, message

    # Retourner un document
    def retourner_document(self, document_id):
        # Vérifier si le document existe
        self.db.cur.execute("SELECT titre FROM Documents WHERE id = ?", (document_id,))
        document = self.db.cur.fetchone()

        if not document:
            message = "Erreur : Document introuvable."
            print(message)
            return False, message

        titre = document[0]

        # Vérifier si le document est bien emprunté
        self.db.cur.execute("SELECT abonne_id FROM Emprunts WHERE document_id = ?", (document_id,))
        emprunt = self.db.cur.fetchone()

        if not emprunt:
            message = f"Le document \"{titre}\" n'est pas emprunté."
            print(message)
            return False, message

        abonne_id = emprunt[0]

        # Vérifier qui l'a emprunté
        self.db.cur.execute("SELECT prenom, nom FROM Abonnes WHERE id = ?", (abonne_id,))
        abonne = self.db.cur.fetchone()

        if not abonne:
            message = "Erreur : Abonné introuvable."
            print(message)
            return False, message

        prenom, nom = abonne

        # Supprimer l'emprunt
        self.db.cur.execute("DELETE FROM Emprunts WHERE document_id = ?", (document_id,))
        self.db.conn.commit()

        message = f"{prenom} {nom} a retourné \"{titre}\" avec succès."
        print(message)
        return True, message

    # Afficher tous les emprunts
    def afficher_emprunts(self):
        self.db.cur.execute("""
             SELECT Documents.titre, Abonnes.prenom, Abonnes.nom
             FROM Emprunts
             JOIN Documents ON Emprunts.document_id = Documents.id
             JOIN Abonnes ON Emprunts.abonne_id = Abonnes.id
         """)
        emprunts = self.db.cur.fetchall()
        if not emprunts:
            print("Aucun document emprunté.")
        else:
            for titre, prenom, nom in emprunts:
                print(f"Document: {titre}, Emprunté par: {prenom} {nom}")