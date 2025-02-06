# Guillaume Pinat

from Abonne import Abonne
from Documents import Livre, BandeDessinee
import csv

class Bibliotheque:
    def __init__(self):
        # Initialisation des listes pour les abonnés, documents, et emprunts
        self.abonnes = []
        self.documents = []
        self.emprunts = []

    # Gestion des abonnés
    def ajouter_abonne(self, prenom, nom):
        # Vérifie si l'abonné existe déjà avant de l'ajouter
        for a in self.abonnes:
            if a.prenom == prenom and a.nom == nom:
                print("Abonné déjà existant.")
                return False  # Abonné déjà existant
        self.abonnes.append(Abonne(prenom, nom))  # Ajoute l'abonné
        print(f'Abonné {prenom} {nom} ajouté avec succès.')
        return True

    def supprimer_abonne(self, prenom, nom):
        # Recherche et supprime l'abonné correspondant
        for abonne in self.abonnes:
            if abonne.prenom == prenom and abonne.nom == nom:
                self.abonnes.remove(abonne)
                print(f'Abonné {prenom} {nom} supprimé avec succès.')
                return True
        print(f'Abonné {prenom} {nom} non trouvé.')  # Si l'abonné n'est pas trouvé
        return False

    def afficher_abonnes(self):
        # Affiche la liste des abonnés ou un message si la liste est vide
        if not self.abonnes:
            print("Aucun abonné enregistré.")
        for abonne in self.abonnes:
            print(abonne)

    # Gestion des documents
    def ajouter_document(self, titre):
        # Vérifie si le document existe déjà avant de l'ajouter
        for doc in self.documents:
            if doc.titre == titre:
                print(f"Document '{titre}' déjà existant.")
                return False
        self.documents.append(titre)  # Ajoute le document à la liste
        print(f"Document '{titre}' ajouté avec succès.")
        return True

    def supprimer_document(self, titre):
        # Recherche et supprime le document correspondant
        for doc in self.documents:
            if doc.titre == titre:
                self.documents.remove(doc)
                print(f"Document '{titre}' supprimé avec succès.")
                return True
        print(f"Document '{titre}' non trouvé.")  # Si le document n'est pas trouvé
        return False

    def afficher_documents(self):
        # Affiche la liste des documents ou un message si la liste est vide
        if not self.documents:
            print("Aucun document enregistré.")
        for doc in self.documents:
            print(doc)

    # Gestion des emprunts
    def emprunter_document(self, titre, abonne):
        # Recherche le document à emprunter
        for doc in self.documents:
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
        # Recherche si le document est un livre et si il peut être retourné
        for doc in self.documents:
            if isinstance(doc, Livre) and doc.titre == titre:
                doc.retourner()  # Appelle la méthode retourner du livre
                return
        print(f'Livre {titre} non trouvé ou déjà retourné.')  # Si le livre n'est pas trouvé ou déjà retourné

    def afficher_emprunts(self):
        if not self.emprunts:
            print("Aucun livre emprunté.")
        else:
            for emprunt in self.emprunts:
                print(
                    f"Document: {emprunt['titre']}, Emprunté par: {emprunt['abonne']}")

    # Sauvegarde des données dans des fichiers txt
    def sauvegarder_donnees(self):
        # Sauvegarde des abonnés dans le fichier "abonnes.txt"
        with open("abonnes.txt", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Prenom", "Nom"])  # Entête
            for abonne in self.abonnes:
                writer.writerow([abonne.prenom, abonne.nom])

        # Sauvegarde des documents dans le fichier "biblio.txt"
        with open("biblio.txt", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Titre", "Auteur", "Type", "Dessinateur"])  # Entête
            for doc in self.documents:
                if isinstance(doc, Livre):
                    writer.writerow([doc.titre, doc.auteur, "Livre", ""])  # Sauvegarde les livres
                elif isinstance(doc, BandeDessinee):
                    writer.writerow([doc.titre, doc.auteur, "Bande Dessinee", doc.dessinateur])  # Sauvegarde les BD

        # Sauvegarde des emprunts dans le fichier "emprunts.txt"
        with open("emprunts.txt", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Titre", "Emprunté par"])  # Entête
            for emprunt in self.emprunts:
                # Accède à 'abonne' au lieu de 'emprunteur'
                writer.writerow([emprunt['titre'], emprunt['abonne']])