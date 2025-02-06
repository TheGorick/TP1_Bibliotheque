#Guillaume Pinat

class Documents:
    _compteur_id = 0

    def __init__(self, titre, auteur):
        Documents._compteur_id += 1
        self._id = Documents._compteur_id
        self.titre = titre
        self.auteur = auteur

    def __str__(self):
        return f"[{self.__class__.__name__}] ID: {self._id} | Titre: {self.titre} | Auteur: {self.auteur}]"

class Livre(Documents):
    def __init__(self, titre, auteur):
        super().__init__(titre, auteur)
        self.disponible = True

    def emprunter(self):
        if self.disponible:
            self.disponible = False
            print(f"Le livre '{self.titre}' a été emprunté.")
        else:
            print(f"Le livre '{self.titre}' est déjà emprunté.")

    def retourner(self):
        self.disponible = True
        print(f"Le livre '{self.titre}' est maintenant disponible.")

    def __str__(self):
        return super().__str__() + f" | Disponibilité: {'Oui' if self.disponible else 'Non'}"


class BandeDessinee(Documents):
    def __init__(self, titre, auteur, dessinateur):
        super().__init__(titre, auteur)
        self.dessinateur = dessinateur

    def __str__(self):
        return super().__str__() + f" | Dessinateur: {self.dessinateur}"