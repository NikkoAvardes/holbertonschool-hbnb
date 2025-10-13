# app/models/review.py
from .base_model import BaseModel

class Review(BaseModel):
    """
    Représente un avis laissé par un utilisateur sur un lieu.
    """

    def __init__(self, text, rating, place, user):
        super().__init__()
        # TODO: valider que text n’est pas vide
        # TODO: valider que rating est un entier entre 1 et 5
        # TODO: vérifier que place et user existent et sont des instances valides
        # TODO: initialiser les attributs
        pass
