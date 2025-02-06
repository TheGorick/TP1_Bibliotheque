# Guillaume Pinat

from Bibliotheque import Bibliotheque, Emprunts, SauvegardeFichiers
from Documents import Livre, BandeDessinee

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QInputDialog, QMessageBox
from functools import partial

class Menu(QWidget):
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
                print("Option invalide, veuillez entrer un chiffre entre 1 et 9.")
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

    def activer_ajout_abonne(self):
        # Demande le prénom de l'abonné via un QInputDialog
        prenom, ok1 = QInputDialog.getText(self, "Ajouter un abonné", "Entrez le prénom de l'abonné :")
        if not ok1:  # Si l'utilisateur annule la saisie
            return

        # Demande le nom de l'abonné
        nom, ok2 = QInputDialog.getText(self, "Ajouter un abonné", "Entrez le nom de l'abonné :")
        if not ok2:
            return

        # Ajoute l'abonné à la bibliothèque si l'entrée est valide
        if self.bibliotheque.ajouter_abonne(prenom, nom):
            self.afficher_message(f"Abonné {prenom} {nom} ajouté avec succès.")
        else:
            self.afficher_message("Abonné déjà existant.", "Erreur")

    def activer_supprimer_abonne(self):
        # Récupère une liste des abonnés sous forme de texte "Prénom Nom"
        abonnes_str = [f"{abonne.prenom} {abonne.nom}" for abonne in self.bibliotheque.abonnes]

        # Utilise QInputDialog pour afficher la liste des abonnés
        abonne, ok = QInputDialog.getItem(self, "Supprimer un abonné",
                                          "Choisir l'abonné à supprimer : ",
                                          abonnes_str, 0, False)
        if ok:  # Si un abonné est sélectionné
            # Sépare le prénom et le nom à partir du texte sélectionné
            prenom, nom = abonne.split()
            self.bibliotheque.supprimer_abonne(prenom, nom)  # Supprime l'abonné sélectionné

    def activer_ajout_document(self):
        # Demande le type de document à ajouter
        classification, ok = QInputDialog.getItem(self, "Ajouter un document", "Choisir le type de document :",
                                                  ["Livre", "Bande Dessinee"], 0, False)
        if not ok:
            return

        # Demande le titre et l'auteur du document
        titre, ok1 = QInputDialog.getText(self, "Ajouter un document", "Entrez le titre du document :")
        if not ok1:
            return

        auteur, ok2 = QInputDialog.getText(self, "Ajouter un document", "Entrez l'auteur :")
        if not ok2:
            return

        # Ajoute le document en fonction du type choisi
        if classification.lower() == 'livre':
            self.bibliotheque.ajouter_document(Livre(titre, auteur))
        elif classification.lower() == 'bande dessinee':
            # Demande le dessinateur si c'est une bande dessinée
            dessinateur, ok3 = QInputDialog.getText(self, "Ajouter une bande dessinée", "Entrez le dessinateur :")
            if not ok3:
                return
            self.bibliotheque.ajouter_document(BandeDessinee(titre, auteur, dessinateur))

    def activer_supprimer_document(self):
        # Récupère une liste des titres des documents
        documents_str = [doc.titre for doc in self.bibliotheque.documents]

        # Utilise QInputDialog pour afficher la liste des documents
        document, ok = QInputDialog.getItem(self, "Supprimer un document",
                                            "Choisir le document à supprimer : ",
                                            documents_str, 0, False)
        if ok:  # Si un document est sélectionné
            self.bibliotheque.supprimer_document(document)  # Supprime le document sélectionné

    def activer_emprunt(self):
        # Crée une liste des titres des documents empruntables (en excluant ceux déjà empruntés)
        documents_str = [doc.titre for doc in self.bibliotheque.documents if isinstance(doc, Livre) and doc.disponible]

        # Si aucun document n'est empruntable, affiche un message et retourne
        if not documents_str:
            self.afficher_message("Aucun document empruntable.")
            return

        # Demande à l'utilisateur de choisir un abonné parmi ceux enregistrés
        abonnés_str = [f"{abonne.prenom} {abonne.nom}" for abonne in self.bibliotheque.abonnes]

        # Si aucun abonné n'est disponible, affiche un message et retourne
        if not abonnés_str:
            self.afficher_message("Aucun abonné enregistré.")
            return

        abonne, ok_abonne = QInputDialog.getItem(self, "Choisir un abonné", "Choisir l'abonné qui emprunte le livre : ",
                                                 abonnés_str, 0, False)

        if not ok_abonne:
            return

        # Demande à l'utilisateur de choisir le document à emprunter
        titre, ok = QInputDialog.getItem(self, "Emprunter un document", "Choisir le document à emprunter : ",
                                         documents_str, 0, False)

        if ok:
            # Récupère l'objet abonné correspondant
            abonne_objet = None
            for a in self.bibliotheque.abonnes:
                if f"{a.prenom} {a.nom}" == abonne:
                    abonne_objet = a
                    break

            self.emprunts.emprunter_document(titre, abonne_objet)


    def activer_retour(self):
        # Crée une liste des titres des documents empruntés
        empruntes_str = [doc.titre for doc in self.bibliotheque.documents if
                         isinstance(doc, Livre) and not doc.disponible]

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
        # Avant de fermer, on sauvegarde les données
        try:
            SauvegardeFichiers.sauvegarder_abonnes(self.bibliotheque.abonnes)
            SauvegardeFichiers.sauvegarder_documents(self.bibliotheque.documents)
            SauvegardeFichiers.sauvegarder_emprunts(self.emprunts.emprunts)
        except Exception as e:
            print(f'Erreur : {e}')
        super().close()  # Appel à la méthode de fermeture de QWidget
