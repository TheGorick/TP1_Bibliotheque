#Guillaume Pinat

class Abonne:
    _compteur_id = 0

    def __init__(self, prenom, nom):
        Abonne._compteur_id += 1
        self._id = Abonne._compteur_id
        self.prenom = prenom
        self.nom = nom

    def __str__(self):
        return f' ID: {self.get_id()} Prénom: {self.prenom} Nom: {self.nom}'

    # getters
    def get_id(self):
        return self._id

    def get_prenom(self):
        return self.prenom

    def get_nom(self):
        return self.nom

    # setters
    def set_prenom(self, prenom):
        self.prenom = prenom

    def set_nom(self, nom):
        self.nom = nom