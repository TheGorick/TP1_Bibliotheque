class Emprunts:
    """Gestion des emprunts avec SQLite"""

    def __init__(self, bibliotheque):
        self.bibliotheque = bibliotheque
        self.db = bibliotheque.db

    # 🔹 Emprunter un document
    def emprunter_document(self, document_id, abonne_id):
        # Récupérer le titre du document
        self.db.cur.execute("SELECT titre FROM Documents WHERE id = ?", (document_id,))
        document = self.db.cur.fetchone()

        if not document:
            print(f"Document avec ID '{document_id}' non trouvé.")
            return False

        # Vérifier si le document est déjà emprunté
        self.db.cur.execute("SELECT id FROM Emprunts WHERE document_id = ?", (document_id,))
        if self.db.cur.fetchone():
            print(f"Le document '{document[0]}' est déjà emprunté.")
            return False

        # Récupérer le prénom et le nom de l'abonné
        self.db.cur.execute("SELECT prenom, nom FROM Abonnes WHERE id = ?", (abonne_id,))
        abonne = self.db.cur.fetchone()

        if not abonne:
            print(f"Abonné avec ID '{abonne_id}' non trouvé.")
            return False

        prenom, nom = abonne  # Extraction des données du tuple

        # Ajouter l'emprunt dans la base de données
        self.db.cur.execute("INSERT INTO Emprunts (document_id, abonne_id) VALUES (?, ?)", (document_id, abonne_id))
        self.db.conn.commit()

        print(f"L'abonné {prenom} {nom} a emprunté '{document[0]}'.")
        return True

    # 🔹 Retourner un document
    def retourner_document(self, titre):
        self.db.cur.execute("DELETE FROM Emprunts WHERE document_id IN (SELECT id FROM Documents WHERE titre = ?)",
                            (titre,))
        self.db.conn.commit()
        print(f"Le document '{titre}' a été retourné.")

    # 🔹 Afficher tous les emprunts
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