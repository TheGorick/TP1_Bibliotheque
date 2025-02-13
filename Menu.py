# Guillaume Pinat

from Bibliotheque import Bibliotheque, Emprunts, SauvegardeFichiers
from Documents import Livre, BandeDessinee

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
            self.afficher_message(
                "Le nom doit contenir au moins 2 lettres et ne peut contenir que des lettres, espaces ou tirets.",
                "Erreur"
            )

        # Ajoute l'abonné à la bibliothèque si les entrées sont valides
        if self.bibliotheque.ajouter_abonne(prenom, nom):
            self.afficher_message(f"Abonné {prenom} {nom} ajouté avec succès.")
        else:
            self.afficher_message("Abonné déjà existant.", "Erreur")

    def activer_supprimer_abonne(self):
        # Vérifie s'il y a des abonnés avant d'afficher la liste
        if not self.bibliotheque.abonnes:
            self.afficher_message("Aucun abonné à supprimer.")
            return

        # Affiche la liste des abonnés
        abonnes_str = [f"{abonne.prenom} {abonne.nom}" for abonne in self.bibliotheque.abonnes]
        abonne, ok = QInputDialog.getItem(self, "Supprimer un abonné",
                                          "Choisir l'abonné à supprimer : ",
                                          abonnes_str, 0, False)
        if ok:
            prenom, nom = abonne.split()
            self.bibliotheque.supprimer_abonne(prenom, nom)

    def activer_ajout_document(self):
        # Demande le type de document à ajouter
        classification, ok = QInputDialog.getItem(self, "Ajouter un document", "Choisir le type de document :",
                                                  ["Livre", "Bande Dessinee"], 0, False)
        if not ok:
            return

        # Demande et valide le titre du document
        while True:
            titre, ok1 = QInputDialog.getText(self, "Ajouter un document", "Entrez le titre du document :")
            if not ok1:  # Annulation
                return
            if titre.strip():  # Vérifie que le titre n'est pas vide
                break
            self.afficher_message("Le titre ne peut pas être vide.", "Erreur")

        # Demande et valide l'auteur du document
        while True:
            auteur, ok2 = QInputDialog.getText(self, "Ajouter un document", "Entrez l'auteur :")
            if not ok2:
                return
            if auteur.strip():  # Vérifie que l'auteur n'est pas vide
                break
            self.afficher_message("L'auteur ne peut pas être vide.", "Erreur")

        # Ajoute le document en fonction du type choisi
        if classification.lower() == 'livre':
            self.bibliotheque.ajouter_document(Livre(titre, auteur))

        elif classification.lower() == 'bande dessinee':
            # Demande et valide le dessinateur si c'est une bande dessinée
            while True:
                dessinateur, ok3 = QInputDialog.getText(self, "Ajouter une bande dessinée",
                                                        "Entrez le dessinateur :")
                if not ok3:
                    return
                if dessinateur.strip():  # Vérifie que le dessinateur n'est pas vide
                    break
                self.afficher_message("Le dessinateur ne peut pas être vide.", "Erreur")

            self.bibliotheque.ajouter_document(BandeDessinee(titre, auteur, dessinateur))


    def activer_supprimer_document(self):
        # Vérifie s'il y a des documents avant d'afficher la liste
        if not self.bibliotheque.documents:
            self.afficher_message("Aucun document à supprimer.")
            return

        # Affiche la liste des documents
        documents_str = [doc.titre for doc in self.bibliotheque.documents]
        titre, ok = QInputDialog.getItem(self, "Supprimer un document",
                                         "Choisir le document à supprimer : ",
                                         documents_str, 0, False)
        if ok:
            self.bibliotheque.supprimer_document(titre)

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
