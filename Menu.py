# Guillaume Pinat

from Bibliotheque import Bibliotheque
from Documents import Livre, BandeDessinee
from Emprunts import Emprunts

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QInputDialog, QMessageBox
from functools import partial

class Menu(QWidget):
    """Classe qui créer un menu et gère les demandes des utilisateurs"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu")
        self.setGeometry(100, 100, 300, 400)

        self.bibliotheque = Bibliotheque()  # Initialisation de bibliotheque
        self.emprunts = Emprunts(self.bibliotheque)  # Initialisation d'emprunts après bibliotheque

        layout = QVBoxLayout()

        # Liste des boutons de l'interface
        self.boutons = [
            QPushButton("1 - Ajouter un abonné"),
            QPushButton("2 - Supprimer un abonné"),
            QPushButton("3 - Afficher tous les abonnés"),
            QPushButton("4 - Ajouter un document"),
            QPushButton("5 - Supprimer un document"),
            QPushButton("6 - Afficher tous les documents"),
            QPushButton("7 - Emprunt"),
            QPushButton("8 - Retour"),
            QPushButton("9 - Afficher tous les emprunts"),
            QPushButton("Q - Quitter")
        ]

        # Ajoute les boutons au layout et connecte chaque bouton à la méthode active_choix
        for i, bouton in enumerate(self.boutons):
            layout.addWidget(bouton)
            bouton.clicked.connect(partial(self.active_choix, i + 1))  # Utilisation de partial pour ajouter l'index comme argument

        # Champ de saisie pour permettre à l'utilisateur d'entrer un chiffre ou "Q/q" pour quitter
        self.saisie = QLineEdit()
        self.saisie.setPlaceholderText("Entrez un chiffre (1-9) ou Q/q pour quitter")
        self.saisie.returnPressed.connect(self.cleanup)  # Connexion de la touche "Enter" au traitement de la saisie
        layout.addWidget(self.saisie)

        self.setLayout(layout)

    def afficher_message(self, message, titre="Message"):
        # Affiche un message via une boîte de dialogue
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle(titre)
        msg.exec()

    def cleanup(self):
        # Récupère le texte de la saisie de l'utilisateur et gère l'entrée
        text = self.saisie.text().strip()
        self.saisie.clear()
        if text.isdigit():  # Si l'utilisateur a entré un chiffre
            choix = int(text)
            if 1 <= choix <= 9:  # Vérifie si le choix est valide
                self.active_choix(choix)  # Exécute la fonction associée à l'option choisie
            else:
                print("Entrée invalide. Veuillez entrer un chiffre entre 1 et 9 ou 'Q' pour quitter.")
        elif text.lower() == 'q':  # Si l'utilisateur entre 'q' ou 'Q'
            self.close()
        else:
            print("Entrée invalide. Veuillez entrer un chiffre entre 1 et 9 ou 'Q' pour quitter.")

    def active_choix(self, choix):
        # Dictionnaire de correspondance entre le choix et la fonction à appeler
        fonctions = {
            1: self.activer_ajout_abonne,
            2: self.activer_supprimer_abonne,
            3: self.bibliotheque.afficher_abonnes,
            4: self.activer_ajout_document,
            5: self.activer_supprimer_document,
            6: self.bibliotheque.afficher_documents,
            7: self.activer_emprunt,
            8: self.activer_retour,
            9: self.emprunts.afficher_emprunts,
            10: self.close
        }
        fonctions[choix]()  # Appelle la fonction correspondante au choix

    def nom_valide(self, nom):
        #Validation du prenom et nom entré
        if len(nom) < 2:  # Vérifie que la longueur du nom est d'au moins 2 caractères
            return False
        for char in nom:  # Parcourt chaque caractère du nom
            if not (char.isalpha() or char in " -"):  # Vérifie si c'est une lettre, un espace ou un tiret
                return False
        return True

    def activer_ajout_abonne(self):

        # Demande et valide le prénom
        while True:
            prenom, ok1 = QInputDialog.getText(self, "Ajouter un abonné", "Entrez le prénom de l'abonné :")
            if not ok1:  # Si l'utilisateur annule la saisie, on quitte la fonction
                return
            if self.nom_valide(prenom):  # Vérifie que le prénom est valide
                break
            self.afficher_message("Le prénom doit contenir au moins 2 lettres et ne peut contenir que des lettres, espaces ou tirets.","Erreur")

        # Demande et valide le nom
        while True:
            nom, ok2 = QInputDialog.getText(self, "Ajouter un abonné", "Entrez le nom de l'abonné :")
            if not ok2:  # Si l'utilisateur annule, on quitte la fonction
                return
            if self.nom_valide(nom):  # Vérifie que le nom est valide
                break
            self.afficher_message("Le nom doit contenir au moins 2 lettres et ne peut contenir que des lettres, espaces ou tirets.","Erreur")

        # Ajoute l'abonné à la bibliothèque si les entrées sont valides
        if self.bibliotheque.ajouter_abonne(prenom, nom):
            self.afficher_message(f"Abonné {prenom} {nom} ajouté avec succès.")
        else:
            self.afficher_message("Abonné déjà existant.", "Erreur")

    def activer_supprimer_abonne(self):
        # Récupérer la liste des abonnés depuis la base de données
        self.bibliotheque.db.cur.execute("SELECT prenom, nom FROM Abonnes")
        abonnes = self.bibliotheque.db.cur.fetchall()

        if not abonnes:
            self.afficher_message("Aucun abonné à supprimer.")
            return

        # Transformer les tuples en une liste de noms pour l'affichage
        abonnes_str = [f"{prenom} {nom}" for prenom, nom in abonnes]

        # Afficher la liste déroulante pour choisir un abonné à supprimer
        abonne, ok = QInputDialog.getItem(self, "Supprimer un abonné", "Choisir l'abonné à supprimer :", abonnes_str, 0,False)

        if ok:
            prenom, nom = abonne.split()
            self.bibliotheque.supprimer_abonne(prenom, nom)

    def activer_ajout_document(self):
        classification, ok = QInputDialog.getItem(self, "Ajouter un document", "Choisir le type de document :",
                                                  ["Livre", "Bande Dessinee"], 0, False)
        if not ok:
            return

        titre, ok1 = QInputDialog.getText(self, "Ajouter un document", "Entrez le titre du document :")
        if not ok1 or not titre.strip():
            return

        auteur, ok2 = QInputDialog.getText(self, "Ajouter un document", "Entrez l'auteur :")
        if not ok2 or not auteur.strip():
            return

        if classification.lower() == "livre":
            document = Livre(titre.strip(), auteur.strip())
        else:
            dessinateur, ok3 = QInputDialog.getText(self, "Ajouter une bande dessinée", "Entrez le dessinateur :")
            if not ok3 or not dessinateur.strip():
                return
            document = BandeDessinee(titre.strip(), auteur.strip(), dessinateur.strip())

        if self.bibliotheque.ajouter_document(document):
            self.afficher_message(f"Document '{titre}' ajouté avec succès.")
        else:
            self.afficher_message("Document déjà existant.", "Erreur")

    def activer_supprimer_document(self):
        # Récupérer la liste des documents depuis la base de données
        self.bibliotheque.db.cur.execute("SELECT titre FROM Documents")
        documents = self.bibliotheque.db.cur.fetchall()

        if not documents:
            self.afficher_message("Aucun document à supprimer.")
            return

        # Transformer les résultats SQL en une liste de titres
        documents_str = [titre[0] for titre in documents]

        # Afficher la liste déroulante pour choisir un document à supprimer
        titre, ok = QInputDialog.getItem(self, "Supprimer un document", "Choisir le document à supprimer :",
                                         documents_str, 0, False)

        if ok:
            self.bibliotheque.supprimer_document(titre)

    def activer_emprunt(self):
        # Récupérer la liste des livres empruntables (non empruntés)
        self.bibliotheque.db.cur.execute("""
            SELECT titre FROM Documents
            WHERE type = 'Livre' AND id NOT IN (SELECT document_id FROM Emprunts)
        """)
        documents = self.bibliotheque.db.cur.fetchall()
        documents_str = [doc[0] for doc in documents]

        if not documents_str:
            self.afficher_message("Aucun document empruntable.")
            return

        # Récupérer la liste des abonnés
        self.bibliotheque.db.cur.execute("SELECT id, prenom, nom FROM Abonnes")
        abonnes = self.bibliotheque.db.cur.fetchall()
        abonnés_str = [f"{prenom} {nom}" for _, prenom, nom in abonnes]
        abonne_id_map = {f"{prenom} {nom}": id for id, prenom, nom in abonnes}  # Associer ID avec nom complet

        if not abonnés_str:
            self.afficher_message("Aucun abonné enregistré.")
            return

        # Sélectionner un abonné via la liste déroulante
        abonne, ok_abonne = QInputDialog.getItem(self, "Choisir un abonné", "Choisir l'abonné qui emprunte le livre : ",
                                                 abonnés_str, 0, False)

        if not ok_abonne:
            return

        # Récupérer l'ID de l'abonné
        abonne_id = abonne_id_map[abonne]

        # Sélectionner un document à emprunter
        titre, ok = QInputDialog.getItem(self, "Emprunter un document", "Choisir le document à emprunter : ",
                                         documents_str, 0, False)

        if ok:
            # Trouver l'ID du document
            self.bibliotheque.db.cur.execute("SELECT id FROM Documents WHERE titre = ?", (titre,))
            document_id = self.bibliotheque.db.cur.fetchone()

            if not document_id:
                self.afficher_message("Erreur : Document introuvable.", "Erreur")
                return

            self.emprunts.emprunter_document(document_id[0], abonne_id)

    def activer_retour(self):
        # Récupérer la liste des livres empruntés
        self.bibliotheque.db.cur.execute("""
            SELECT Documents.titre FROM Documents
            JOIN Emprunts ON Documents.id = Emprunts.document_id
            WHERE Documents.type = 'Livre'
        """)
        empruntes = self.bibliotheque.db.cur.fetchall()
        empruntes_str = [doc[0] for doc in empruntes]

        # Si aucun document n'est emprunté, affiche un message et retourne
        if not empruntes_str:
            self.afficher_message("Aucun document emprunté.")
            return

        # Utilise QInputDialog pour afficher une liste déroulante des documents empruntés
        titre, ok = QInputDialog.getItem(self, "Retourner un document", "Choisir le document à retourner : ",
                                         empruntes_str, 0, False)

        if ok:
            self.emprunts.retourner_document(titre)

    def close(self):
        try:
            self.bibliotheque.db.fermer_connexion()  # Fermer la connexion SQLite proprement
            print("Connexion à la base de données fermée.")
        except Exception as e:
            print(f"Erreur lors de la fermeture de la base de données : {e}")

        super().close()  # Appel à la méthode de fermeture de QWidget
