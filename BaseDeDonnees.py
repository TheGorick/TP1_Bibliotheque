#Guillaume Pinat

import sqlite3

class BaseDeDonnees:
    def __init__(self, nom_db="bibliotheque.db"):
        self.conn = sqlite3.connect(nom_db)
        self.cur = self.conn.cursor()
        self.creer_tables()

    def creer_tables(self):
        # Création des tables pour abonnés, documents et emprunts
        self.cur.executescript("""
        CREATE TABLE IF NOT EXISTS Abonnes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom TEXT NOT NULL,
            nom TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            type TEXT NOT NULL,  -- "Livre" ou "Bande Dessinee"
            dessinateur TEXT
        );

        CREATE TABLE IF NOT EXISTS Emprunts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            abonne_id INTEGER NOT NULL,
            FOREIGN KEY (document_id) REFERENCES Documents(id),
            FOREIGN KEY (abonne_id) REFERENCES Abonnes(id)
        );
        """)

        self.conn.commit()

    def fermer_connexion(self):
        self.conn.close()


if __name__ == "__main__":
    db = BaseDeDonnees()  # Initialise la base de données
    print("Connexion à SQLite réussie et tables créées.")
    db.fermer_connexion()  # Ferme la connexion