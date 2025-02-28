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

        abonnes_str = [f"{prenom} {nom}" for prenom, nom in abonnes]

        abonne, ok = QInputDialog.getItem(self, "Supprimer un abonné", "Choisir l'abonné à supprimer :", abonnes_str, 0,
                                          False)

        if ok:
            prenom, nom = abonne.split()
            success, message = self.bibliotheque.supprimer_abonne(prenom, nom)

            # Afficher le message en pop-up
            self.afficher_message(message)

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
        # Récupérer tous les documents disponibles
        self.bibliotheque.db.cur.execute("SELECT id, titre FROM Documents")
        documents = self.bibliotheque.db.cur.fetchall()

        if not documents:
            self.afficher_message("Aucun document à supprimer.")
            return

        documents_str = [f"{doc_id} - {titre}" for doc_id, titre in documents]

        doc_selection, ok = QInputDialog.getItem(self, "Supprimer un document", "Choisir le document à supprimer :",
                                                 documents_str, 0, False)

        if ok:
            document_id = int(doc_selection.split(" - ")[0])  # Extraire l'ID du document
            success, message = self.bibliotheque.supprimer_document(document_id)

            # Afficher le message en pop-up
            self.afficher_message(message)

    def activer_emprunt(self):
        # Récupération des livres empruntables avec ID et titre pour éviter les conflits
        self.bibliotheque.db.cur.execute("""
            SELECT id, titre FROM Documents
            WHERE type = 'Livre' AND id NOT IN (SELECT document_id FROM Emprunts)
        """)
        documents = self.bibliotheque.db.cur.fetchall()
        documents_str = [f"{doc_id} - {titre}" for doc_id, titre in documents]  # ✅ Utilisation de l'ID

        # Récupération des abonnés directement sous forme "ID - Prénom Nom"
        self.bibliotheque.db.cur.execute("SELECT id, prenom, nom FROM Abonnes")
        abonnes = self.bibliotheque.db.cur.fetchall()
        abonnés_str = [f"{id_abonne} - {prenom} {nom}" for id_abonne, prenom, nom in
                       abonnes]  # ✅ Plus besoin de `abonne_id_map`

        # Sélection du document avec son ID
        document_selection, ok_doc = QInputDialog.getItem(self, "Emprunter un document",
                                                          "Choisir le document à emprunter :", documents_str, 0, False)
        if not ok_doc:
            return
        document_id = int(document_selection.split(" - ")[0])  # ✅ Récupération directe de l'ID

        # Sélection de l'abonné via son ID
        abonne_selection, ok_abonne = QInputDialog.getItem(self, "Choisir un abonné", "Choisir l'abonné qui emprunte :",
                                                           abonnés_str, 0, False)
        if not ok_abonne:
            return
        abonne_id = int(abonne_selection.split(" - ")[0])

        success, message = self.emprunts.emprunter_document(document_id, abonne_id)  # ✅ Retourne un message
        self.afficher_message(message)  # ✅ Affiche en pop-up

    def activer_retour(self):
        # Récupérer les livres empruntés avec leur ID et titre
        self.bibliotheque.db.cur.execute("""
            SELECT Documents.id, Documents.titre FROM Documents
            JOIN Emprunts ON Documents.id = Emprunts.document_id
            WHERE Documents.type = 'Livre'
        """)
        empruntes = self.bibliotheque.db.cur.fetchall()
        empruntes_str = [f"{doc_id} - {titre}" for doc_id, titre in empruntes]  # ✅ Utilisation de l'ID

        if not empruntes_str:
            self.afficher_message("Aucun document emprunté.")
            return

        # Sélectionner un document par son ID
        document_selection, ok = QInputDialog.getItem(self, "Retourner un document",
                                                      "Choisir le document à retourner :", empruntes_str, 0, False)
        if not ok:
            return
        document_id = int(document_selection.split(" - ")[0])  # ✅ Extraction directe de l'ID

        # Exécuter le retour du document et afficher le message
        success, message = self.emprunts.retourner_document(document_id)
        self.afficher_message(message)  # ✅ Affichage du message en pop-up

    def close(self):
        try:
            self.bibliotheque.db.fermer_connexion()  # Fermer la connexion SQLite proprement
            print("Connexion à la base de données fermée.")
        except Exception as e:
            print(f"Erreur lors de la fermeture de la base de données : {e}")

        super().close()  # Appel à la méthode de fermeture de QWidget
