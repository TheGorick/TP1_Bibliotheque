# Guillaume Pinat

from Abonne import Abonne
from Documents import Livre, BandeDessinee
import csv

class Bibliotheque:
    def __init__(self):
        self.abonnes = []  # Liste des abonnés
        self.documents = []  # Liste des documents

    # Gestion des abonnés
    def ajouter_abonne(self, prenom, nom):
        """Ajoute un abonné si il n'existe pas déjà."""
        for a in self.abonnes:
            if a.prenom == prenom and a.nom == nom:
                print("Abonné déjà existant.")
                return False
        self.abonnes.append(Abonne(prenom, nom))
        print(f'Abonné {prenom} {nom} ajouté avec succès.')
        return True

    def supprimer_abonne(self, prenom, nom):
        """Supprime un abonné s'il existe."""
        for abonne in self.abonnes:
            if abonne.prenom == prenom and abonne.nom == nom:
                self.abonnes.remove(abonne)
                print(f'Abonné {prenom} {nom} supprimé avec succès.')
                return True
        print(f'Abonné {prenom} {nom} non trouvé.')
        return False

    def afficher_abonnes(self):
        """Affiche la liste des abonnés."""
        if not self.abonnes:
            print("Aucun abonné enregistré.")
        for abonne in self.abonnes:
            print(abonne)

    # Gestion des documents
    def ajouter_document(self, document):
        """Ajoute un document à la bibliothèque s'il n'existe pas déjà."""
        for doc in self.documents:
            if doc.titre == document.titre:
                print(f"Document '{document.titre}' déjà existant.")
                return False
        self.documents.append(document)  # Ajoute le document à la liste
        print(f"Document '{document}' ajouté avec succès.")
        return True

    def supprimer_document(self, titre):
        """Supprime un document s'il existe."""
        for doc in self.documents:
            if doc.titre == titre:
                self.documents.remove(doc)
                print(f"Document '{titre}' supprimé avec succès.")
                return True
        print(f"Document '{titre}' non trouvé.")  # Si le document n'est pas trouvé
        return False

    def afficher_documents(self):
        """Affiche la liste des documents."""
        if not self.documents:
            print("Aucun document enregistré.")
        for doc in self.documents:
            print(doc)

class Emprunts:
    def __init__(self, bibliotheque):
        self.bibliotheque = bibliotheque  # Référence à la bibliothèque
        self.emprunts = []  # Liste des emprunts

    def emprunter_document(self, titre, abonne):
        """Permet à un abonné d'emprunter un document s'il est disponible."""
        for doc in self.bibliotheque.documents:
            if isinstance(doc, Livre) and doc.titre == titre:
                if doc.disponible:
                    doc.disponible = False  # Le document n'est plus disponible
                    # Ajoute l'emprunt dans la liste des emprunts avec l'abonné
                    self.emprunts.append({'titre': titre, 'abonne': abonne.prenom + " " + abonne.nom})
                    print(f"{abonne.prenom} {abonne.nom} a emprunté '{titre}' avec succès.")
                    return
                else:
                    print(f"Le document '{titre}' n'est plus disponible.")
                    return
        print(f"Le document '{titre}' n'a pas été trouvé.")

    def retourner_document(self, titre):
        """Permet de retourner un document emprunté."""
        for doc in self.bibliotheque.documents:
            if isinstance(doc, Livre) and doc.titre == titre:
                doc.retourner()
                return
        print(f'Livre {titre} non trouvé ou déjà retourné.')

    def afficher_emprunts(self):
        """Affiche la liste des emprunts en cours."""
        if not self.emprunts:
            print("Aucun livre emprunté.")
        else:
            for emprunt in self.emprunts:
                print(f"Document: {emprunt['titre']}, Emprunté par: {emprunt['abonne']}")

class SauvegardeFichiers:
    """Classe pour gérer la sauvegarde des données dans des fichiers txt."""

    @staticmethod
    def sauvegarder_abonnes(abonnes, fichier="abonnes.txt"):
        """Sauvegarde la liste des abonnés dans un fichier."""
        with open(fichier, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Prenom", "Nom"])
            for abonne in abonnes:
                writer.writerow([abonne.prenom, abonne.nom])

    @staticmethod
    def sauvegarder_documents(documents, fichier="biblio.txt"):
        """Sauvegarde la liste des documents dans un fichier."""
        with open(fichier, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Titre", "Auteur", "Type", "Dessinateur"])
            for doc in documents:
                if isinstance(doc, Livre):
                    writer.writerow([doc.titre, doc.auteur, "Livre", ""])
                elif isinstance(doc, BandeDessinee):
                    writer.writerow([doc.titre, doc.auteur, "Bande Dessinee", doc.dessinateur])

    @staticmethod
    def sauvegarder_emprunts(emprunts, fichier="emprunts.txt"):
        """Sauvegarde la liste des emprunts dans un fichier."""
        with open(fichier, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Titre", "Emprunté par"])
            for emprunt in emprunts:
                writer.writerow([emprunt['titre'], emprunt['abonne']])