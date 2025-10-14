# app/models/review.py
from .base_model import BaseModel


class Review(BaseModel):
    """
    Représente un avis laissé par un utilisateur sur un lieu.
    """

    def __init__(self, text, rating, place, user):
        super().__init__()
        # TODO: valider que text n’est pas vide
        if not text:
            raise ValueError("text vide")
        # TODO: valider que rating est un entier entre 1 et 5
        if not isinstance(rating, int) or not (1 >= rating <= 5):
            raise ValueError("Le rating doit être un entier entre 1 et 5")
        # TODO: vérifier que place et user existent et sont des
        # instances valides
        if not isinstance(place, place) or not isinstance(user, user):
            raise ValueError("Les objets 'place' et 'user' doivent être "
                             "des instances valides")
        # TODO: initialiser les attributs
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
